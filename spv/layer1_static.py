"""
SPV Layer 1: Static Analysis

AST-based pattern detection for known anti-patterns in generated code.
23 rules designed on the development split (75 tasks).

Each rule returns a list of findings with severity and description.

Rule families
-------------
* S01-S12  BigQuery SQL   (sqlglot AST + a dialect-aware call scanner)
* A01-A06  Airflow DAGs   (Python ``ast``)
* P01-P05  Python / ETL   (Python ``ast``)

SQL rules accept an optional ``schema`` argument in the corpus format::

    {"orders": {"columns": {"order_id": {"type": "INT64",
                                         "description": "Primary key"}}}}

Without a schema the rules fall back to naming heuristics and report with a
lower severity where the evidence is weaker.

If ``sqlglot`` is not installed the AST-based SQL rules degrade gracefully:
S03 and S10 keep working (they use the call scanner), S06/S08/S12 use regex
fallbacks, and the remaining SQL rules return no findings.
"""

from __future__ import annotations

import ast
import logging
import re
from dataclasses import dataclass
from functools import lru_cache
from typing import Callable, Iterable, Iterator

try:  # graceful degradation: the module must import without sqlglot
    import sqlglot
    from sqlglot import exp

    SQLGLOT_AVAILABLE = True
except Exception:  # pragma: no cover - exercised only when sqlglot is absent
    sqlglot = None  # type: ignore[assignment]
    exp = None  # type: ignore[assignment]
    SQLGLOT_AVAILABLE = False

logger = logging.getLogger(__name__)


@dataclass
class Finding:
    rule_id: str
    severity: str  # "high", "medium", "low"
    description: str
    line: int | None = None
    failure_mode: str | None = None  # FM1-FM7


# ---------------------------------------------------------------------------
# Generic helpers
# ---------------------------------------------------------------------------

def _strip_code_fences(code: str) -> str:
    """Blank out everything outside markdown code fences (LLM output often
    arrives fenced). Line numbers are preserved."""
    if "```" not in code:
        return code
    out: list[str] = []
    inside = False
    kept = False
    for line in code.split("\n"):
        if line.strip().startswith("```"):
            inside = not inside
            out.append("")
            continue
        if inside:
            out.append(line)
            kept = kept or bool(line.strip())
        else:
            out.append("")
    return "\n".join(out) if kept else code


def _line_at(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def _finalize(findings: list[Finding]) -> list[Finding]:
    """De-duplicate and order findings by line."""
    seen: set[tuple] = set()
    unique: list[Finding] = []
    for f in findings:
        key = (f.rule_id, f.line, f.description)
        if key not in seen:
            seen.add(key)
            unique.append(f)
    unique.sort(key=lambda f: (f.line is None, f.line or 0))
    return unique


def _short(text: str, limit: int = 80) -> str:
    text = " ".join(str(text).split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


# ---------------------------------------------------------------------------
# Schema model (optional input for SQL rules)
# ---------------------------------------------------------------------------

_INT_TYPES = {"INT64", "INT", "INTEGER", "BIGINT", "SMALLINT", "TINYINT", "BYTEINT"}
_FLOAT_TYPES = {"FLOAT64", "FLOAT", "DOUBLE", "NUMERIC", "BIGNUMERIC", "DECIMAL", "BIGDECIMAL"}
_STRING_TYPES = {"STRING", "VARCHAR", "TEXT", "CHAR"}


def _type_family(type_name: str | None) -> str | None:
    if not type_name:
        return None
    base = re.split(r"[<(]", str(type_name).strip().upper(), maxsplit=1)[0].strip()
    if base in _INT_TYPES or base in _FLOAT_TYPES:
        return "number"
    if base in _STRING_TYPES:
        return "string"
    if base in {"BOOL", "BOOLEAN"}:
        return "bool"
    if base in {"DATE", "TIMESTAMP", "DATETIME", "TIME", "BYTES"}:
        return base.lower()
    return None


_FAMILY_COMPATIBLE = {frozenset({"number"}), frozenset({"string"}), frozenset({"bool"}),
                      frozenset({"date"}), frozenset({"timestamp"}), frozenset({"datetime"}),
                      frozenset({"time"}), frozenset({"bytes"})}

_PK_DESC_RE = re.compile(r"primary\s+key|\bunique\s+(id|identifier|key)\b", re.I)
_FK_DESC_RE = re.compile(r"foreign\s+key|\breferences\b", re.I)
_DUP_DESC_RE = re.compile(r"\bmultiple\b|\bduplicate|one-to-many|many-to-|not\s+unique|non-unique", re.I)
_NULLABLE_DESC_RE = re.compile(
    r"\bnullable\b|\bnull\b|\boptional\b|may\s+be\s+(missing|empty|absent)|can\s+be\s+(missing|empty)", re.I)
_NOT_NULL_DESC_RE = re.compile(r"not\s+null|non-null|never\s+null|\brequired\b", re.I)
_PARTITION_TABLE_KEYS = ("partition_column", "partitioned_by", "partition_by", "partitioning",
                         "time_partitioning", "partition")
_PARTITION_DESC_RE = re.compile(r"partition(?:ed)?\s+(?:by|on)\s+`?([A-Za-z_]\w*)`?", re.I)


class _Schema:
    """Normalised, case-insensitive view over a corpus-style schema dict."""

    def __init__(self, raw: dict | None):
        self.tables: dict[str, dict[str, dict]] = {}
        self.table_meta: dict[str, dict] = {}
        if not isinstance(raw, dict):
            return
        for tname, tdef in raw.items():
            if not isinstance(tdef, dict):
                continue
            cols = tdef.get("columns", None)
            if cols is None:
                # allow {"table": {"col": "TYPE"}} shorthand
                if tdef and all(isinstance(v, (str, dict)) for v in tdef.values()) and not any(
                        k in tdef for k in ("type", "description")):
                    cols = tdef
                else:
                    continue
            norm: dict[str, dict] = {}
            if isinstance(cols, dict):
                for cname, cdef in cols.items():
                    norm[str(cname).lower()] = cdef if isinstance(cdef, dict) else {"type": str(cdef)}
            elif isinstance(cols, list):
                for cdef in cols:
                    if isinstance(cdef, dict) and cdef.get("name"):
                        norm[str(cdef["name"]).lower()] = cdef
            if norm:
                key = self.basename(str(tname))
                self.tables[key] = norm
                self.table_meta[key] = tdef

    def __bool__(self) -> bool:
        return bool(self.tables)

    @staticmethod
    def basename(name: str) -> str:
        return name.replace("`", "").split(".")[-1].lower()

    def has_table(self, table: str | None) -> bool:
        return bool(table) and table in self.tables

    def column(self, table: str | None, col: str) -> dict | None:
        if not table:
            return None
        return self.tables.get(table, {}).get(col.lower())

    def col_type(self, table: str | None, col: str) -> str | None:
        info = self.column(table, col)
        return str(info.get("type")).upper() if info and info.get("type") else None

    def types_by_name(self, col: str) -> set[str]:
        """All declared types of a column name across tables."""
        out = set()
        for cols in self.tables.values():
            info = cols.get(col.lower())
            if info and info.get("type"):
                out.add(str(info["type"]).upper())
        return out

    def _is_pk(self, table: str, col: str) -> bool:
        info = self.column(table, col) or {}
        if info.get("primary_key") is True:
            return True
        desc = str(info.get("description", ""))
        if _PK_DESC_RE.search(desc) and not _DUP_DESC_RE.search(desc):
            return True
        pk = self.table_meta.get(table, {}).get("primary_key")
        if isinstance(pk, str):
            return pk.lower() == col.lower()
        if isinstance(pk, (list, tuple)) and len(pk) == 1:
            return str(pk[0]).lower() == col.lower()
        return False

    def _has_pk_info(self, table: str) -> bool:
        if self.table_meta.get(table, {}).get("primary_key"):
            return True
        return any(self._is_pk(table, c) for c in self.tables.get(table, {}))

    def is_unique(self, table: str | None, col: str) -> bool | None:
        """True = one row per value, False = may repeat, None = unknown."""
        info = self.column(table, col)
        if info is None or table is None:
            return None
        if self._is_pk(table, col):
            return True
        desc = str(info.get("description", ""))
        if info.get("foreign_key") or _FK_DESC_RE.search(desc) or _DUP_DESC_RE.search(desc):
            return False
        if info.get("unique") is True:
            return True
        if self._has_pk_info(table):
            return False
        return None

    def is_nullable(self, table: str | None, col: str) -> bool | None:
        info = self.column(table, col)
        if info is None or table is None:
            return None
        mode = str(info.get("mode", "")).upper()
        if mode == "REQUIRED":
            return False
        if mode == "NULLABLE":
            return True
        if isinstance(info.get("nullable"), bool):
            return info["nullable"]
        desc = str(info.get("description", ""))
        if _NOT_NULL_DESC_RE.search(desc):
            return False
        if _NULLABLE_DESC_RE.search(desc):
            return True
        if self._is_pk(table, col):
            return False
        return None

    def partition_columns(self, table: str | None) -> list[str]:
        if not self.has_table(table):
            return []
        meta = self.table_meta.get(table, {})
        out: list[str] = []
        for key in _PARTITION_TABLE_KEYS:
            val = meta.get(key)
            if not val:
                continue
            if isinstance(val, str):
                out.append(val)
            elif isinstance(val, (list, tuple)):
                out.extend(str(v) for v in val)
            elif isinstance(val, dict):
                out.append(str(val.get("field") or val.get("column") or "_PARTITIONTIME"))
            elif val is True:
                out.append("_PARTITIONTIME")
        m = _PARTITION_DESC_RE.search(str(meta.get("description", "")))
        if m:
            out.append(m.group(1))
        for cname, info in self.tables[table].items():
            if info.get("partition") or info.get("is_partition") or info.get("partitioned"):
                out.append(cname)
            elif re.search(r"\bpartition", str(info.get("description", "")), re.I):
                out.append(cname)
        return sorted({c.lower() for c in out})

    def temporal_columns(self, table: str | None) -> list[str]:
        if not self.has_table(table):
            return []
        return sorted(c for c, info in self.tables[table].items()
                      if _type_family(info.get("type")) in {"date", "timestamp", "datetime"})


# ---------------------------------------------------------------------------
# SQL helpers: parsing
# ---------------------------------------------------------------------------

_JINJA_EXPR_RE = re.compile(r"\{\{.*?\}\}", re.S)
_JINJA_STMT_RE = re.compile(r"\{%.*?%\}|\{#.*?#\}", re.S)


def _keep_newlines(match: re.Match, fill: str = "") -> str:
    text = match.group(0)
    return fill + "\n" * text.count("\n")


@lru_cache(maxsize=256)
def _parse_sql(sql: str) -> tuple:
    """Parse SQL into sqlglot trees (BigQuery dialect first). Returns () when
    sqlglot is unavailable or the text cannot be parsed. Trees are cached and
    must be treated as read-only by the rules."""
    if not SQLGLOT_AVAILABLE or not sql or not sql.strip():
        return ()
    text = _strip_code_fences(sql)
    candidates = [text]
    if "{{" in text or "{%" in text or "{#" in text:
        dejinja = _JINJA_STMT_RE.sub(lambda m: _keep_newlines(m), text)
        # '{{ ds }}' (quoted) stays a string literal; a bare {{ x }} becomes an identifier
        dejinja = re.sub(r"(?<!['\"])\{\{.*?\}\}(?!['\"])",
                         lambda m: _keep_newlines(m, "jinja_placeholder"), dejinja, flags=re.S)
        candidates.append(dejinja)
    for candidate in candidates:
        for dialect in ("bigquery", None):
            try:
                trees = [t for t in sqlglot.parse(candidate, read=dialect) if t is not None]
            except Exception:
                continue
            if trees:
                _annotate_lines(trees, candidate)
                return tuple(trees)
    logger.debug("layer1_static: could not parse SQL; AST rules skipped")
    return ()


def _annotate_lines(trees: list, text: str) -> None:
    """Older sqlglot releases do not record token positions on identifiers.
    When no position is present, approximate one by matching identifiers (in
    depth-first order) against successive occurrences in the source."""
    try:
        idents = [i for t in trees for i in t.find_all(exp.Identifier, bfs=False)]
    except Exception:
        return
    if not idents or any(isinstance(i.meta.get("line"), int) for i in idents):
        return
    masked = _mask_sql(text)
    cursor: dict[str, int] = {}
    for ident in idents:
        name = str(ident.this or "")
        if not name:
            continue
        key = name.lower()
        last = name.split(".")[-1]
        m = re.compile(r"(?<![\w])" + re.escape(last) + r"(?![\w])", re.I).search(masked, cursor.get(key, 0))
        if m is None:
            continue
        cursor[key] = m.end()
        ident.meta["line"] = _line_at(text, m.start())


def _node_line(node) -> int | None:
    """Best-effort source line of an AST node (min line of any positioned token)."""
    best = None
    try:
        for n in node.find_all(exp.Expression):
            line = n.meta.get("line") if n.meta else None
            if isinstance(line, int) and (best is None or line < best):
                best = line
    except Exception:
        return None
    return best


def _find_line(sql: str, pattern: str) -> int | None:
    m = re.search(pattern, sql, re.I)
    return _line_at(sql, m.start()) if m else None


def _sql_of(node) -> str:
    try:
        return node.sql(dialect="bigquery")
    except Exception:
        return str(node)


def _func_name(node) -> str:
    """Upper-case SQL function name of a sqlglot function node."""
    if node is None:
        return ""
    if isinstance(node, exp.Anonymous):
        return str(node.name).upper()
    if isinstance(node, exp.Func):
        try:
            return node.sql_name().upper()
        except Exception:
            return type(node).__name__.upper()
    return ""


def _own_nodes(root, types=None) -> Iterator:
    """Yield descendants of ``root`` without descending into nested query
    scopes (nested SELECT / subquery nodes are yielded but not entered)."""
    scope_types = (exp.Select, exp.Subquery, exp.Union)
    stack = list(root.iter_expressions())
    while stack:
        node = stack.pop()
        if types is None or isinstance(node, types):
            yield node
        if isinstance(node, scope_types):
            continue
        stack.extend(node.iter_expressions())


def _inside(node, types, stop) -> bool:
    """True if ``node`` has an ancestor of ``types`` at or below ``stop``."""
    if node is stop:
        return False
    cur = node.parent
    while cur is not None:
        if isinstance(cur, types):
            return True
        if cur is stop:
            break
        cur = cur.parent
    return False


def _select_from(sel):
    return sel.args.get("from") or sel.args.get("from_")


def _sources(sel) -> list:
    out = []
    frm = _select_from(sel)
    if frm is not None and frm.this is not None:
        out.append(frm.this)
    for j in sel.args.get("joins") or []:
        if j.this is not None:
            out.append(j.this)
    return out


def _cte_names(tree) -> set[str]:
    return {c.alias_or_name.lower() for c in tree.find_all(exp.CTE) if c.alias_or_name}


def _table_basename(table) -> str:
    return _Schema.basename(table.name or "")


def _alias_map(sel, ctes: set[str]) -> dict[str, str | None]:
    """alias (lower) -> base table name (lower) or None for CTEs/subqueries."""
    amap: dict[str, str | None] = {}
    for src in _sources(sel):
        alias = (src.alias_or_name or "").lower()
        if not alias:
            continue
        if isinstance(src, exp.Table):
            base = _table_basename(src)
            is_cte = base in ctes and not src.args.get("db")
            amap[alias] = None if is_cte else base
        else:
            amap[alias] = None
    return amap


def _resolve(col, amap: dict[str, str | None], schema: _Schema | None) -> tuple[str | None, str | None]:
    """Resolve a column to (alias, base_table). Either may be None."""
    qual = (col.table or "").lower()
    if qual:
        if qual in amap:
            return qual, amap[qual]
        return qual, None
    if schema:
        hits = [(a, t) for a, t in amap.items() if t and schema.column(t, col.name) is not None]
        if len(hits) == 1:
            return hits[0]
    if len(amap) == 1:
        (alias, table), = amap.items()
        return alias, table
    return None, None


def _col_type(col, amap, schema: _Schema | None) -> str | None:
    if not schema:
        return None
    _, table = _resolve(col, amap, schema)
    declared = schema.col_type(table, col.name)
    if declared:
        return declared
    if not (col.table or "") or table is None:
        types = schema.types_by_name(col.name)
        if len(types) == 1 and not (col.table or ""):
            return next(iter(types))
    return None


_KEY_NAME_RE = re.compile(
    r"(^id$|_id$|^id_|_ids$|^key$|_key$|_pk$|_fk$|_sk$|^uuid$|_uuid$|_guid$|_code$|^code$|"
    r"_number$|_no$|_num$|^sku$|_sku$|^email$|_email$|_hash$)", re.I)
_DATE_NAME_RE = re.compile(r"(^|_)(date|day|dt|month|week|year|hour)$", re.I)
_TS_NAME_RE = re.compile(
    r"(_at|_ts|_time|_timestamp|_tstamp)$|^(ts|timestamp|event_time|event_timestamp|created|updated)$", re.I)
_TEMPORAL_NAME_RE = re.compile(r"date|time|(^|_)(ts|dt|day)($|_)|_at$|created|updated|_partition", re.I)


def _is_key_like(name: str) -> bool:
    return bool(_KEY_NAME_RE.search(name or ""))


def _looks_like_own_pk(col: str, table: str | None) -> bool:
    """Heuristic: ``id`` or ``<singular table>_id`` is the table's own key."""
    col = (col or "").lower()
    if col in {"id", "uuid", "pk"}:
        return True
    if not table or not col.endswith("_id"):
        return False
    stem = col[:-3]
    table = table.lower()
    variants = {table, table.rstrip("s"), re.sub(r"ies$", "y", table), re.sub(r"es$", "", table)}
    return any(v == stem or v.endswith("_" + stem) for v in variants)


def _unwrap(node):
    while isinstance(node, (exp.Paren, exp.Cast, exp.Neg)) or (
            getattr(exp, "TryCast", None) and isinstance(node, exp.TryCast)):
        node = node.this
    return node


# ---------------------------------------------------------------------------
# SQL helpers: lexical call scanner (works without sqlglot)
# ---------------------------------------------------------------------------

@lru_cache(maxsize=256)
def _mask_sql(sql: str) -> str:
    """Return ``sql`` with comments and string-literal bodies replaced by
    spaces. Length and line structure are preserved so offsets map 1:1."""
    chars = list(sql)
    n = len(sql)

    def blank(a: int, b: int) -> None:
        for k in range(a, min(b, n)):
            if chars[k] != "\n":
                chars[k] = " "

    i = 0
    while i < n:
        ch = sql[i]
        two = sql[i:i + 2]
        if two == "--" or (ch == "#" and sql[i - 1:i] != "{"):
            j = sql.find("\n", i)
            j = n if j == -1 else j
            blank(i, j)
            i = j
        elif two == "/*":
            j = sql.find("*/", i + 2)
            j = n if j == -1 else j + 2
            blank(i, j)
            i = j
        elif ch in "'\"":
            quote = ch * 3 if sql[i:i + 3] == ch * 3 else ch
            j = i + len(quote)
            while j < n:
                if sql[j] == "\\":
                    j += 2
                    continue
                if sql.startswith(quote, j):
                    break
                j += 1
            blank(i + len(quote), j)
            i = min(j + len(quote), n)
        elif ch == "`":
            j = sql.find("`", i + 1)
            i = n if j == -1 else j + 1
        else:
            i += 1
    return "".join(chars)


@dataclass
class _SqlCall:
    name: str
    args: list[str]          # original text of each top-level argument
    start: int
    end: int                 # offset just past the closing parenthesis
    line: int


def _iter_sql_calls(sql: str, names: Iterable[str]) -> Iterator[_SqlCall]:
    """Find calls to the given SQL functions, with top-level argument split."""
    masked = _mask_sql(sql)
    pattern = re.compile(r"(?<![\w.`])(" + "|".join(sorted(names, key=len, reverse=True)) + r")\s*\(", re.I)
    for m in pattern.finditer(masked):
        open_pos = m.end() - 1
        depth = 0
        arg_start = open_pos + 1
        args: list[str] = []
        close = None
        for k in range(open_pos, len(masked)):
            c = masked[k]
            if c in "([":
                depth += 1
            elif c in ")]":
                depth -= 1
                if depth == 0:
                    close = k
                    break
            elif c == "," and depth == 1:
                args.append(sql[arg_start:k].strip())
                arg_start = k + 1
        if close is None:
            continue
        last = sql[arg_start:close].strip()
        if last or args:
            args.append(last)
        yield _SqlCall(m.group(1).upper(), args, m.start(), close + 1, _line_at(sql, m.start()))


_STRING_LITERAL_RE = re.compile(r"^[rRbB]{0,2}(['\"])(.*)\1$", re.S)
_SIMPLE_COLUMN_RE = re.compile(r"^`?[A-Za-z_][\w]*`?(\.`?[A-Za-z_]\w*`?)*$")


def _text_is_timestamp(text: str, schema: _Schema | None) -> bool | None:
    """Classify a SQL expression (as text): True = TIMESTAMP, False = not a
    TIMESTAMP (or already timezone-handled), None = unknown."""
    text = text.strip()
    upper = text.upper()
    if not text:
        return None
    if "AT TIME ZONE" in upper:
        return False
    if _STRING_LITERAL_RE.match(text):
        return False
    if _SIMPLE_COLUMN_RE.match(text):
        name = text.replace("`", "").split(".")[-1]
        if schema:
            types = schema.types_by_name(name)
            if types:
                if types == {"TIMESTAMP"}:
                    return True
                if "TIMESTAMP" not in types:
                    return False
                return None
        if name.upper() in {"CURRENT_TIMESTAMP"}:
            return True
        return True if _TS_NAME_RE.search(name) else None
    if re.search(r"CURRENT_TIMESTAMP|TIMESTAMP_(ADD|SUB|TRUNC|SECONDS|MILLIS|MICROS)|"
                 r"PARSE_TIMESTAMP|(?<![\w.])TIMESTAMP\s*\(", upper):
        return True
    if re.search(r"(?<![\w.])(DATETIME|DATE|PARSE_DATE|PARSE_DATETIME|DATE_TRUNC|DATE_ADD|DATE_SUB|"
                 r"DATETIME_TRUNC)\s*\(|CURRENT_DATETIME|CURRENT_DATE", upper):
        return False
    return None


# ---------------------------------------------------------------------------
# SQL RULES (S01-S12)
# ---------------------------------------------------------------------------

def _single_row_select(sel, schema: _Schema | None = None, ctes: set[str] | None = None) -> tuple[bool, str]:
    """Decide whether a SELECT provably returns at most one row.
    Returns (is_single_row, evidence_level) where evidence_level is one of
    'proven', 'likely' (key-equality filter without schema proof) or 'none'."""
    if not isinstance(sel, exp.Select):
        return False, "none"
    limit = sel.args.get("limit")
    if limit is not None:
        lim = limit.expression if limit.expression is not None else limit.this
        if lim is not None and _sql_of(lim).strip() in {"1", "0"}:
            return True, "proven"
    if _select_from(sel) is None:
        return True, "proven"
    projections = sel.expressions or []
    group = sel.args.get("group")
    if group is None and projections:
        all_agg = True
        for p in projections:
            e = p.unalias()
            nodes = [e, *_own_nodes(e)]
            if not any(isinstance(n, exp.AggFunc) and not _inside(n, exp.Window, e) for n in nodes):
                all_agg = False
                break
        if all_agg:
            return True, "proven"
    where = sel.args.get("where")
    if where is not None and group is None:
        amap = _alias_map(sel, ctes or set())
        for eq in _own_nodes(where, exp.EQ):
            for side in (eq.this, eq.expression):
                side = _unwrap(side)
                if not isinstance(side, exp.Column):
                    continue
                alias, table = _resolve(side, amap, schema)
                if alias is None or alias not in amap:
                    continue  # outer (correlated) reference
                if schema and schema.is_unique(table, side.name) is True:
                    return True, "proven"
                if (not schema or schema.is_unique(table, side.name) is None) and \
                        _looks_like_own_pk(side.name, table or alias):
                    return True, "likely"
    return False, "none"


def check_sql_missing_join_condition(sql: str, schema: dict | None = None) -> list[Finding]:
    """Rule S01: Missing or suspicious JOIN condition.

    Flags JOIN without ON/USING, CROSS / comma joins against tables, ON clauses
    that are always true, that do not relate the joined table to the rest of
    the query, that contain no equality predicate, or whose equality predicates
    do not reference key columns (many-to-many risk)."""
    if not SQLGLOT_AVAILABLE:
        return []
    findings: list[Finding] = []
    sch = _Schema(schema)
    for tree in _parse_sql(sql):
        ctes = _cte_names(tree)
        for sel in tree.find_all(exp.Select):
            joins = sel.args.get("joins") or []
            if not joins:
                continue
            amap = _alias_map(sel, ctes)
            where = sel.args.get("where")
            for j in joins:
                target = j.this
                if target is None or isinstance(target, (exp.Unnest, exp.Lateral)):
                    continue  # correlated array expansion, not a relational join
                if isinstance(target, exp.Table) and (target.args.get("db") is not None) and \
                        str(target.args["db"].name).lower() in amap and not target.args.get("catalog"):
                    continue  # FROM t, t.array_col  (implicit UNNEST)
                tname = (target.alias_or_name or _short(_sql_of(target), 40))
                talias = tname.lower()
                line = _node_line(j)
                on = j.args.get("on")
                using = j.args.get("using")
                kind = str(j.args.get("kind") or "").upper()
                method = str(j.args.get("method") or "").upper()

                if using:
                    names = [getattr(u, "name", str(u)) for u in using]
                    if names and not any(_is_key_like(n) for n in names):
                        findings.append(Finding(
                            "S01", "medium",
                            f"JOIN {tname} USING ({', '.join(names)}) joins on non-key column(s); "
                            "verify the join cardinality (many-to-many risk).", line, "FM1"))
                    continue

                if on is None:
                    if method == "NATURAL":
                        findings.append(Finding(
                            "S01", "medium",
                            f"NATURAL JOIN with {tname}: join keys are implied by column names and "
                            "change silently when the schema evolves.", line, "FM1"))
                        continue
                    if isinstance(target, exp.Subquery) and _single_row_select(target.this, sch, ctes)[0]:
                        continue  # cross join with a one-row subquery is a common, safe idiom
                    linked = False
                    if where is not None:
                        for eq in _own_nodes(where, exp.EQ):
                            quals = {(c.table or "").lower() for c in eq.find_all(exp.Column)}
                            if talias in quals and len(quals - {""}) >= 2:
                                linked = True
                                break
                    if linked:
                        continue  # old-style implicit join with the predicate in WHERE
                    if kind == "CROSS":
                        findings.append(Finding(
                            "S01", "medium",
                            f"CROSS JOIN (or comma join) with {tname} has no join predicate: every row is "
                            "paired with every row of the other side. Confirm the Cartesian product is "
                            "intended.", line, "FM1"))
                    else:
                        findings.append(Finding(
                            "S01", "high",
                            f"JOIN {tname} has no ON/USING clause; this produces a Cartesian product.",
                            line, "FM1"))
                    continue

                on_cols = list(on.find_all(exp.Column))
                if not on_cols:
                    findings.append(Finding(
                        "S01", "high",
                        f"JOIN {tname} ON {_short(_sql_of(on), 40)} is a constant condition (no columns); "
                        "the join degenerates into a Cartesian product.", line, "FM1"))
                    continue

                quals = {(c.table or "").lower() for c in on_cols}
                if "" not in quals and talias not in quals and len(amap) > 1:
                    findings.append(Finding(
                        "S01", "high",
                        f"ON clause of JOIN {tname} does not reference {tname} "
                        f"({_short(_sql_of(on), 60)}); the joined table is effectively cross-joined.",
                        line, "FM1"))
                    continue

                eq_types = (exp.EQ, exp.NullSafeEQ) if hasattr(exp, "NullSafeEQ") else (exp.EQ,)
                cross_eqs = []       # equality predicates relating two different relations
                same_side_eqs = 0
                for eq in on.find_all(*eq_types):
                    left = _unwrap(eq.this)
                    right = _unwrap(eq.expression)
                    lcols = list(left.find_all(exp.Column))
                    rcols = list(right.find_all(exp.Column))
                    if not lcols or not rcols:
                        continue  # column = literal is a filter, not a join predicate
                    lq = {(c.table or "").lower() for c in lcols}
                    rq = {(c.table or "").lower() for c in rcols}
                    if "" not in lq and "" not in rq and lq == rq:
                        same_side_eqs += 1
                        continue
                    if _sql_of(left).lower() == _sql_of(right).lower():
                        same_side_eqs += 1
                        continue
                    cross_eqs.append((eq, lcols, rcols))

                if not cross_eqs:
                    if same_side_eqs:
                        findings.append(Finding(
                            "S01", "high",
                            f"ON clause of JOIN {tname} only compares columns of the same table "
                            f"({_short(_sql_of(on), 60)}); it does not relate {tname} to the other side.",
                            line, "FM1"))
                    elif len(quals - {""}) >= 2 or "" in quals:
                        findings.append(Finding(
                            "S01", "medium",
                            f"JOIN {tname} has no equality predicate between the two sides "
                            f"({_short(_sql_of(on), 60)}); non-equi joins can match many rows per key.",
                            line, "FM1"))
                    else:
                        findings.append(Finding(
                            "S01", "high",
                            f"ON clause of JOIN {tname} contains only filters on one table "
                            f"({_short(_sql_of(on), 60)}); there is no join predicate.", line, "FM1"))
                    continue

                # Equality predicates exist: do they reference key columns?
                join_cols = [c for _, lc, rc in cross_eqs for c in (*lc, *rc)]
                key_like = False
                for c in join_cols:
                    _, table = _resolve(c, amap, sch)
                    info = sch.column(table, c.name) if sch else None
                    if _is_key_like(c.name) or (info is not None and sch.is_unique(table, c.name) is not None
                                                and (sch.is_unique(table, c.name) or info.get("foreign_key")
                                                     or _FK_DESC_RE.search(str(info.get("description", ""))))):
                        key_like = True
                        break
                if not key_like:
                    names = sorted({_sql_of(c) for c in join_cols})
                    date_only = all(_DATE_NAME_RE.search(c.name) or _TS_NAME_RE.search(c.name) for c in join_cols)
                    findings.append(Finding(
                        "S01", "low" if date_only else "medium",
                        f"JOIN {tname} is keyed on non-key column(s) {', '.join(names)}; "
                        "values are unlikely to be unique on either side (many-to-many fan-out risk).",
                        line, "FM1"))
                    continue

                if sch:
                    # Many-to-many: every equality pair is non-unique on both sides.
                    verdicts = []
                    for _, lcols, rcols in cross_eqs:
                        if len(lcols) != 1 or len(rcols) != 1:
                            continue
                        lu = sch.is_unique(_resolve(lcols[0], amap, sch)[1], lcols[0].name)
                        ru = sch.is_unique(_resolve(rcols[0], amap, sch)[1], rcols[0].name)
                        verdicts.append((lu, ru, lcols[0], rcols[0]))
                    if verdicts and all(lu is False and ru is False for lu, ru, _, _ in verdicts):
                        pair = verdicts[0]
                        findings.append(Finding(
                            "S01", "medium",
                            f"JOIN {tname} ON {_sql_of(pair[2])} = {_sql_of(pair[3])}: neither column is "
                            "unique in its table according to the schema (many-to-many join inflates "
                            "row counts and aggregates).", line, "FM1"))
    return _finalize(findings)


def _flatten_group(group) -> list:
    out = []
    stack = list(group.expressions or [])
    for key in ("rollup", "cube", "grouping_sets"):
        val = group.args.get(key)
        if isinstance(val, list):
            stack.extend(val)
    wrappers = tuple(t for t in (getattr(exp, n, None) for n in ("Rollup", "Cube", "GroupingSets")) if t)
    while stack:
        node = stack.pop()
        if isinstance(node, wrappers) or isinstance(node, exp.Tuple):
            stack.extend(node.expressions or [])
        elif isinstance(node, exp.Paren):
            stack.append(node.this)
        elif node is not None and not isinstance(node, bool):
            out.append(node)
    return out


def _strip_qualifiers(sql_text: str) -> str:
    return re.sub(r"`?\b[A-Za-z_]\w*`?\.(?=`?[A-Za-z_])", "", sql_text)


def check_sql_group_by_mismatch(sql: str, schema: dict | None = None) -> list[Finding]:
    """Rule S02: GROUP BY with fewer dimensions than non-aggregate SELECT columns.

    Every non-aggregated SELECT expression must be covered by the GROUP BY
    (by expression, alias, ordinal or by its columns). Also flags aggregates
    mixed with bare columns when there is no GROUP BY at all."""
    findings: list[Finding] = []
    for tree in _parse_sql(sql):
        for sel in tree.find_all(exp.Select):
            group = sel.args.get("group")
            if group is not None and group.args.get("all"):
                continue  # GROUP BY ALL
            projections = sel.expressions or []
            non_agg: list[tuple[int, object, str, list]] = []
            has_agg = False
            for idx, proj in enumerate(projections, 1):
                alias = proj.alias if isinstance(proj, exp.Alias) else ""
                e = proj.unalias()
                if isinstance(e, exp.Star) or (isinstance(e, exp.Column) and isinstance(e.this, exp.Star)):
                    continue
                nodes = [e, *_own_nodes(e)]
                if any(isinstance(n, exp.AggFunc) and not _inside(n, exp.Window, e) for n in nodes):
                    has_agg = True
                outside = [n for n in nodes if isinstance(n, exp.Column)
                           and not _inside(n, (exp.AggFunc, exp.Window), e)]
                if outside:
                    non_agg.append((idx, e, alias, outside))

            if group is None:
                if has_agg and non_agg:
                    names = ", ".join(_short(_sql_of(e), 40) for _, e, _, _ in non_agg[:5])
                    findings.append(Finding(
                        "S02", "high",
                        f"SELECT mixes aggregate functions with {len(non_agg)} non-aggregated "
                        f"expression(s) ({names}) but has no GROUP BY.", _node_line(sel), "FM3"))
                continue

            group_exprs = _flatten_group(group)
            ordinals = set()
            group_sqls, group_sqls_bare = set(), set()
            group_cols_q: set[tuple[str, str]] = set()
            group_cols_unq: set[str] = set()
            group_col_names: set[str] = set()
            for g in group_exprs:
                if isinstance(g, exp.Literal) and not g.is_string:
                    try:
                        ordinals.add(int(g.this))
                    except (TypeError, ValueError):
                        pass
                    continue
                text = _sql_of(g).lower()
                group_sqls.add(text)
                group_sqls_bare.add(_strip_qualifiers(text))
                for c in g.find_all(exp.Column):
                    name = c.name.lower()
                    group_col_names.add(name)
                    if c.table:
                        group_cols_q.add((c.table.lower(), name))
                    else:
                        group_cols_unq.add(name)

            def col_grouped(c) -> bool:
                name = c.name.lower()
                if c.table:
                    return (c.table.lower(), name) in group_cols_q or name in group_cols_unq
                return name in group_col_names

            unmatched = []
            for idx, e, alias, outside in non_agg:
                text = _sql_of(e).lower()
                if idx in ordinals:
                    continue
                if alias and alias.lower() in group_cols_unq:
                    continue
                if text in group_sqls or _strip_qualifiers(text) in group_sqls_bare:
                    continue
                if all(col_grouped(c) for c in outside):
                    continue
                unmatched.append(e)
            if unmatched:
                names = ", ".join(_short(_sql_of(e), 40) for e in unmatched[:5])
                findings.append(Finding(
                    "S02", "high",
                    f"GROUP BY has {len(group_exprs)} expression(s) but SELECT has {len(non_agg)} "
                    f"non-aggregated expression(s); not covered by GROUP BY: {names}.",
                    _node_line(group) or _node_line(sel), "FM3"))
    return _finalize(findings)


_COARSE_PARTS = {"DAY", "WEEK", "ISOWEEK", "MONTH", "QUARTER", "YEAR", "ISOYEAR", "DATE",
                 "DAYOFWEEK", "DAYOFYEAR"}
_EXTRACT_RE = re.compile(r"^\s*([A-Za-z_]+(?:\s*\(\s*\w+\s*\))?)\s+FROM\s+(.*)$", re.S | re.I)
_TZ_SUFFIX_RE = re.compile(r"([+-]\d{2}(:?\d{2})?|Z|UTC|[A-Za-z]+/[A-Za-z_]+)\s*$")


def _part_base(part: str) -> str:
    return re.sub(r"\s*\(.*$", "", part.strip().strip("'\"")).upper()


def check_sql_missing_timezone(sql: str, schema: dict | None = None) -> list[Finding]:
    """Rule S03: Date/time functions without explicit timezone specification.

    BigQuery evaluates TIMESTAMP -> DATE conversions, truncations and EXTRACTs
    in UTC unless a time zone is passed, which shifts day/week/month
    boundaries for any business that does not report in UTC."""
    findings: list[Finding] = []
    text = _strip_code_fences(sql)
    sch = _Schema(schema)
    names = ["TIMESTAMP_TRUNC", "DATE_TRUNC", "DATETIME", "DATE", "TIME", "EXTRACT",
             "FORMAT_TIMESTAMP", "CURRENT_DATETIME", "CURRENT_DATE", "CURRENT_TIME",
             "TIMESTAMP", "PARSE_TIMESTAMP", "CAST", "SAFE_CAST"]
    for call in _iter_sql_calls(text, names):
        name, args, line = call.name, call.args, call.line
        nargs = len(args)

        if name == "TIMESTAMP_TRUNC":
            if nargs == 2 and _part_base(args[1]) in _COARSE_PARTS:
                findings.append(Finding(
                    "S03", "high",
                    f"TIMESTAMP_TRUNC({_short(args[0], 40)}, {args[1]}) has no time zone argument; "
                    f"{_part_base(args[1])} boundaries are computed in UTC. Pass the reporting time zone "
                    "as the third argument.", line, "FM2"))
        elif name == "DATE_TRUNC":
            if nargs == 2 and _text_is_timestamp(args[0], sch) and _part_base(args[1]) in _COARSE_PARTS:
                findings.append(Finding(
                    "S03", "medium",
                    f"DATE_TRUNC on TIMESTAMP expression {_short(args[0], 40)} without a time zone; "
                    "the truncation boundary is evaluated in UTC.", line, "FM2"))
        elif name in {"DATE", "DATETIME", "TIME"}:
            if nargs == 1:
                kind = _text_is_timestamp(args[0], sch)
                if kind is True:
                    findings.append(Finding(
                        "S03", "high",
                        f"{name}({_short(args[0], 40)}) converts a TIMESTAMP without a time zone argument; "
                        f"the conversion uses UTC. Use {name}(ts, 'Area/City').", line, "FM2"))
                elif kind is None:
                    findings.append(Finding(
                        "S03", "medium",
                        f"{name}({_short(args[0], 40)}) has no time zone argument; if the argument is a "
                        "TIMESTAMP the conversion silently uses UTC.", line, "FM2"))
        elif name == "EXTRACT":
            if nargs != 1 or "AT TIME ZONE" in _mask_sql(args[0]).upper():
                continue
            m = _EXTRACT_RE.match(args[0])
            if not m:
                continue
            part, operand = _part_base(m.group(1)), m.group(2)
            if part not in _COARSE_PARTS | {"HOUR"}:
                continue
            kind = _text_is_timestamp(operand, sch)
            if kind is True:
                findings.append(Finding(
                    "S03", "high",
                    f"EXTRACT({part} FROM {_short(operand, 40)}) on a TIMESTAMP without AT TIME ZONE; "
                    f"the {part} is taken in UTC.", line, "FM2"))
            elif kind is None and part == "DATE":
                findings.append(Finding(
                    "S03", "medium",
                    f"EXTRACT(DATE FROM {_short(operand, 40)}) without AT TIME ZONE; the date is taken "
                    "in UTC.", line, "FM2"))
        elif name == "FORMAT_TIMESTAMP":
            if nargs == 2:
                findings.append(Finding(
                    "S03", "medium",
                    f"FORMAT_TIMESTAMP({_short(', '.join(args), 50)}) has no time zone argument; "
                    "the timestamp is formatted in UTC.", line, "FM2"))
        elif name in {"CURRENT_DATE", "CURRENT_DATETIME", "CURRENT_TIME"}:
            if nargs == 0:
                findings.append(Finding(
                    "S03", "low",
                    f"{name}() without a time zone returns the current value in UTC, which differs from "
                    "the local business date for part of every day.", line, "FM2"))
        elif name == "TIMESTAMP":
            if nargs == 1:
                lit = _STRING_LITERAL_RE.match(args[0])
                if lit and not _TZ_SUFFIX_RE.search(lit.group(2)):
                    findings.append(Finding(
                        "S03", "low",
                        f"TIMESTAMP({_short(args[0], 40)}) parses a literal without a UTC offset or time "
                        "zone argument; it is interpreted as UTC.", line, "FM2"))
        elif name == "PARSE_TIMESTAMP":
            if nargs == 2:
                lit = _STRING_LITERAL_RE.match(args[0])
                if lit and not re.search(r"%E?[zZ]|%Ez", lit.group(2)):
                    findings.append(Finding(
                        "S03", "low",
                        f"PARSE_TIMESTAMP({_short(args[0], 30)}, ...) has neither a time zone argument nor "
                        "a zone element in the format; input is assumed to be UTC.", line, "FM2"))
        elif name in {"CAST", "SAFE_CAST"}:
            if nargs != 1:
                continue
            m = re.match(r"^(.*)\s+AS\s+(DATE|DATETIME|TIME)\s*$", args[0], re.S | re.I)
            if m and _text_is_timestamp(m.group(1), sch) is True:
                findings.append(Finding(
                    "S03", "high",
                    f"{name}({_short(m.group(1), 40)} AS {m.group(2).upper()}) converts a TIMESTAMP "
                    "using UTC; use DATE(ts, 'Area/City') to make the time zone explicit.", line, "FM2"))

    masked = _mask_sql(text)
    for m in re.finditer(r"(?<![\w.`])CURRENT_(DATE|DATETIME|TIME)\b(?!\s*\()", masked, re.I):
        findings.append(Finding(
            "S03", "low",
            f"CURRENT_{m.group(1).upper()} without a time zone returns the current value in UTC, which "
            "differs from the local business date for part of every day.", _line_at(text, m.start()), "FM2"))
    return _finalize(findings)


_PSEUDO_PARTITION_COLS = {"_partitiontime", "_partitiondate", "_table_suffix"}


def check_sql_missing_partition_filter(sql: str, schema: dict | None = None) -> list[Finding]:
    """Rule S04: BigQuery queries without PARTITION filter on partitioned tables.

    With schema partition metadata the rule is exact (high severity). Wildcard
    tables require a _TABLE_SUFFIX filter. Without metadata the rule reports a
    low-severity finding when a table is read with no filter on any
    date/timestamp column at all."""
    findings: list[Finding] = []
    sch = _Schema(schema)
    for tree in _parse_sql(sql):
        ctes = _cte_names(tree)

        # Columns used in filtering positions anywhere in the statement.
        filter_cols: list[tuple[str, str]] = []  # (qualifier, name)
        for holder in tree.find_all(exp.Where, exp.Join, exp.Having):
            root = holder.args.get("on") if isinstance(holder, exp.Join) else holder
            if root is None:
                continue
            for c in root.find_all(exp.Column):
                filter_cols.append(((c.table or "").lower(), c.name.lower()))

        def filtered(col_names: set[str], aliases: set[str]) -> bool:
            return any(name in col_names and (qual == "" or qual in aliases)
                       for qual, name in filter_cols)

        unknown_tables = []
        seen: set[str] = set()
        for table in tree.find_all(exp.Table):
            base = _table_basename(table)
            if not base or (base in ctes and not table.args.get("db")):
                continue
            if isinstance(table.parent, (exp.Insert, exp.Create, exp.Update, exp.Delete, exp.Merge)) and \
                    table.parent.this is table:
                continue  # write target, not a scan
            if isinstance(table.parent, exp.Schema):
                continue
            alias = (table.alias_or_name or base).lower()
            aliases = {alias, base}
            key = f"{base}:{alias}"
            if key in seen:
                continue
            seen.add(key)
            line = _node_line(table)

            if base.endswith("*"):
                if not filtered({"_table_suffix"}, aliases):
                    findings.append(Finding(
                        "S04", "high",
                        f"Wildcard table {table.name} is queried without a _TABLE_SUFFIX filter; "
                        "every shard is scanned.", line, "FM4"))
                continue

            pcols = set(sch.partition_columns(base)) if sch else set()
            if pcols:
                if not filtered(pcols | _PSEUDO_PARTITION_COLS, aliases):
                    findings.append(Finding(
                        "S04", "high",
                        f"Table {base} is partitioned on {', '.join(sorted(pcols))} but the query has no "
                        "filter on the partition column (full scan; the query is rejected when "
                        "require_partition_filter is set).", line, "FM4"))
            elif sch and sch.has_table(base):
                temporal = set(sch.temporal_columns(base))
                if temporal and not filtered(temporal | _PSEUDO_PARTITION_COLS, aliases):
                    findings.append(Finding(
                        "S04", "low",
                        f"Table {base} is read without a filter on any date/timestamp column "
                        f"(candidate partition columns: {', '.join(sorted(temporal))}); if the table is "
                        "partitioned this is a full scan.", line, "FM4"))
            else:
                unknown_tables.append((base, line))

        if unknown_tables:
            has_temporal_filter = any(
                name in _PSEUDO_PARTITION_COLS or _TEMPORAL_NAME_RE.search(name) for _, name in filter_cols)
            if not has_temporal_filter:
                names = ", ".join(sorted({b for b, _ in unknown_tables})[:5])
                findings.append(Finding(
                    "S04", "low",
                    f"No partition/date filter detected for table(s) {names}; on partitioned BigQuery "
                    "tables this scans every partition (and fails if require_partition_filter is set).",
                    min((ln for _, ln in unknown_tables if ln), default=None), "FM4"))
    return _finalize(findings)


def _duplicated_aliases(sel, amap, sch: _Schema) -> dict[str, str]:
    """For one SELECT, return {alias: duplicating_alias} for relations whose
    rows are multiplied by a join, as far as the schema lets us prove it."""
    dup: dict[str, str] = {}
    present: list[str] = []
    frm = _select_from(sel)
    if frm is not None and frm.this is not None and frm.this.alias_or_name:
        present.append(frm.this.alias_or_name.lower())
    for j in sel.args.get("joins") or []:
        target = j.this
        if target is None or not target.alias_or_name:
            continue
        u = target.alias_or_name.lower()
        on = j.args.get("on")
        u_table = amap.get(u)
        if on is not None and u_table:
            for eq in on.find_all(exp.EQ):
                left, right = _unwrap(eq.this), _unwrap(eq.expression)
                if not isinstance(left, exp.Column) or not isinstance(right, exp.Column):
                    continue
                la, lt = _resolve(left, amap, sch)
                ra, rt = _resolve(right, amap, sch)
                if la == u and ra != u:
                    u_col, o_col, o_alias, o_table = left, right, ra, rt
                elif ra == u and la != u:
                    u_col, o_col, o_alias, o_table = right, left, la, lt
                else:
                    continue
                if sch.is_unique(u_table, u_col.name) is False:
                    for p in present:
                        dup.setdefault(p, u)
                if o_alias and sch.is_unique(o_table, o_col.name) is False:
                    dup.setdefault(u, o_alias)
        present.append(u)
    return dup


def _has_literal_filter(sel, alias: str, amap, sch) -> bool:
    """True if the SELECT restricts ``alias`` with a column = literal / IN predicate."""
    roots = [sel.args.get("where")] + [j.args.get("on") for j in sel.args.get("joins") or []]
    for root in roots:
        if root is None:
            continue
        for pred in [root, *_own_nodes(root)]:
            if isinstance(pred, exp.EQ):
                sides = (_unwrap(pred.this), _unwrap(pred.expression))
                for a, b in (sides, sides[::-1]):
                    if isinstance(a, exp.Column) and isinstance(b, (exp.Literal, exp.Boolean)) and \
                            _resolve(a, amap, sch)[0] == alias:
                        return True
            elif isinstance(pred, exp.In) and not pred.args.get("query"):
                col = _unwrap(pred.this)
                if isinstance(col, exp.Column) and _resolve(col, amap, sch)[0] == alias:
                    return True
    return False


def check_sql_distinct_in_aggregation(sql: str, schema: dict | None = None) -> list[Finding]:
    """Rule S05: SUM/COUNT without DISTINCT where schema implies duplicates.

    Detects COUNT(col) / SUM(expr) / AVG(expr) evaluated over rows that a join
    has multiplied (one-to-many fan-out proven from the schema), COUNT over a
    non-unique (foreign-key) column, and - without a schema - COUNT of an
    id-like column over joined rows."""
    findings: list[Finding] = []
    sch = _Schema(schema)
    for tree in _parse_sql(sql):
        ctes = _cte_names(tree)
        for sel in tree.find_all(exp.Select):
            amap = _alias_map(sel, ctes)
            joins = [j for j in (sel.args.get("joins") or [])
                     if not isinstance(j.this, (exp.Unnest, exp.Lateral))]
            dup = _duplicated_aliases(sel, amap, sch) if sch and joins else {}
            for agg in _own_nodes(sel, (exp.Count, exp.Sum, exp.Avg)):
                if isinstance(agg.parent, exp.Window):
                    continue
                arg = agg.this
                if arg is None or isinstance(arg, (exp.Distinct, exp.Star)):
                    continue
                fname = _func_name(agg) or type(agg).__name__.upper()
                line = _node_line(agg) or _node_line(sel)
                proj_alias = ""
                if isinstance(agg.parent, exp.Alias):
                    proj_alias = agg.parent.alias.lower()

                if isinstance(agg, exp.Count):
                    col = _unwrap(arg)
                    if not isinstance(col, exp.Column):
                        continue
                    alias, table = _resolve(col, amap, sch)
                    unique = sch.is_unique(table, col.name) if sch else None
                    if alias in dup:
                        by = dup[alias]
                        filtered = _has_literal_filter(sel, by, amap, sch)
                        findings.append(Finding(
                            "S05", "low" if filtered else "high",
                            f"COUNT({_sql_of(col)}) counts joined rows: {alias} rows are repeated by the "
                            f"one-to-many join with {by}"
                            + (" (a filter on that table may restore uniqueness - verify)" if filtered else "")
                            + f". Use COUNT(DISTINCT {_sql_of(col)}).", line, "FM3"))
                    elif unique is False:
                        findings.append(Finding(
                            "S05", "medium",
                            f"COUNT({_sql_of(col)}) without DISTINCT: {col.name} is not unique in "
                            f"{table} per the schema, so this counts rows rather than distinct "
                            f"{col.name} values.", line, "FM3"))
                    elif unique is None and _is_key_like(col.name):
                        if joins:
                            findings.append(Finding(
                                "S05", "medium",
                                f"COUNT({_sql_of(col)}) without DISTINCT over joined tables; if any join "
                                f"is one-to-many the same {col.name} is counted multiple times.",
                                line, "FM3"))
                        elif re.search(r"unique|distinct|uniq", proj_alias):
                            findings.append(Finding(
                                "S05", "medium",
                                f"COUNT({_sql_of(col)}) AS {proj_alias} is named as a distinct count but "
                                "has no DISTINCT.", line, "FM3"))
                        elif table and not _looks_like_own_pk(col.name, table):
                            findings.append(Finding(
                                "S05", "low",
                                f"COUNT({_sql_of(col)}) without DISTINCT: {col.name} looks like a foreign "
                                f"key in {table}; this counts rows, not distinct {col.name} values.",
                                line, "FM3"))
                else:
                    hit = None
                    for col in arg.find_all(exp.Column):
                        alias, _ = _resolve(col, amap, sch)
                        if alias in dup:
                            hit = (col, alias, dup[alias])
                            break
                    if hit:
                        col, alias, by = hit
                        filtered = _has_literal_filter(sel, by, amap, sch)
                        findings.append(Finding(
                            "S05", "low" if filtered else "high",
                            f"{fname}({_short(_sql_of(arg), 50)}) aggregates {alias} values that are "
                            f"repeated by the one-to-many join with {by}"
                            + (" (a filter on that table may restore uniqueness - verify)" if filtered else "")
                            + "; the result is inflated. De-duplicate or pre-aggregate before joining.",
                            line, "FM3"))
    return _finalize(findings)


_DATE_FUNCS = {"DATE", "DATE_TRUNC", "CURRENT_DATE", "DATE_ADD", "DATE_SUB", "PARSE_DATE",
               "LAST_DAY", "DATE_FROM_UNIX_DATE", "SAFE.DATE"}
_TS_FUNCS = {"TIMESTAMP", "CURRENT_TIMESTAMP", "TIMESTAMP_TRUNC", "TIMESTAMP_ADD", "TIMESTAMP_SUB",
             "PARSE_TIMESTAMP", "DATETIME", "CURRENT_DATETIME", "DATETIME_TRUNC", "DATETIME_ADD",
             "DATETIME_SUB", "PARSE_DATETIME", "TIMESTAMP_SECONDS", "TIMESTAMP_MILLIS",
             "TIMESTAMP_MICROS", "NOW"}
_DATE_LITERAL_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_TS_LITERAL_RE = re.compile(r"^\d{4}-\d{2}-\d{2}[ T]\d{1,2}:")


def _temporal_kind(node, amap, sch: _Schema | None) -> str | None:
    """'timestamp' | 'date' | 'date_literal' | 'timestamp_literal' | 'other' | None."""
    if node is None:
        return None
    while isinstance(node, exp.Paren):
        node = node.this
    if isinstance(node, exp.Literal):
        if not node.is_string:
            return "other"
        value = str(node.this)
        if _TS_LITERAL_RE.match(value):
            return "timestamp_literal"
        if _DATE_LITERAL_RE.match(value):
            return "date_literal"
        return "other"
    if isinstance(node, exp.Column):
        ctype = _col_type(node, amap, sch)
        if ctype:
            fam = _type_family(ctype)
            if fam in {"timestamp", "datetime"}:
                return "timestamp"
            return "date" if fam == "date" else "other"
        return "timestamp" if _TS_NAME_RE.search(node.name) else None
    text = _sql_of(node).upper()
    m = re.search(r"\bAS\s+(DATE|TIMESTAMP|DATETIME)\s*\)$", text)
    if m and text.startswith(("CAST(", "SAFE_CAST(")):
        return "date" if m.group(1) == "DATE" else "timestamp"
    m = re.match(r"^(?:TIMESTAMP|DATETIME)\s+'", text)
    if m:
        return "timestamp_literal"
    if re.match(r"^DATE\s+'", text):
        return "date_literal"
    m = re.match(r"^((?:SAFE\.)?[A-Z_]+)\s*\(", text)
    fname = m.group(1) if m else text
    if fname in _TS_FUNCS:
        return "timestamp"
    if fname in _DATE_FUNCS:
        return "date"
    return None


def _between_fallback(sql: str) -> list[Finding]:
    findings = []
    text = _strip_code_fences(sql)
    masked = _mask_sql(text)
    pattern = re.compile(r"([`\w.]+|\))\s+(?:NOT\s+)?BETWEEN\s+(.+?)\s+AND\s+"
                         r"((?:[^\s();,]+(?:\([^()]*\))?)+)", re.I | re.S)
    for m in pattern.finditer(masked):
        operand = m.group(1)
        low, high = text[m.start(2):m.end(2)], text[m.start(3):m.end(3)]
        bounds = f"{low} {high}".upper()
        name = operand.replace("`", "").split(".")[-1]
        ts_bound = bool(re.search(r"TIMESTAMP|DATETIME|\d{4}-\d{2}-\d{2}[ T]\d{1,2}:", bounds))
        date_bound = bool(re.search(r"\d{4}-\d{2}-\d{2}|DATE", bounds))
        if _TS_NAME_RE.search(name) or ts_bound:
            sev = "high"
        elif date_bound and _TEMPORAL_NAME_RE.search(name):
            sev = "medium"
        else:
            continue
        findings.append(Finding(
            "S06", sev,
            f"BETWEEN on temporal expression {operand} ({_short(low, 30)} .. {_short(high, 30)}): the "
            "inclusive upper bound mishandles TIMESTAMP values. Use >= start AND < next_period_start.",
            _line_at(text, m.start()), "FM2"))
    return _finalize(findings)


def check_sql_between_timestamps(sql: str, schema: dict | None = None) -> list[Finding]:
    """Rule S06: BETWEEN used for timestamp ranges.

    BETWEEN is inclusive on both ends. With a date-only upper bound a
    TIMESTAMP column loses everything after midnight of the last day; with a
    timestamp upper bound adjacent windows double-count the boundary instant.
    The half-open pattern ``>= start AND < end`` avoids both."""
    trees = _parse_sql(sql)
    if not trees:
        return _between_fallback(sql)
    findings: list[Finding] = []
    sch = _Schema(schema)
    for tree in trees:
        ctes = _cte_names(tree)
        scope_maps: dict[int, dict] = {}
        for between in tree.find_all(exp.Between):
            sel = between.find_ancestor(exp.Select)
            if sel is not None and id(sel) not in scope_maps:
                scope_maps[id(sel)] = _alias_map(sel, ctes)
            amap = scope_maps.get(id(sel), {}) if sel is not None else {}
            operand = between.this
            low, high = between.args.get("low"), between.args.get("high")
            kind = _temporal_kind(operand, amap, sch)
            lk, hk = _temporal_kind(low, amap, sch), _temporal_kind(high, amap, sch)
            if kind in {"date", "other", "date_literal"}:
                continue
            op_text = _short(_sql_of(operand), 40)
            line = _node_line(between)
            rng = f"{_short(_sql_of(low), 30)} AND {_short(_sql_of(high), 30)}"
            if kind == "timestamp":
                if hk in {"date_literal", "date"}:
                    msg = (f"{op_text} is a TIMESTAMP but BETWEEN {rng} uses a date-only upper bound: rows "
                           "after 00:00:00 on the last day are silently excluded.")
                else:
                    msg = (f"{op_text} BETWEEN {rng} is inclusive on both ends: rows exactly on the upper "
                           "boundary are counted in two adjacent windows and sub-second precision is lost.")
                findings.append(Finding(
                    "S06", "high", msg + " Use >= start AND < next_period_start.", line, "FM2"))
            elif kind is None:
                bounds = {lk, hk}
                if bounds & {"timestamp", "timestamp_literal"}:
                    findings.append(Finding(
                        "S06", "high",
                        f"{op_text} BETWEEN {rng} compares against timestamp bounds; the inclusive upper "
                        "bound double-counts or drops boundary rows. Use >= start AND < end.", line, "FM2"))
                elif bounds <= {"date_literal", "date"} and isinstance(_unwrap(operand), exp.Column) and \
                        _TEMPORAL_NAME_RE.search(_unwrap(operand).name):
                    findings.append(Finding(
                        "S06", "medium",
                        f"{op_text} BETWEEN {rng}: if {op_text} is a TIMESTAMP/DATETIME, rows after "
                        "midnight on the last day are silently excluded. Use >= start AND < "
                        "next_period_start.", line, "FM2"))
    return _finalize(findings)


_NUMERIC_COL_NAME_RE = re.compile(
    r"(^id$|_id$|amount|count|qty|quantity|price|total|revenue|cost|(^|_)(num|number|age|year|score|"
    r"rank|size|duration|seconds|minutes|hours|days)($|_))", re.I)
_STRING_COL_NAME_RE = re.compile(
    r"(^name$|_name$|status|email|^code$|_code$|(^|_)type$|category|zip|postal|phone|_str$|"
    r"description|title|country|currency|^sku$|_sku$|label|city|state$)", re.I)
_NUMERIC_STRING_RE = re.compile(r"^\s*-?\d+(\.\d+)?\s*$")


def _operand_type(node, amap, sch) -> tuple[str | None, str]:
    """Return (family, kind) where kind is 'col' | 'strlit' | 'numlit' | 'cast' | 'other'."""
    while isinstance(node, exp.Paren):
        node = node.this
    if isinstance(node, exp.Literal):
        return ("string", "strlit") if node.is_string else ("number", "numlit")
    if isinstance(node, exp.Neg) and isinstance(node.this, exp.Literal) and not node.this.is_string:
        return "number", "numlit"
    if isinstance(node, exp.Boolean):
        return "bool", "other"
    if isinstance(node, exp.Cast):
        to = node.args.get("to")
        return _type_family(_sql_of(to)) if to is not None else None, "cast"
    if isinstance(node, exp.Column):
        return _type_family(_col_type(node, amap, sch)), "col"
    return None, "other"


def check_sql_implicit_type_coercion(sql: str, schema: dict | None = None) -> list[Finding]:
    """Rule S07: Implicit type coercion in WHERE/JOIN comparisons.

    BigQuery does not coerce STRING <-> INT64 (the query fails), while most
    engines LLMs learned from coerce silently and compare differently
    ('10' < '9'). Flags comparisons between incompatible column types (schema)
    and column/literal mismatches (schema or naming heuristics)."""
    if not SQLGLOT_AVAILABLE:
        return []
    findings: list[Finding] = []
    sch = _Schema(schema)
    cmp_types = (exp.EQ, exp.NEQ, exp.GT, exp.GTE, exp.LT, exp.LTE)
    for tree in _parse_sql(sql):
        ctes = _cte_names(tree)
        for sel in tree.find_all(exp.Select):
            amap = _alias_map(sel, ctes)
            for node in _own_nodes(sel, (*cmp_types, exp.In)):
                if isinstance(node, exp.In):
                    if node.args.get("query") is not None:
                        continue
                    pairs = [(node.this, e) for e in (node.expressions or [])[:1]]
                else:
                    pairs = [(node.this, node.expression)]
                in_join = node.find_ancestor(exp.Join) is not None and \
                    not _inside(node, exp.Where, sel)
                where = "JOIN condition" if in_join else "predicate"
                for left, right in pairs:
                    lf, lk = _operand_type(left, amap, sch)
                    rf, rk = _operand_type(right, amap, sch)
                    if lk != "col" and rk == "col":
                        left, right, lf, rf, lk, rk = right, left, rf, lf, rk, lk
                    if lk not in {"col", "cast"}:
                        continue
                    ltxt, rtxt = _short(_sql_of(left), 40), _short(_sql_of(right), 40)
                    line = _node_line(node)
                    lname = left.name if isinstance(left, exp.Column) else ""

                    if lf and rf and rk in {"col", "cast"}:
                        if lf != rf:
                            findings.append(Finding(
                                "S07", "high",
                                f"Type mismatch in {where}: {ltxt} ({lf.upper()}) is compared with {rtxt} "
                                f"({rf.upper()}) without an explicit CAST; BigQuery rejects or mis-compares "
                                "mixed types.", line, "FM4"))
                        continue
                    if lf and rk == "strlit":
                        value = str(right.this) if isinstance(right, exp.Literal) else ""
                        if lf == "number":
                            findings.append(Finding(
                                "S07", "high",
                                f"Numeric column {ltxt} is compared with string literal '{_short(value, 20)}' "
                                f"in {where}; BigQuery does not coerce STRING to a number. Use a numeric "
                                "literal or CAST.", line, "FM4"))
                        elif lf == "bool":
                            findings.append(Finding(
                                "S07", "medium",
                                f"BOOL column {ltxt} is compared with string literal '{_short(value, 20)}'; "
                                "use TRUE/FALSE.", line, "FM4"))
                        continue
                    if lf and rk == "numlit":
                        if lf in {"string", "date", "timestamp", "datetime", "bool"}:
                            findings.append(Finding(
                                "S07", "high",
                                f"{lf.upper()} column {ltxt} is compared with numeric literal {rtxt} in "
                                f"{where}; quote the literal or CAST the column explicitly.", line, "FM4"))
                        continue
                    if lf is None and lk == "col" and lname:
                        # No schema knowledge: fall back to naming conventions.
                        if rk == "strlit" and isinstance(right, exp.Literal) and \
                                _NUMERIC_STRING_RE.match(str(right.this)) and \
                                _NUMERIC_COL_NAME_RE.search(lname) and not _STRING_COL_NAME_RE.search(lname):
                            findings.append(Finding(
                                "S07", "medium",
                                f"{ltxt} looks numeric but is compared with the quoted number "
                                f"'{right.this}' in {where}; this relies on implicit STRING/number "
                                "coercion.", line, "FM4"))
                        elif rk == "numlit" and _STRING_COL_NAME_RE.search(lname) and \
                                not _NUMERIC_COL_NAME_RE.search(lname):
                            findings.append(Finding(
                                "S07", "medium",
                                f"{ltxt} looks like a STRING column but is compared with numeric literal "
                                f"{rtxt} in {where}; this relies on implicit coercion (and drops leading "
                                "zeros).", line, "FM4"))
    return _finalize(findings)


def check_sql_select_star(sql: str, schema: dict | None = None) -> list[Finding]:
    """Rule S08: SELECT * in production queries.

    The output schema silently changes when upstream tables gain, lose or
    reorder columns, and BigQuery bills for every column scanned."""
    trees = _parse_sql(sql)
    findings: list[Finding] = []
    if not trees:
        text = _strip_code_fences(sql)
        masked = _mask_sql(text)
        for m in re.finditer(r"\bSELECT\s+(?:DISTINCT\s+|ALL\s+)?(?:[`\w]+\.)?\*", masked, re.I):
            if re.search(r"EXISTS\s*\(\s*$", masked[:m.start()], re.I):
                continue
            findings.append(Finding(
                "S08", "medium",
                "SELECT * makes the output schema depend on upstream table definitions; list the "
                "required columns explicitly.", _line_at(text, m.start()), "FM5"))
        return _finalize(findings)

    for tree in trees:
        ctes = _cte_names(tree)
        for sel in tree.find_all(exp.Select):
            if isinstance(sel.parent, exp.Exists):
                continue  # EXISTS (SELECT * ...) is harmless
            stars = []
            for proj in sel.expressions or []:
                e = proj.unalias()
                if isinstance(e, exp.Star):
                    stars.append((e, None))
                elif isinstance(e, exp.Column) and isinstance(e.this, exp.Star):
                    stars.append((e, (e.table or "").lower()))
            if not stars:
                continue
            amap = _alias_map(sel, ctes)
            sources = _sources(sel)
            for star, qual in stars:
                if qual:
                    base_table = amap.get(qual) is not None or qual not in amap
                    label = f"{qual}.*"
                else:
                    base_table = any(v is not None for v in amap.values()) or not sources
                    label = "*"
                has_except = bool(star.args.get("except") or star.args.get("except_")
                                  or star.args.get("replace"))
                if base_table:
                    sev = "medium"
                    detail = ("reads every column of a base table: the result schema changes silently "
                              "when the table evolves and all columns are billed")
                else:
                    sev = "low"
                    detail = "propagates whatever columns the upstream CTE/subquery exposes"
                if has_except:
                    detail += " (EXCEPT/REPLACE narrows it but new columns still flow through)"
                findings.append(Finding(
                    "S08", sev, f"SELECT {label} {detail}. List the required columns explicitly.",
                    _node_line(star) or _node_line(sel) or _find_line(sql, r"\bSELECT\b"), "FM5"))
    return _finalize(findings)


_NULL_SAFE_FUNCS = {"IFNULL", "NVL", "COALESCE", "ZEROIFNULL", "NVL2"}


def _null_protected(col, sel, not_null_names: set[str]) -> bool:
    if col.name.lower() in not_null_names:
        return True
    cur = col.parent
    while cur is not None and cur is not sel:
        if isinstance(cur, exp.Coalesce) or _func_name(cur) in _NULL_SAFE_FUNCS:
            return True
        if isinstance(cur, (exp.Case, exp.If)):
            text = _sql_of(cur).upper()
            if " IS NULL" in text or "IS NOT NULL" in text:
                return True
        cur = cur.parent
    return False


def check_sql_missing_null_handling(sql: str, schema: dict | None = None) -> list[Finding]:
    """Rule S09: Missing NULL handling on nullable columns in calculations.

    A column is treated as nullable when the schema says so or when it comes
    from the optional side of an outer join. Flags unguarded use in arithmetic
    / concatenation (result becomes NULL), in <> / NOT IN filters (NULL rows
    vanish), and NOT IN (subquery) whose column may be NULL (returns no rows)."""
    if not SQLGLOT_AVAILABLE:
        return []
    findings: list[Finding] = []
    sch = _Schema(schema)
    arith = tuple(t for t in (getattr(exp, n, None) for n in
                              ("Add", "Sub", "Mul", "Div", "Mod", "DPipe", "Concat")) if t)
    for tree in _parse_sql(sql):
        ctes = _cte_names(tree)
        for sel in tree.find_all(exp.Select):
            amap = _alias_map(sel, ctes)
            nullable_aliases: set[str] = set()
            seen_aliases: list[str] = []
            frm = _select_from(sel)
            if frm is not None and frm.this is not None and frm.this.alias_or_name:
                seen_aliases.append(frm.this.alias_or_name.lower())
            for j in sel.args.get("joins") or []:
                if j.this is None or not j.this.alias_or_name:
                    continue
                side = str(j.args.get("side") or "").upper()
                alias = j.this.alias_or_name.lower()
                if side == "LEFT":
                    nullable_aliases.add(alias)
                elif side == "RIGHT":
                    nullable_aliases.update(seen_aliases)
                elif side == "FULL":
                    nullable_aliases.update(seen_aliases)
                    nullable_aliases.add(alias)
                seen_aliases.append(alias)

            # columns explicitly guarded with IS NOT NULL in this scope
            not_null: set[str] = set()
            roots = [sel.args.get("where")] + [j.args.get("on") for j in sel.args.get("joins") or []]
            for root in roots:
                if root is None:
                    continue
                for is_node in [root, *_own_nodes(root)]:
                    if isinstance(is_node, exp.Is) and isinstance(is_node.expression, exp.Null) and \
                            isinstance(is_node.parent, exp.Not) and isinstance(is_node.this, exp.Column):
                        not_null.add(is_node.this.name.lower())

            def nullable_reason(col) -> str | None:
                alias, table = _resolve(col, amap, sch)
                if alias and alias in nullable_aliases:
                    return f"comes from the optional side of an outer join ({alias})"
                if sch and table and sch.is_nullable(table, col.name):
                    return "is nullable per the schema"
                return None

            for node in _own_nodes(sel, arith):
                operands = node.expressions if (hasattr(exp, "Concat") and isinstance(node, exp.Concat)) \
                    else [node.this, node.args.get("expression")]
                for operand in operands:
                    col = _unwrap(operand) if operand is not None else None
                    if not isinstance(col, exp.Column):
                        continue
                    reason = nullable_reason(col)
                    if not reason or _null_protected(col, sel, not_null):
                        continue
                    op = "concatenation" if type(node).__name__ in {"DPipe", "Concat"} else "arithmetic"
                    findings.append(Finding(
                        "S09", "medium",
                        f"{_sql_of(col)} {reason} and is used in {op} "
                        f"({_short(_sql_of(node), 50)}) without COALESCE/IFNULL; a NULL makes the whole "
                        "expression NULL and the row silently drops out of SUM/AVG.",
                        _node_line(col) or _node_line(node), "FM5"))

            where = sel.args.get("where")
            if where is not None:
                for node in [where, *_own_nodes(where)]:
                    if isinstance(node, exp.NEQ):
                        for side in (node.this, node.expression):
                            col = _unwrap(side)
                            if isinstance(col, exp.Column):
                                reason = nullable_reason(col)
                                if reason and not _null_protected(col, sel, not_null):
                                    findings.append(Finding(
                                        "S09", "medium",
                                        f"{_sql_of(col)} {reason}; the filter {_short(_sql_of(node), 40)} "
                                        "evaluates to NULL for NULL values and silently excludes those "
                                        "rows. Add OR ... IS NULL or use IFNULL.",
                                        _node_line(node), "FM5"))
                    elif isinstance(node, exp.Not) and isinstance(node.this, exp.In):
                        in_node = node.this
                        query = in_node.args.get("query")
                        if query is None:
                            col = _unwrap(in_node.this)
                            if isinstance(col, exp.Column):
                                reason = nullable_reason(col)
                                if reason and not _null_protected(col, sel, not_null):
                                    findings.append(Finding(
                                        "S09", "medium",
                                        f"{_sql_of(col)} {reason}; NOT IN (...) silently excludes rows "
                                        "where it is NULL.", _node_line(node), "FM5"))
                            continue
                        inner = query.this if isinstance(query, exp.Subquery) else query
                        if not isinstance(inner, exp.Select) or len(inner.expressions or []) != 1:
                            continue
                        proj = _unwrap(inner.expressions[0].unalias())
                        if not isinstance(proj, exp.Column):
                            continue
                        inner_map = _alias_map(inner, ctes)
                        _, itable = _resolve(proj, inner_map, sch)
                        if sch and sch.is_nullable(itable, proj.name) is False:
                            continue
                        guarded = False
                        iwhere = inner.args.get("where")
                        if iwhere is not None:
                            for is_node in _own_nodes(iwhere, exp.Is):
                                if isinstance(is_node.expression, exp.Null) and isinstance(is_node.parent, exp.Not) \
                                        and isinstance(is_node.this, exp.Column) \
                                        and is_node.this.name.lower() == proj.name.lower():
                                    guarded = True
                        if not guarded:
                            findings.append(Finding(
                                "S09", "medium",
                                f"NOT IN (SELECT {_sql_of(proj)} ...): if the subquery returns a single NULL "
                                "the predicate is never true and the outer query returns no rows. Filter "
                                f"{proj.name} IS NOT NULL or use NOT EXISTS.", _node_line(node), "FM5"))
    return _finalize(findings)


_GRANULARITY_WORDS = {
    "day": "DAY", "daily": "DAY",
    "week": "WEEK", "weekly": "WEEK", "wk": "WEEK",
    "month": "MONTH", "monthly": "MONTH", "mth": "MONTH",
    "quarter": "QUARTER", "quarterly": "QUARTER", "qtr": "QUARTER",
    "year": "YEAR", "yearly": "YEAR", "annual": "YEAR", "yr": "YEAR",
    "hour": "HOUR", "hourly": "HOUR",
}
_PART_FAMILY = {"ISOWEEK": "WEEK", "ISOYEAR": "YEAR", "DAYOFWEEK": "DAY", "DAYOFYEAR": "DAY", "DATE": "DAY"}
_TRUNC_PARTS = {"MICROSECOND", "MILLISECOND", "SECOND", "MINUTE", "HOUR", "DAY", "WEEK", "ISOWEEK",
                "MONTH", "QUARTER", "YEAR", "ISOYEAR"}


def check_sql_date_trunc_granularity(sql: str, schema: dict | None = None) -> list[Finding]:
    """Rule S10: Wrong date truncation granularity (MONTH vs WEEK boundaries).

    Flags: truncation part that contradicts the column alias; WEEK without an
    explicit week start (BigQuery weeks start on Sunday); WEEK and
    MONTH/QUARTER/YEAR buckets mixed in one statement (weeks straddle month
    boundaries); EXTRACT(WEEK/ISOWEEK/MONTH) without the matching year; and
    PostgreSQL-style DATE_TRUNC('month', x) argument order."""
    findings: list[Finding] = []
    text = _strip_code_fences(sql)
    masked = _mask_sql(text)
    trunc_parts: list[tuple[str, int]] = []      # (family, line) of *_TRUNC calls
    extract_parts: list[tuple[str, int]] = []    # (raw part, line) of EXTRACT calls

    for call in _iter_sql_calls(text, ["DATE_TRUNC", "TIMESTAMP_TRUNC", "DATETIME_TRUNC", "EXTRACT"]):
        raw_part = None
        if call.name == "EXTRACT":
            if len(call.args) != 1:
                continue
            m = _EXTRACT_RE.match(call.args[0])
            if not m:
                continue
            raw_part = m.group(1).strip().upper()
            extract_parts.append((_part_base(raw_part), call.line))
        else:
            if len(call.args) < 2:
                continue
            first = _STRING_LITERAL_RE.match(call.args[0])
            if first and _part_base(first.group(2)) in _TRUNC_PARTS:
                findings.append(Finding(
                    "S10", "high",
                    f"{call.name}({call.args[0]}, ...) uses PostgreSQL argument order; BigQuery expects "
                    f"{call.name}(expression, {_part_base(first.group(2))}).", call.line, "FM4"))
                raw_part = first.group(2).strip().upper()
            else:
                raw_part = call.args[1].strip().upper()
            trunc_parts.append((_PART_FAMILY.get(_part_base(raw_part), _part_base(raw_part)), call.line))

        base = _part_base(raw_part)
        family = _PART_FAMILY.get(base, base)

        if base == "WEEK" and "(" not in raw_part:
            findings.append(Finding(
                "S10", "medium",
                f"{call.name} with WEEK uses BigQuery's default Sunday week start; business/ISO weeks start "
                "on Monday, so weekly buckets are shifted by one day. Use WEEK(MONDAY) or ISOWEEK.",
                call.line, "FM2"))

        alias_match = re.match(r"\s*AS\s+`?([A-Za-z_]\w*)`?", masked[call.end:], re.I)
        if alias_match and family in set(_GRANULARITY_WORDS.values()):
            tokens = [t for t in re.split(r"[_\W]+", alias_match.group(1).lower()) if t]
            implied = {_GRANULARITY_WORDS[t] for t in tokens if t in _GRANULARITY_WORDS}
            if implied and family not in implied:
                findings.append(Finding(
                    "S10", "high",
                    f"{call.name}(... {base} ...) is aliased as '{alias_match.group(1)}', which implies "
                    f"{'/'.join(sorted(implied))} granularity; the truncation unit does not match the "
                    "column's meaning.", call.line, "FM2"))

    trunc_families = {f for f, _ in trunc_parts}
    if "WEEK" in trunc_families and trunc_families & {"MONTH", "QUARTER", "YEAR"}:
        coarse = sorted(trunc_families & {"MONTH", "QUARTER", "YEAR"})
        line = min(ln for f, ln in trunc_parts if f == "WEEK")
        findings.append(Finding(
            "S10", "medium",
            f"Statement mixes WEEK and {'/'.join(coarse)} truncation: weeks straddle "
            f"{'/'.join(c.lower() for c in coarse)} boundaries, so weekly buckets cannot be rolled up or "
            "compared to those periods without splitting boundary weeks.", line, "FM2"))

    extracted = {p for p, _ in extract_parts}
    has_year_context = bool(extracted & {"YEAR", "ISOYEAR"}) or bool(trunc_parts) or \
        bool(re.search(r"FORMAT_(DATE|TIMESTAMP|DATETIME)\s*\(", masked, re.I))
    for part, line in extract_parts:
        if part == "ISOWEEK" and "ISOYEAR" not in extracted:
            extra = " (YEAR is not the ISO year: late-December/early-January days land in the wrong year)" \
                if "YEAR" in extracted else ""
            findings.append(Finding(
                "S10", "medium",
                f"EXTRACT(ISOWEEK ...) is not paired with EXTRACT(ISOYEAR ...){extra}; week numbers collide "
                "or split across year boundaries.", line, "FM2"))
        elif part == "WEEK" and not extracted & {"YEAR", "ISOYEAR"}:
            findings.append(Finding(
                "S10", "medium",
                "EXTRACT(WEEK ...) without the year: week numbers repeat every year and week 0/53 split "
                "the days around New Year.", line, "FM2"))
        elif part in {"MONTH", "QUARTER", "DAYOFYEAR"} and not has_year_context and \
                re.search(r"\bGROUP\s+BY\b", masked, re.I):
            findings.append(Finding(
                "S10", "medium",
                f"EXTRACT({part} ...) is used for grouping without the year; the same {part.lower()} of "
                f"different years is merged into one bucket. Use DATE_TRUNC(..., {part if part != 'DAYOFYEAR' else 'DAY'}).",
                line, "FM2"))
    return _finalize(findings)


def check_sql_scalar_subquery_multiple_rows(sql: str, schema: dict | None = None) -> list[Finding]:
    """Rule S11: Subquery that may return multiple rows in scalar context.

    A subquery used as a value (in the SELECT list, in a comparison or in
    arithmetic) must return at most one row. It is accepted when it is a pure
    aggregate without GROUP BY, has LIMIT 1, has no FROM, or filters on a
    unique key; everything else fails at run time as soon as data grows."""
    if not SQLGLOT_AVAILABLE:
        return []
    findings: list[Finding] = []
    sch = _Schema(schema)
    scalar_parents = (exp.EQ, exp.NEQ, exp.GT, exp.GTE, exp.LT, exp.LTE,
                      exp.Add, exp.Sub, exp.Mul, exp.Div, exp.Between)
    for tree in _parse_sql(sql):
        ctes = _cte_names(tree)
        for sq in tree.find_all(exp.Subquery):
            parent = sq.parent
            child = sq
            while isinstance(parent, exp.Paren):
                child, parent = parent, parent.parent
            if isinstance(parent, exp.Alias) and isinstance(parent.parent, exp.Select):
                child, parent = parent, parent.parent
            if isinstance(parent, exp.Select):
                scalar = any(p is child for p in parent.expressions or [])
                context = "the SELECT list"
            else:
                scalar = isinstance(parent, scalar_parents)
                context = "a comparison/expression"
            if not scalar:
                continue
            inner = sq.this
            while isinstance(inner, (exp.Subquery, exp.Paren)):
                inner = inner.this
            line = _node_line(sq)
            if not isinstance(inner, exp.Select):
                findings.append(Finding(
                    "S11", "medium",
                    f"Set operation used as a scalar subquery in {context}; it can return more than one "
                    "row and fail with 'Scalar subquery produced more than one element'.", line, "FM1"))
                continue
            single, evidence = _single_row_select(inner, sch, ctes)
            if single:
                continue
            group = inner.args.get("group")
            where = inner.args.get("where")
            has_key_filter = False
            if where is not None:
                for eq in _own_nodes(where, exp.EQ):
                    if any(isinstance(_unwrap(s), exp.Column) and _is_key_like(_unwrap(s).name)
                           for s in (eq.this, eq.expression)):
                        has_key_filter = True
                        break
            if group is not None:
                reason = "it has a GROUP BY and returns one row per group"
                sev = "high"
            elif has_key_filter:
                reason = "its key filter is not proven unique (a foreign-key lookup can match several rows)"
                sev = "medium"
            elif where is None:
                reason = "it has no WHERE, aggregate or LIMIT 1"
                sev = "high"
            else:
                reason = "nothing restricts it to a single row (no aggregate, LIMIT 1 or unique-key filter)"
                sev = "high"
            findings.append(Finding(
                "S11", sev,
                f"Scalar subquery in {context} may return multiple rows: {reason} "
                f"[{_short(_sql_of(inner), 60)}]. BigQuery fails at run time with 'Scalar subquery produced "
                "more than one element'.", line, "FM1"))
    return _finalize(findings)


_ORDER_SENSITIVE_WINDOW_FUNCS = {
    "ROW_NUMBER", "RANK", "DENSE_RANK", "NTILE", "PERCENT_RANK", "CUME_DIST",
    "LAG", "LEAD", "FIRST_VALUE", "LAST_VALUE", "NTH_VALUE",
}


def _window_order_fallback(sql: str) -> list[Finding]:
    findings = []
    text = _strip_code_fences(sql)
    masked = _mask_sql(text)
    for call in _iter_sql_calls(text, _ORDER_SENSITIVE_WINDOW_FUNCS):
        m = re.match(r"\s*(?:(?:IGNORE|RESPECT)\s+NULLS\s*)?OVER\s*\(", masked[call.end:], re.I)
        if not m:
            continue
        start = call.end + m.end() - 1
        depth, close = 0, None
        for k in range(start, len(masked)):
            if masked[k] == "(":
                depth += 1
            elif masked[k] == ")":
                depth -= 1
                if depth == 0:
                    close = k
                    break
        if close is None:
            continue
        body = masked[start + 1:close]
        if re.search(r"\bORDER\s+BY\b", body, re.I):
            continue
        if re.match(r"\s*[A-Za-z_]\w*\s*$", body):
            continue  # named window; cannot resolve lexically
        findings.append(Finding(
            "S12", "high",
            f"{call.name}() OVER ({_short(text[start + 1:close], 40)}) has no ORDER BY; the result is "
            "non-deterministic.", call.line, "FM3"))
    return _finalize(findings)


def check_sql_window_missing_order_by(sql: str, schema: dict | None = None) -> list[Finding]:
    """Rule S12: Order-sensitive window functions without ORDER BY.

    ROW_NUMBER / RANK / DENSE_RANK / LAG / LEAD / FIRST_VALUE / ... depend on
    row order. Without ORDER BY in the window the engine picks an arbitrary
    order, so de-duplication and 'latest row' logic return different rows on
    every run."""
    trees = _parse_sql(sql)
    if not trees:
        return _window_order_fallback(sql)
    findings: list[Finding] = []
    for tree in trees:
        named: dict[str, bool] = {}
        for sel in tree.find_all(exp.Select):
            for wdef in sel.args.get("windows") or []:
                name = (wdef.this.name if isinstance(wdef.this, exp.Identifier) else wdef.name) or ""
                named[name.lower()] = bool(wdef.args.get("order"))
        for win in tree.find_all(exp.Window):
            func = win.this
            if func is None or isinstance(func, exp.Identifier):
                continue  # named window definition
            while type(func).__name__ in {"IgnoreNulls", "RespectNulls"}:
                func = func.this
            fname = _func_name(func)
            if fname not in _ORDER_SENSITIVE_WINDOW_FUNCS:
                continue
            has_order = bool(win.args.get("order"))
            ref = win.args.get("alias")
            if not has_order and ref is not None:
                ref_name = (getattr(ref, "name", None) or str(ref)).lower()
                has_order = named.get(ref_name, False)
            if has_order:
                continue
            partition = win.args.get("partition_by") or []
            part_txt = ", ".join(_sql_of(p) for p in partition) or "<none>"
            findings.append(Finding(
                "S12", "high",
                f"{fname}() window (PARTITION BY {_short(part_txt, 40)}) has no ORDER BY; row order within "
                "the partition is arbitrary, so the result is non-deterministic across runs.",
                _node_line(win) or _find_line(sql, rf"\b{fname}\b"), "FM3"))
    return _finalize(findings)


# ---------------------------------------------------------------------------
# Python AST helpers (Airflow + ETL rules)
# ---------------------------------------------------------------------------

@lru_cache(maxsize=256)
def _parse_python(code: str):
    """Parse Python source; returns None when it is not valid Python."""
    if not code or not code.strip():
        return None
    text = _strip_code_fences(code)
    try:
        return ast.parse(text)
    except (SyntaxError, ValueError, RecursionError):
        return None


def _dotted(node) -> str:
    """Dotted name of a Name/Attribute chain ('' for anything else)."""
    parts = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if isinstance(node, ast.Name):
        parts.append(node.id)
        return ".".join(reversed(parts))
    if isinstance(node, ast.Call):
        inner = _dotted(node.func)
        return ".".join([inner + "()"] + list(reversed(parts))) if inner else ""
    return ""


def _call_name(call: ast.Call) -> str:
    func = call.func
    if isinstance(func, ast.Attribute):
        return func.attr
    if isinstance(func, ast.Name):
        return func.id
    return ""


def _kw(call: ast.Call, name: str):
    for k in call.keywords:
        if k.arg == name:
            return k.value
    return None


def _has_star_kwargs(call: ast.Call) -> bool:
    return any(k.arg is None for k in call.keywords)


def _const_str(node) -> str | None:
    return node.value if isinstance(node, ast.Constant) and isinstance(node.value, str) else None


def _parent_map(tree) -> dict:
    parents = {}
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            parents[child] = node
    return parents


def _dict_items(node) -> dict[str, ast.AST]:
    """Literal items of a dict display or dict(...) call, keyed by string key."""
    out: dict[str, ast.AST] = {}
    if isinstance(node, ast.Dict):
        for k, v in zip(node.keys, node.values):
            key = _const_str(k) if k is not None else None
            if key is not None:
                out[key] = v
    elif isinstance(node, ast.Call) and _call_name(node) == "dict":
        for k in node.keywords:
            if k.arg:
                out[k.arg] = k.value
    return out


def _is_dag_decorator(dec) -> bool:
    target = dec.func if isinstance(dec, ast.Call) else dec
    return _dotted(target).split(".")[-1] == "dag"


def _task_decorator(dec) -> tuple[bool, str, list]:
    """(is_task_decorator, dotted_name, keywords)."""
    target = dec.func if isinstance(dec, ast.Call) else dec
    dotted = _dotted(target)
    parts = dotted.split(".")
    is_task = bool(dotted) and (parts[0] == "task" or "task" in parts[:-1] or parts[-1] in {
        "task", "branch_task", "short_circuit_task", "sensor_task"})
    return is_task, dotted, (dec.keywords if isinstance(dec, ast.Call) else [])


def _trigger_rule_value(node) -> str | None:
    if node is None:
        return None
    s = _const_str(node)
    if s is not None:
        return s.lower()
    if isinstance(node, ast.Attribute):
        return node.attr.lower()
    return "<dynamic>"


@dataclass
class _Task:
    var: str
    task_id: str | None
    operator: str
    lineno: int
    call: ast.Call | None
    trigger_rule: str | None
    is_branch: bool
    is_sensor: bool
    has_star_kwargs: bool = False
    multi: bool = False  # created in a loop/comprehension: stands for several tasks

    @property
    def label(self) -> str:
        return self.task_id or self.var


class _AirflowModel:
    """Tasks, DAG declarations, default_args and dependency edges of a DAG file."""

    def __init__(self, tree: ast.AST):
        self.tree = tree
        self.tasks: dict[str, _Task] = {}
        self.call_var: dict[int, str] = {}
        self.edges: set[tuple[str, str]] = set()
        self.default_args: dict[str, ast.AST] = {}
        self.dags: list[tuple[int, list, bool]] = []  # (lineno, keywords, has_star_kwargs)
        self.task_fns: dict[str, tuple[str, list, int]] = {}
        self.list_vars: dict[str, list[str]] = {}
        self._collect_decorated()
        self._collect_dags_and_default_args()
        self._collect_tasks()
        self._visit(getattr(tree, "body", []), {})

    # -- collection -------------------------------------------------------
    def _collect_decorated(self) -> None:
        for node in ast.walk(self.tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                for dec in node.decorator_list:
                    is_task, dotted, kws = _task_decorator(dec)
                    if is_task:
                        self.task_fns[node.name] = (dotted, kws, node.lineno)
                    elif _is_dag_decorator(dec):
                        kws = dec.keywords if isinstance(dec, ast.Call) else []
                        star = isinstance(dec, ast.Call) and _has_star_kwargs(dec)
                        self.dags.append((node.lineno, kws, star))
                        self._absorb_default_args(kws)

    def _absorb_default_args(self, keywords) -> None:
        for k in keywords:
            if k.arg == "default_args":
                value = k.value
                if isinstance(value, ast.Name):
                    value = self._assigned.get(value.id, value)
                self.default_args.update(_dict_items(value))

    def _collect_dags_and_default_args(self) -> None:
        self._assigned: dict[str, ast.AST] = {}
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                self._assigned[node.targets[0].id] = node.value
        for name, value in self._assigned.items():
            if name.lower() in {"default_args", "args", "dag_default_args"} or name.lower().endswith(
                    "default_args"):
                self.default_args.update(_dict_items(value))
        # re-absorb for @dag decorators now that assignments are known
        for node in ast.walk(self.tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                for dec in node.decorator_list:
                    if _is_dag_decorator(dec) and isinstance(dec, ast.Call):
                        self._absorb_default_args(dec.keywords)
            elif isinstance(node, ast.Call) and _call_name(node) == "DAG":
                self.dags.append((node.lineno, node.keywords, _has_star_kwargs(node)))
                self._absorb_default_args(node.keywords)
        self.dags.sort(key=lambda d: d[0])

    def _is_operator_call(self, call: ast.Call) -> bool:
        name = _call_name(call)
        if name == "DAG" or not name:
            return False
        if name.endswith(("Operator", "Sensor")):
            return True
        return _kw(call, "task_id") is not None

    def _taskflow_call(self, call: ast.Call) -> tuple[str, list] | None:
        """Return (fn_name, override_keywords) if call instantiates a @task function."""
        func = call.func
        if isinstance(func, ast.Name) and func.id in self.task_fns:
            return func.id, []
        if isinstance(func, ast.Call) and isinstance(func.func, ast.Attribute) and \
                func.func.attr == "override" and isinstance(func.func.value, ast.Name) and \
                func.func.value.id in self.task_fns:
            return func.func.value.id, func.keywords
        return None

    def _register(self, call: ast.Call, var: str | None) -> None:
        tf = self._taskflow_call(call)
        if tf is not None:
            fn, override_kws = tf
            dotted, dec_kws, _ = self.task_fns[fn]
            kws = {k.arg: k.value for k in dec_kws if k.arg}
            kws.update({k.arg: k.value for k in override_kws if k.arg})
            name = var or f"<{fn}@{call.lineno}>"
            low = dotted.lower()
            self.tasks[name] = _Task(name, _const_str(kws.get("task_id")) or fn, "@" + dotted, call.lineno,
                                     None, _trigger_rule_value(kws.get("trigger_rule")),
                                     "branch" in low, low.endswith("sensor"))
            self.tasks[name].multi = id(call) in self._looped_calls
            self.call_var[id(call)] = name
            return
        if not self._is_operator_call(call):
            return
        op = _call_name(call)
        task_id = _const_str(_kw(call, "task_id"))
        name = var or f"<{task_id or op}@{call.lineno}>"
        self.tasks[name] = _Task(name, task_id, op, call.lineno, call,
                                 _trigger_rule_value(_kw(call, "trigger_rule")),
                                 op.startswith("Branch"), op.endswith("Sensor"), _has_star_kwargs(call),
                                 id(call) in self._looped_calls)
        self.call_var[id(call)] = name

    def _collect_tasks(self) -> None:
        assigned_calls: dict[int, str] = {}
        self._looped_calls: set[int] = set()
        loop_types = (ast.For, ast.AsyncFor, ast.While, ast.ListComp, ast.SetComp, ast.GeneratorExp,
                      ast.DictComp)
        for node in ast.walk(self.tree):
            if isinstance(node, loop_types):
                self._looped_calls.update(id(n) for n in ast.walk(node) if isinstance(n, ast.Call))
        for node in ast.walk(self.tree):
            value, targets = None, []
            if isinstance(node, ast.Assign):
                value, targets = node.value, node.targets
            elif isinstance(node, ast.AnnAssign) and node.value is not None:
                value, targets = node.value, [node.target]
            if isinstance(value, ast.Call) and len(targets) == 1 and isinstance(targets[0], ast.Name):
                assigned_calls[id(value)] = targets[0].id
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Call):
                self._register(node, assigned_calls.get(id(node)))

    # -- dependency graph ---------------------------------------------------
    def _refs(self, node, env: dict[str, list[str]]) -> list[str]:
        if node is None:
            return []
        if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.RShift, ast.LShift)):
            left, right = self._refs(node.left, env), self._refs(node.right, env)
            for a in left:
                for b in right:
                    self.edges.add((a, b) if isinstance(node.op, ast.RShift) else (b, a))
            return right
        if isinstance(node, ast.Name):
            if node.id in env:
                return list(env[node.id])
            if node.id in self.list_vars and node.id not in self.tasks:
                return list(self.list_vars[node.id])
            return [node.id]
        if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
            out: list[str] = []
            for el in node.elts:
                out.extend(self._refs(el, env))
            return out
        if isinstance(node, ast.Starred):
            return self._refs(node.value, env)
        if isinstance(node, ast.Subscript):
            return self._refs(node.value, env)
        if isinstance(node, (ast.ListComp, ast.GeneratorExp, ast.SetComp)):
            return self._refs(node.elt, env)
        if isinstance(node, ast.Call):
            if id(node) in self.call_var:
                return [self.call_var[id(node)]]
            return self._handle_call(node, env)
        return []

    def _handle_call(self, call: ast.Call, env) -> list[str]:
        name = _call_name(call)
        if name in {"set_downstream", "set_upstream"} and isinstance(call.func, ast.Attribute):
            base = self._refs(call.func.value, env)
            others: list[str] = []
            for a in call.args:
                others.extend(self._refs(a, env))
            for a in base:
                for b in others:
                    self.edges.add((a, b) if name == "set_downstream" else (b, a))
            return base
        if name in {"chain", "chain_linear"}:
            groups = [self._refs(a, env) for a in call.args]
            for up, down in zip(groups, groups[1:]):
                for a in up:
                    for b in down:
                        self.edges.add((a, b))
            return groups[-1] if groups else []
        if name == "cross_downstream":
            args = list(call.args)
            up = self._refs(args[0] if args else _kw(call, "from_tasks"), env)
            down = self._refs(args[1] if len(args) > 1 else _kw(call, "to_tasks"), env)
            for a in up:
                for b in down:
                    self.edges.add((a, b))
            return down
        return []

    def _visit(self, stmts, env: dict[str, list[str]]) -> None:
        for stmt in stmts or []:
            if isinstance(stmt, ast.Expr):
                self._refs(stmt.value, env)
            elif isinstance(stmt, (ast.Assign, ast.AnnAssign)):
                value = stmt.value
                targets = stmt.targets if isinstance(stmt, ast.Assign) else [stmt.target]
                if isinstance(value, (ast.List, ast.Tuple, ast.ListComp)) and len(targets) == 1 and \
                        isinstance(targets[0], ast.Name):
                    self.list_vars[targets[0].id] = self._refs(value, env)
                elif isinstance(value, ast.BinOp):
                    self._refs(value, env)
            if isinstance(stmt, (ast.For, ast.AsyncFor)):
                inner = dict(env)
                if isinstance(stmt.target, ast.Name):
                    refs = self._refs(stmt.iter, env)
                    if refs:
                        inner[stmt.target.id] = refs
                self._visit(stmt.body, inner)
                self._visit(stmt.orelse, env)
                continue
            for fld in ("body", "orelse", "finalbody"):
                body = getattr(stmt, fld, None)
                if isinstance(body, list):
                    self._visit(body, env)
            for handler in getattr(stmt, "handlers", []) or []:
                self._visit(handler.body, env)

    # -- queries ------------------------------------------------------------
    def downstream(self, var: str) -> set[str]:
        return {b for a, b in self.edges if a == var}

    def upstream(self, var: str) -> set[str]:
        return {a for a, b in self.edges if b == var}

    def descendants(self, var: str) -> set[str]:
        seen: set[str] = set()
        stack = [var]
        while stack:
            cur = stack.pop()
            for nxt in self.downstream(cur):
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
        return seen

    def operator_calls(self) -> list[_Task]:
        return sorted(self.tasks.values(), key=lambda t: t.lineno)


@lru_cache(maxsize=128)
def _airflow_model(code: str) -> _AirflowModel | None:
    tree = _parse_python(code)
    if tree is None:
        return None
    try:
        return _AirflowModel(tree)
    except Exception:  # defensive: never let model building break a rule
        logger.debug("layer1_static: failed to build Airflow model", exc_info=True)
        return None


def _regex_lines(code: str, pattern: str) -> list[int]:
    text = _strip_code_fences(code)
    return [_line_at(text, m.start()) for m in re.finditer(pattern, text)]


# ---------------------------------------------------------------------------
# AIRFLOW RULES (A01-A06)
# ---------------------------------------------------------------------------

_SAFE_DEFAULT_TRIGGER = {None, "all_success"}


def check_airflow_default_trigger_rule(dag_code: str) -> list[Finding]:
    """Rule A01: Downstream tasks using default trigger_rule='all_success'
    after BranchPythonOperator.

    A branch operator marks every non-selected path as *skipped*. A task that
    joins those paths with the default trigger rule is skipped as well, so the
    pipeline 'succeeds' without loading anything."""
    findings: list[Finding] = []
    model = _airflow_model(dag_code)
    branch_re = r"\bBranch\w*Operator\s*\(|@task\.branch|@branch_task"
    if model is None:
        lines = _regex_lines(dag_code, branch_re)
        if lines and "trigger_rule" not in dag_code:
            findings.append(Finding(
                "A01", "medium",
                "Branch operator is used but no task sets trigger_rule; a task joining the branches with "
                "the default 'all_success' is skipped whenever a branch is skipped.", lines[0], "FM6"))
        return findings

    default_rule = _trigger_rule_value(model.default_args.get("trigger_rule"))
    branches = [t for t in model.tasks.values() if t.is_branch]
    for branch in sorted(branches, key=lambda t: t.lineno):
        desc = model.descendants(branch.var)
        if not desc:
            if "trigger_rule" not in dag_code and len(model.tasks) >= 3:
                findings.append(Finding(
                    "A01", "medium",
                    f"Branch task '{branch.label}' is defined but its downstream dependencies could not be "
                    "resolved and no task sets trigger_rule; a task joining the branches with the default "
                    "'all_success' is always skipped.", branch.lineno, "FM6"))
            continue
        for var in sorted(desc):
            task = model.tasks.get(var)
            if task is None or task.has_star_kwargs:
                continue
            ups = model.upstream(var)
            related = ups & (desc | {branch.var})
            fan_in = len(ups) >= 2 or any(u in model.tasks and model.tasks[u].multi for u in related)
            if not fan_in or not related or task.is_branch:
                continue
            rule = task.trigger_rule or default_rule
            if rule in _SAFE_DEFAULT_TRIGGER:
                up_labels = ", ".join(sorted(model.tasks[u].label if u in model.tasks else u for u in ups))
                findings.append(Finding(
                    "A01", "high",
                    f"Task '{task.label}' joins paths downstream of branch task '{branch.label}' "
                    f"(upstream: {up_labels}) but uses the default trigger_rule='all_success'; it is "
                    "skipped whenever a non-selected branch is skipped. Use "
                    "trigger_rule='none_failed_min_one_success'.", task.lineno, "FM6"))
    return _finalize(findings)


def check_airflow_sensor_no_timeout(dag_code: str) -> list[Finding]:
    """Rule A02: Sensors without explicit timeout parameter.

    The default sensor timeout is 7 days. In the default 'poke' mode the
    sensor also occupies a worker slot for that whole time."""
    findings: list[Finding] = []
    model = _airflow_model(dag_code)
    if model is None:
        text = _strip_code_fences(dag_code)
        masked_lines = text.split("\n")
        for m in re.finditer(r"\b(\w+Sensor)\s*\(", text):
            if re.match(r"\s*class\s", masked_lines[_line_at(text, m.start()) - 1]):
                continue
            depth, end = 0, None
            for k in range(m.end() - 1, len(text)):
                if text[k] == "(":
                    depth += 1
                elif text[k] == ")":
                    depth -= 1
                    if depth == 0:
                        end = k
                        break
            body = text[m.end():end] if end else text[m.end():m.end() + 500]
            if not re.search(r"\btimeout\s*=", body) and not re.search(r"['\"]timeout['\"]\s*:", text):
                findings.append(Finding(
                    "A02", "high",
                    f"{m.group(1)} has no timeout; the default is 7 days.", _line_at(text, m.start()), "FM6"))
        return _finalize(findings)

    default_timeout = "timeout" in model.default_args
    default_exec_timeout = "execution_timeout" in model.default_args
    default_mode = _const_str(model.default_args.get("mode"))

    def emit(label: str, op: str, line: int, has_exec_timeout: bool, mode: str | None, deferrable: bool):
        mode = (mode or default_mode or "poke").lower()
        if has_exec_timeout and mode == "poke" and not deferrable:
            findings.append(Finding(
                "A02", "low",
                f"Sensor '{label}' ({op}) has no timeout and is bounded only by execution_timeout; set "
                "timeout explicitly so the sensor fails with AirflowSensorTimeout and soft_fail works.",
                line, "FM6"))
        elif mode == "reschedule" or deferrable:
            findings.append(Finding(
                "A02", "medium",
                f"Sensor '{label}' ({op}) has no timeout; it keeps waiting for the default 7 days before "
                "failing, so a missing upstream goes unnoticed.", line, "FM6"))
        else:
            findings.append(Finding(
                "A02", "high",
                f"Sensor '{label}' ({op}) has no timeout and runs in mode='poke': it holds a worker slot "
                "for up to the default 7 days when the condition never becomes true. Set timeout (and "
                "mode='reschedule').", line, "FM6"))

    for task in model.operator_calls():
        if not task.is_sensor:
            continue
        if task.call is not None:
            call = task.call
            if _has_star_kwargs(call) or _kw(call, "timeout") is not None or default_timeout:
                continue
            deferrable = isinstance(_kw(call, "deferrable"), ast.Constant) and bool(_kw(call, "deferrable").value)
            emit(task.label, task.operator, task.lineno,
                 _kw(call, "execution_timeout") is not None or default_exec_timeout,
                 _const_str(_kw(call, "mode")), deferrable)

    # TaskFlow sensors: @task.sensor(...)
    for fn, (dotted, kws, lineno) in model.task_fns.items():
        if not dotted.lower().endswith("sensor"):
            continue
        kwmap = {k.arg: k.value for k in kws if k.arg}
        if "timeout" in kwmap or default_timeout or any(k.arg is None for k in kws):
            continue
        emit(fn, "@" + dotted, lineno, "execution_timeout" in kwmap or default_exec_timeout,
             _const_str(kwmap.get("mode")), False)
    return _finalize(findings)


_NOW_ATTRS = {"now", "utcnow", "today"}
_NOW_BASES = {"datetime", "datetime.datetime", "dt", "dt.datetime", "date", "datetime.date", "dt.date",
              "pendulum", "pendulum.DateTime", "pendulum.datetime", "timezone", "pd.Timestamp",
              "pandas.Timestamp", "arrow"}
_DATE_KW = {"start_date", "end_date"}


def check_airflow_datetime_now(dag_code: str) -> list[Finding]:
    """Rule A03: Using datetime.now() instead of Airflow macros ({{ ds }}).

    Wall-clock time makes a task non-idempotent: retries, backfills and late
    runs process a different window than the scheduled data interval. As a
    start_date it moves on every DAG parse and the DAG may never run."""
    findings: list[Finding] = []
    tree = _parse_python(dag_code)
    if tree is None:
        text = _strip_code_fences(dag_code)
        for m in re.finditer(r"\b(datetime|date|pendulum|timezone)\.(now|utcnow|today)\s*\(", text):
            findings.append(Finding(
                "A03", "medium",
                f"{m.group(1)}.{m.group(2)}() uses wall-clock time; use the run's logical date "
                "({{ ds }}, data_interval_start) so reruns and backfills are reproducible.",
                _line_at(text, m.start()), "FM2"))
        return _finalize(findings)

    parents = _parent_map(tree)

    def context(node) -> tuple[bool, bool]:
        """(is_date_argument, runs_at_parse_time)."""
        is_date_arg = False
        parse_time = True
        cur = node
        while cur in parents:
            parent = parents[cur]
            if isinstance(parent, ast.keyword) and parent.arg in _DATE_KW:
                is_date_arg = True
            if isinstance(parent, ast.Dict):
                for k, v in zip(parent.keys, parent.values):
                    if v is cur and k is not None and _const_str(k) in _DATE_KW:
                        is_date_arg = True
            if isinstance(parent, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if cur in parent.body and not any(_is_dag_decorator(d) for d in parent.decorator_list):
                    parse_time = False
            elif isinstance(parent, ast.Lambda):
                parse_time = False
            cur = parent
        return is_date_arg, parse_time

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Attribute) and func.attr in _NOW_ATTRS and _dotted(func.value) in _NOW_BASES:
            expr = f"{_dotted(func.value)}.{func.attr}()"
            is_date_arg, parse_time = context(node)
            if is_date_arg:
                findings.append(Finding(
                    "A03", "high",
                    f"{expr} is used for start_date/end_date: the value changes on every DAG parse, so the "
                    "schedule is unpredictable and the DAG may never trigger. Use a static datetime.",
                    node.lineno, "FM2"))
            elif parse_time:
                findings.append(Finding(
                    "A03", "high",
                    f"{expr} is evaluated at DAG parse time, not at task run time; the value is unrelated "
                    "to the run being processed. Use templated macros ({{ ds }}, {{ data_interval_start }}).",
                    node.lineno, "FM2"))
            else:
                findings.append(Finding(
                    "A03", "medium",
                    f"{expr} inside a task makes it non-idempotent: retries and backfills process "
                    "'today' instead of the run's data interval. Use the logical date from the task "
                    "context ({{ ds }}, data_interval_start).", node.lineno, "FM2"))
        elif _call_name(node) == "days_ago":
            is_date_arg, _ = context(node)
            if is_date_arg:
                findings.append(Finding(
                    "A03", "medium",
                    "days_ago() gives a dynamic (and deprecated) start_date that shifts on every DAG "
                    "parse; use a static datetime.", node.lineno, "FM2"))
    return _finalize(findings)


def check_airflow_missing_catchup(dag_code: str) -> list[Finding]:
    """Rule A04: Missing catchup=False (backfill risk).

    On Airflow 2.x catchup defaults to True: when the DAG is deployed or
    unpaused the scheduler creates a run for every interval since start_date."""
    findings: list[Finding] = []
    model = _airflow_model(dag_code)
    if model is None:
        text = _strip_code_fences(dag_code)
        lines = _regex_lines(dag_code, r"\bDAG\s*\(|@dag\b")
        if lines and not re.search(r"\bcatchup\s*=", text):
            findings.append(Finding(
                "A04", "medium",
                "DAG does not set catchup=False; on Airflow 2.x every interval since start_date is "
                "backfilled when the DAG is enabled.", lines[0], "FM6"))
        return findings

    for lineno, keywords, star in model.dags:
        kwmap = {k.arg: k.value for k in keywords if k.arg}
        if star:
            continue
        schedule_given = [kwmap[k] for k in ("schedule", "schedule_interval", "timetable") if k in kwmap]
        if schedule_given and all(isinstance(v, ast.Constant) and v.value is None for v in schedule_given):
            continue  # manually triggered DAG: nothing to backfill
        catchup = kwmap.get("catchup")
        if catchup is None:
            findings.append(Finding(
                "A04", "medium",
                "DAG does not set catchup=False: on Airflow 2.x (default catchup=True) enabling the DAG "
                "launches a run for every schedule interval since start_date (backfill storm, duplicate "
                "loads for non-idempotent tasks).", lineno, "FM6"))
        elif isinstance(catchup, ast.Constant) and catchup.value is True:
            findings.append(Finding(
                "A04", "low",
                "DAG sets catchup=True: every missed interval since start_date is backfilled; make sure "
                "all tasks are idempotent and bounded by max_active_runs.", lineno, "FM6"))
    return _finalize(findings)


_URI_WITH_CREDS_RE = re.compile(r"\b[a-zA-Z][a-zA-Z0-9+.\-]*://[^\s:/@'\"{}]+:[^\s@/'\"{}]+@[^\s/'\"]+")
_DB_URI_RE = re.compile(
    r"\b(?:jdbc:[a-z0-9]+:|(?:postgres(?:ql)?|mysql|mariadb|mssql|oracle|redshift|snowflake|mongodb|redis|"
    r"amqps?|sqlite|clickhouse|presto|trino|hive|impala|db2|teradata|vertica|sqlserver)(?:\+\w+)?://)\S+",
    re.I)
_DSN_SECRET_RE = re.compile(r"\b(password|pwd|passwd)\s*=\s*[^;\s'\"{}]+", re.I)
_SECRET_NAME_RE = re.compile(
    r"(password|passwd|pwd|secret|api_?key|access_?key|auth_?token|token|private_?key|credential)", re.I)
_SECRET_NAME_EXCLUDE_RE = re.compile(
    r"(conn_id|_var|_name|_path|_file|_url|_uri|_endpoint|_field|_column|_env|_key_name|_arn|_scope|"
    r"_type|_header|_prefix|_ttl|_expiry|_expires)$", re.I)
_CONN_KW_NAMES = {"host", "hostname", "server", "user", "username", "database", "dbname", "dsn",
                  "account", "port", "sid", "service_name", "password", "passwd"}
_CONNECT_FUNCS = {"connect", "create_engine", "MongoClient", "Redis", "StrictRedis", "Connection",
                  "create_connection", "from_url"}
_IP_RE = re.compile(r"^\d{1,3}(\.\d{1,3}){3}(:\d+)?$")


def _is_placeholder(value: str) -> bool:
    return (not value.strip()) or "{{" in value or value.startswith(("$", "%(")) or \
        re.fullmatch(r"<[^>]+>|x+|\*+|changeme|\.\.\.", value.strip(), re.I) is not None


def check_airflow_hardcoded_connection(dag_code: str) -> list[Finding]:
    """Rule A05: Hardcoded connection strings instead of Airflow
    Variables/Connections.

    Credentials and hosts embedded in DAG code leak through version control
    and pin every environment to the same database; they belong in an Airflow
    Connection (conn_id), Variable or a secrets backend."""
    findings: list[Finding] = []
    tree = _parse_python(dag_code)
    text = _strip_code_fences(dag_code)
    if tree is None:
        for m in _URI_WITH_CREDS_RE.finditer(text):
            findings.append(Finding(
                "A05", "high",
                "Connection URI with embedded credentials is hardcoded; use an Airflow Connection "
                "(conn_id) or a secrets backend.", _line_at(text, m.start()), "FM6"))
        for m in re.finditer(r"\b(password|passwd|pwd|secret|api_?key|token)\s*=\s*['\"][^'\"{}]+['\"]",
                             text, re.I):
            findings.append(Finding(
                "A05", "high",
                f"Hardcoded secret in '{m.group(1)}'; use an Airflow Connection/Variable.",
                _line_at(text, m.start()), "FM6"))
        return _finalize(findings)

    docstrings = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.body:
            first = node.body[0]
            if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant) and \
                    isinstance(first.value.value, str):
                docstrings.add(id(first.value))

    def secret_name(name: str | None) -> bool:
        return bool(name) and bool(_SECRET_NAME_RE.search(name)) and not _SECRET_NAME_EXCLUDE_RE.search(name)

    def literal(node) -> str | None:
        s = _const_str(node)
        if s is not None and not _is_placeholder(s):
            return s
        return None

    reported_lines: set[int] = set()

    def report(sev: str, msg: str, line: int) -> None:
        if line in reported_lines:
            return
        reported_lines.add(line)
        findings.append(Finding("A05", sev, msg, line, "FM6"))

    # 1. secrets assigned / passed by name
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            fname = _call_name(node)
            for k in node.keywords:
                if secret_name(k.arg) and literal(k.value) is not None:
                    report("high",
                           f"Hardcoded secret passed as {k.arg}=... to {fname or 'call'}(); read it from an "
                           "Airflow Connection, Variable or secrets backend.", k.value.lineno)
            if fname in _CONNECT_FUNCS:
                literal_kws = [k.arg for k in node.keywords
                               if k.arg in _CONN_KW_NAMES and isinstance(k.value, ast.Constant)
                               and k.value.value is not None and not (
                                   isinstance(k.value.value, str) and _is_placeholder(k.value.value))]
                if literal_kws:
                    report("medium",
                           f"{_dotted(node.func) or fname}() is called with hardcoded connection parameters "
                           f"({', '.join(literal_kws)}); use a Hook with conn_id or BaseHook.get_connection().",
                           node.lineno)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                name = target.id if isinstance(target, ast.Name) else (
                    target.attr if isinstance(target, ast.Attribute) else None)
                if secret_name(name) and literal(node.value) is not None:
                    report("high",
                           f"Hardcoded secret assigned to '{name}'; read it from an Airflow Connection, "
                           "Variable or secrets backend.", node.lineno)
        elif isinstance(node, ast.Dict):
            for k, v in zip(node.keys, node.values):
                key = _const_str(k) if k is not None else None
                if secret_name(key) and literal(v) is not None:
                    report("high",
                           f"Hardcoded secret under dict key '{key}'; read it from an Airflow Connection, "
                           "Variable or secrets backend.", v.lineno)

    # 2. connection strings inside string literals (incl. f-string fragments)
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Constant) and isinstance(node.value, str)) or id(node) in docstrings:
            continue
        value = node.value
        line = getattr(node, "lineno", None) or 1
        if _URI_WITH_CREDS_RE.search(value):
            report("high",
                   "Connection URI with embedded credentials is hardcoded "
                   f"({_short(re.sub(r':[^:@/]+@', ':***@', value), 50)}); use an Airflow Connection "
                   "(conn_id) or a secrets backend.", line)
        elif _DSN_SECRET_RE.search(value) and re.search(r"host|server|dbname|database|user|uid", value, re.I):
            report("high",
                   "DSN/connection string with an embedded password is hardcoded; use an Airflow "
                   "Connection (conn_id).", line)
        elif _DB_URI_RE.search(value):
            report("medium",
                   f"Database connection string is hardcoded ({_short(value, 50)}); environments cannot be "
                   "switched without a code change. Use an Airflow Connection (conn_id).", line)

    # 3. hardcoded host / IP keyword arguments on any call
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            for k in node.keywords:
                s = _const_str(k.value)
                if k.arg in {"host", "hostname", "server"} and s and (_IP_RE.match(s) or "." in s) \
                        and not _is_placeholder(s):
                    report("medium",
                           f"Hardcoded host '{_short(s, 40)}' passed as {k.arg}=...; use an Airflow "
                           "Connection (conn_id).", k.value.lineno)
    return _finalize(findings)


def check_airflow_missing_failure_callback(dag_code: str) -> list[Finding]:
    """Rule A06: Missing on_failure_callback.

    Without a failure callback (DAG-level, in default_args or per task) or
    e-mail alerting, a failed load is only visible to someone who opens the
    Airflow UI, and downstream consumers keep reading stale data."""
    findings: list[Finding] = []
    model = _airflow_model(dag_code)
    if model is None:
        text = _strip_code_fences(dag_code)
        lines = _regex_lines(dag_code, r"\bDAG\s*\(|@dag\b")
        if lines and "on_failure_callback" not in text and "email_on_failure" not in text:
            findings.append(Finding(
                "A06", "medium",
                "No on_failure_callback is configured for the DAG or its tasks; failures are silent.",
                lines[0], "FM6"))
        return findings

    tasks = model.operator_calls()
    if not model.dags and not tasks:
        return findings

    da = model.default_args
    if "on_failure_callback" in da:
        return findings
    for _, keywords, star in model.dags:
        if star or any(k.arg == "on_failure_callback" for k in keywords):
            return findings
    email_flag = da.get("email_on_failure")
    email_disabled = isinstance(email_flag, ast.Constant) and email_flag.value is False
    if "email" in da and not email_disabled:
        return findings  # e-mail alerting on failure is active

    def task_has_callback(t: _Task) -> bool:
        if t.call is not None:
            return _kw(t.call, "on_failure_callback") is not None or t.has_star_kwargs
        dotted, kws, _ = model.task_fns.get(t.task_id or "", ("", [], 0))
        return any(k.arg == "on_failure_callback" for k in kws)

    with_cb = [t for t in tasks if task_has_callback(t)]
    without_cb = [t for t in tasks if not task_has_callback(t)]
    line = model.dags[0][0] if model.dags else (tasks[0].lineno if tasks else None)
    if not with_cb:
        findings.append(Finding(
            "A06", "medium",
            "No on_failure_callback is defined on the DAG, in default_args or on any task (and no failure "
            "e-mail is configured); task failures raise no alert and stale data goes unnoticed.",
            line, "FM6"))
    elif without_cb:
        names = ", ".join(t.label for t in without_cb[:6]) + (", ..." if len(without_cb) > 6 else "")
        findings.append(Finding(
            "A06", "low",
            f"on_failure_callback is set on some tasks only; {len(without_cb)} task(s) fail silently: "
            f"{names}. Move the callback to default_args.", without_cb[0].lineno, "FM6"))
    return _finalize(findings)


# ---------------------------------------------------------------------------
# PYTHON / ETL RULES (P01-P05)
# ---------------------------------------------------------------------------

def _iter_calls(tree) -> Iterator[ast.Call]:
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            yield node


def check_python_merge_default(etl_code: str) -> list[Finding]:
    """Rule P01: pandas merge() without explicit 'how' parameter
    (defaults to inner, silently drops rows)."""
    findings: list[Finding] = []
    tree = _parse_python(etl_code)
    if tree is None:
        text = _strip_code_fences(etl_code)
        for m in re.finditer(r"\.merge\s*\(", text):
            window = text[m.end():m.end() + 400]
            end = window.find("\n\n")
            if "how" not in (window if end == -1 else window[:end]):
                findings.append(Finding(
                    "P01", "medium",
                    "merge() without explicit how=: the default inner join silently drops unmatched rows.",
                    _line_at(text, m.start()), "FM1"))
        return _finalize(findings)

    for call in _iter_calls(tree):
        func = call.func
        if not (isinstance(func, ast.Attribute) and func.attr == "merge"):
            continue
        if _kw(call, "how") is not None or _has_star_kwargs(call):
            continue
        base = _dotted(func.value)
        module_level = base in {"pd", "pandas", "dd", "dask.dataframe", "cudf", "ps", "modin.pandas", "mpd"}
        how_position = 2 if module_level else 1   # pd.merge(left, right, how) / df.merge(right, how)
        if len(call.args) > how_position and not any(isinstance(a, ast.Starred) for a in call.args):
            continue
        if not module_level and not call.args and not any(
                k.arg in {"right", "on", "left_on", "right_on"} for k in call.keywords):
            continue  # not a DataFrame merge (no right-hand frame or keys)
        target = f"{base}.merge" if base else "merge"
        findings.append(Finding(
            "P01", "medium",
            f"{target}() without explicit how=: pandas defaults to an inner join, which silently drops "
            "rows without a match on either side. State how='left'/'inner'/... (and consider "
            "validate= and indicator=True).", call.lineno, "FM1"))
    return _finalize(findings)


def check_python_nan_handling(etl_code: str) -> list[Finding]:
    """Rule P02: Operations that silently drop NaN without explicit handling.

    * ``df.dropna()`` with no subset/how/thresh removes any row with a NaN in
      any column;
    * ``groupby`` drops NaN keys unless ``dropna=False``;
    * ``value_counts`` / ``nunique`` / ``pivot_table`` / ``crosstab`` exclude
      NaN by default;
    * ``errors='coerce'`` turns unparseable values into NaN/NaT that are later
      dropped by the above."""
    findings: list[Finding] = []
    tree = _parse_python(etl_code)
    if tree is None:
        text = _strip_code_fences(etl_code)
        for m in re.finditer(r"\.dropna\s*\(\s*\)", text):
            findings.append(Finding(
                "P02", "medium", "dropna() without subset drops every row containing any NaN.",
                _line_at(text, m.start()), "FM5"))
        for m in re.finditer(r"\.groupby\s*\(", text):
            if "dropna" not in text[m.end():m.end() + 200].split("\n")[0]:
                findings.append(Finding(
                    "P02", "medium", "groupby() drops NaN keys by default; pass dropna=False.",
                    _line_at(text, m.start()), "FM5"))
        return _finalize(findings)

    for call in _iter_calls(tree):
        func = call.func
        name = _call_name(call)
        is_method = isinstance(func, ast.Attribute)
        if _has_star_kwargs(call):
            continue
        kws = {k.arg for k in call.keywords}

        if is_method and name == "dropna":
            if not kws & {"subset", "how", "thresh"} and not call.args:
                findings.append(Finding(
                    "P02", "medium",
                    "dropna() without subset/how/thresh removes every row that has a NaN in ANY column; "
                    "rows are lost silently. Restrict with subset=[...] and log the number of dropped rows.",
                    call.lineno, "FM5"))
        elif is_method and name == "groupby":
            if "dropna" not in kws and (call.args or kws & {"by", "level"}):
                findings.append(Finding(
                    "P02", "medium",
                    "groupby() excludes rows whose key is NaN (dropna=True by default); totals no longer "
                    "reconcile with the input. Pass dropna=False or fill the keys explicitly.",
                    call.lineno, "FM5"))
        elif is_method and name in {"value_counts", "nunique"}:
            if "dropna" not in kws:
                findings.append(Finding(
                    "P02", "low",
                    f"{name}() ignores NaN by default; pass dropna=False if missing values must be counted.",
                    call.lineno, "FM5"))
        elif name in {"pivot_table", "crosstab"}:
            if "dropna" not in kws and "fill_value" not in kws:
                findings.append(Finding(
                    "P02", "low",
                    f"{name}() drops NaN groups/columns by default (dropna=True) and leaves gaps unfilled; "
                    "set dropna= / fill_value= explicitly.", call.lineno, "FM5"))
        elif name in {"to_numeric", "to_datetime", "to_timedelta", "astype"}:
            errors = _kw(call, "errors")
            if _const_str(errors) == "coerce":
                findings.append(Finding(
                    "P02", "medium",
                    f"{name}(errors='coerce') silently converts unparseable values to NaN/NaT; they are "
                    "then dropped or ignored by later aggregations. Count and report the coerced values.",
                    call.lineno, "FM5"))
    return _finalize(findings)


_READ_TEXT_TABLE_FUNCS = {"read_csv", "read_table", "read_fwf"}


def check_python_read_csv_dtype(etl_code: str) -> list[Finding]:
    """Rule P03: pd.read_csv without explicit dtype (type inference risk).

    Inference turns identifiers with leading zeros into integers, integer
    columns with a missing value into floats, and can pick different types
    for different files or chunks of the same feed."""
    findings: list[Finding] = []
    tree = _parse_python(etl_code)
    funcs = _READ_TEXT_TABLE_FUNCS | {"read_excel"}
    if tree is None:
        text = _strip_code_fences(etl_code)
        for m in re.finditer(r"\b(read_csv|read_table|read_fwf|read_excel)\s*\(", text):
            stmt = text[m.end():m.end() + 400].split("\n\n")[0]
            if "dtype" not in stmt and "converters" not in stmt:
                findings.append(Finding(
                    "P03", "medium",
                    f"{m.group(1)}() without dtype=: column types are inferred from the data.",
                    _line_at(text, m.start()), "FM5"))
        return _finalize(findings)

    for call in _iter_calls(tree):
        name = _call_name(call)
        if name not in funcs or _has_star_kwargs(call):
            continue
        if isinstance(call.func, ast.Attribute) and isinstance(call.func.value, ast.Name) and \
                call.func.value.id in {"spark", "self"}:
            continue
        if _kw(call, "dtype") is not None or _kw(call, "converters") is not None:
            continue
        base = _dotted(call.func.value) if isinstance(call.func, ast.Attribute) else ""
        target = f"{base}.{name}" if base else name
        findings.append(Finding(
            "P03", "medium",
            f"{target}() without explicit dtype=: pandas infers types per file, so IDs lose leading zeros, "
            "integer columns with a missing value become float, and mixed chunks yield object columns. "
            "Declare dtype= (and parse_dates=) for the expected schema.", call.lineno, "FM5"))
    return _finalize(findings)


_COMPRESSED_OPENERS = {"gzip", "bz2", "lzma"}
_TEXT_MODE_RE = re.compile(r"^[rwxaUt+]+$")


def check_python_missing_encoding(etl_code: str) -> list[Finding]:
    """Rule P04: Missing encoding parameter in file operations.

    Text-mode open()/read_text()/write_text() use the platform locale encoding
    (cp1252 on Windows, UTF-8 on most Linux images), so the same script
    produces different bytes - or mojibake - in different environments."""
    findings: list[Finding] = []
    tree = _parse_python(etl_code)
    if tree is None:
        text = _strip_code_fences(etl_code)
        for m in re.finditer(r"(?<![\w.])open\s*\(([^()]*)\)", text):
            body = m.group(1)
            if "encoding" not in body and not re.search(r"['\"][rwax+]*b[rwax+]*['\"]", body):
                findings.append(Finding(
                    "P04", "medium",
                    "open() in text mode without encoding=: the platform default encoding is used.",
                    _line_at(text, m.start()), "FM5"))
        return _finalize(findings)

    def mode_of(call: ast.Call, position: int, default: str) -> str | None:
        node = _kw(call, "mode")
        if node is None and len(call.args) > position:
            node = call.args[position]
        if node is None:
            return default
        return _const_str(node)  # None when dynamic

    for call in _iter_calls(tree):
        if _has_star_kwargs(call) or any(isinstance(a, ast.Starred) for a in call.args):
            continue
        func = call.func
        name = _call_name(call)
        has_encoding = _kw(call, "encoding") is not None

        if isinstance(func, ast.Name) and name == "open":
            mode = mode_of(call, 1, "r")
            if mode is None or "b" in mode or has_encoding or len(call.args) >= 4:
                continue
            findings.append(Finding(
                "P04", "medium",
                f"open(..., '{mode}') in text mode without encoding=: the locale's default encoding is used, "
                "so output differs between environments and non-ASCII data is corrupted. Pass "
                "encoding='utf-8'.", call.lineno, "FM5"))
        elif isinstance(func, ast.Attribute) and name == "open":
            base = _dotted(func.value)
            if base in {"io", "codecs"}:
                mode = mode_of(call, 1, "r")
                enc_pos = 3 if base == "io" else 2
                if mode is None or "b" in mode or has_encoding or len(call.args) > enc_pos:
                    continue
                findings.append(Finding(
                    "P04", "medium",
                    f"{base}.open() in text mode without encoding=; pass encoding='utf-8'.",
                    call.lineno, "FM5"))
            elif base in _COMPRESSED_OPENERS:
                mode = mode_of(call, 1, "rb")
                if mode is None or "t" not in mode or has_encoding:
                    continue
                findings.append(Finding(
                    "P04", "medium",
                    f"{base}.open(..., '{mode}') in text mode without encoding=; pass encoding='utf-8'.",
                    call.lineno, "FM5"))
            else:
                # pathlib-style obj.open(mode='r'); only when the receiver/mode makes that clear
                is_path = isinstance(func.value, ast.Call) and _call_name(func.value) in {
                    "Path", "PurePath", "PosixPath", "WindowsPath"}
                mode_node = _kw(call, "mode") or (call.args[0] if call.args else None)
                mode = _const_str(mode_node) if mode_node is not None else ("r" if is_path else None)
                if mode is None or not _TEXT_MODE_RE.match(mode) or "b" in mode:
                    continue
                if not is_path and mode_node is None:
                    continue
                if has_encoding or len(call.args) >= 3:
                    continue
                findings.append(Finding(
                    "P04", "medium",
                    f"{base or 'path'}.open('{mode}') in text mode without encoding=; pass "
                    "encoding='utf-8'.", call.lineno, "FM5"))
        elif isinstance(func, ast.Attribute) and name == "read_text":
            if not has_encoding and not call.args:
                findings.append(Finding(
                    "P04", "medium",
                    "read_text() without encoding=: the locale's default encoding is used; pass "
                    "encoding='utf-8'.", call.lineno, "FM5"))
        elif isinstance(func, ast.Attribute) and name == "write_text":
            if not has_encoding and len(call.args) < 2:
                findings.append(Finding(
                    "P04", "medium",
                    "write_text() without encoding=: the locale's default encoding is used; pass "
                    "encoding='utf-8'.", call.lineno, "FM5"))
        elif name in _READ_TEXT_TABLE_FUNCS:
            if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name) and \
                    func.value.id in {"spark", "self"}:
                continue
            if not has_encoding:
                findings.append(Finding(
                    "P04", "low",
                    f"{name}() without encoding=: pandas assumes UTF-8; files exported as "
                    "Latin-1/cp1252/UTF-16 raise or decode to mojibake. State the source encoding "
                    "explicitly.", call.lineno, "FM5"))
    return _finalize(findings)


_MUTABLE_FACTORIES = {"list", "dict", "set", "defaultdict", "OrderedDict", "Counter", "deque",
                      "bytearray", "DataFrame", "Series", "array", "zeros", "ones", "empty"}


def _mutable_default_kind(node) -> str | None:
    if isinstance(node, (ast.List, ast.ListComp)):
        return "list"
    if isinstance(node, (ast.Dict, ast.DictComp)):
        return "dict"
    if isinstance(node, (ast.Set, ast.SetComp)):
        return "set"
    if isinstance(node, ast.Call):
        name = _call_name(node)
        if name in _MUTABLE_FACTORIES:
            return f"{_dotted(node.func) or name}()"
        if isinstance(node.func, ast.Attribute) and name in _NOW_ATTRS and _dotted(node.func.value) in _NOW_BASES:
            return f"call:{_dotted(node.func)}()"
    return None


def check_python_mutable_default_args(etl_code: str) -> list[Finding]:
    """Rule P05: Mutable default arguments in function definitions.

    Defaults are evaluated once, at definition time. A list/dict/set default
    is shared between calls (state leaks from one batch to the next) and a
    ``datetime.now()`` default is frozen at import time."""
    findings: list[Finding] = []
    tree = _parse_python(etl_code)
    if tree is None:
        text = _strip_code_fences(etl_code)
        for m in re.finditer(r"\bdef\s+(\w+)\s*\(([^)]*)\)", text, re.S):
            for arg in re.finditer(r"(\w+)\s*(?::[^=,]+)?=\s*(\[\s*\]|\{\s*\}|list\(\)|dict\(\)|set\(\))",
                                   m.group(2)):
                findings.append(Finding(
                    "P05", "medium",
                    f"Function '{m.group(1)}' has mutable default argument {arg.group(1)}={arg.group(2)}; "
                    "it is shared between calls. Use None and create the object inside the function.",
                    _line_at(text, m.start()), None))
        return _finalize(findings)

    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
            continue
        fname = getattr(node, "name", "<lambda>")
        args = node.args
        positional = [*args.posonlyargs, *args.args]
        pairs = list(zip(positional[len(positional) - len(args.defaults):], args.defaults))
        pairs += [(a, d) for a, d in zip(args.kwonlyargs, args.kw_defaults) if d is not None]
        for arg, default in pairs:
            kind = _mutable_default_kind(default)
            if kind is None:
                continue
            line = getattr(default, "lineno", None) or getattr(node, "lineno", None)
            if kind.startswith("call:"):
                findings.append(Finding(
                    "P05", "medium",
                    f"Function '{fname}' evaluates default {arg.arg}={kind[5:]} once at definition time; "
                    "every later call reuses the timestamp of the first import. Use None and compute it "
                    "inside the function.", line, None))
            else:
                findings.append(Finding(
                    "P05", "medium",
                    f"Function '{fname}' has mutable default argument {arg.arg}={kind}; the object is "
                    "created once and shared between calls, so state leaks across invocations. Use None "
                    "and create it inside the function.", line, None))
    return _finalize(findings)


# ---------------------------------------------------------------------------
# Rule registry
# ---------------------------------------------------------------------------

RULES_SQL = [
    check_sql_missing_join_condition,           # S01
    check_sql_group_by_mismatch,                # S02
    check_sql_missing_timezone,                 # S03
    check_sql_missing_partition_filter,         # S04
    check_sql_distinct_in_aggregation,          # S05
    check_sql_between_timestamps,               # S06
    check_sql_implicit_type_coercion,           # S07
    check_sql_select_star,                      # S08
    check_sql_missing_null_handling,            # S09
    check_sql_date_trunc_granularity,           # S10
    check_sql_scalar_subquery_multiple_rows,    # S11
    check_sql_window_missing_order_by,          # S12
]

RULES_AIRFLOW = [
    check_airflow_default_trigger_rule,         # A01
    check_airflow_sensor_no_timeout,            # A02
    check_airflow_datetime_now,                 # A03
    check_airflow_missing_catchup,              # A04
    check_airflow_hardcoded_connection,         # A05
    check_airflow_missing_failure_callback,     # A06
]

RULES_PYTHON = [
    check_python_merge_default,                 # P01
    check_python_nan_handling,                  # P02
    check_python_read_csv_dtype,                # P03
    check_python_missing_encoding,              # P04
    check_python_mutable_default_args,          # P05
]

ALL_RULES: list[Callable[..., list[Finding]]] = [*RULES_SQL, *RULES_AIRFLOW, *RULES_PYTHON]

RULE_IDS: dict[str, Callable[..., list[Finding]]] = {
    **{f"S{i:02d}": rule for i, rule in enumerate(RULES_SQL, 1)},
    **{f"A{i:02d}": rule for i, rule in enumerate(RULES_AIRFLOW, 1)},
    **{f"P{i:02d}": rule for i, rule in enumerate(RULES_PYTHON, 1)},
}


def analyze(code: str, category: str, schema: dict | None = None) -> list[Finding]:
    """Run every Layer 1 rule for ``category`` over ``code``.

    ``schema`` (optional, corpus format) sharpens the SQL rules; it is ignored
    for Airflow and ETL code. A rule that raises is logged and skipped so that
    one defective rule never hides the findings of the others."""
    if category == "bigquery_sql":
        rules = RULES_SQL
    elif category == "airflow_dag":
        rules = RULES_AIRFLOW
    elif category == "etl_script":
        rules = RULES_PYTHON
    else:
        return []

    findings: list[Finding] = []
    for rule in rules:
        try:
            if rules is RULES_SQL:
                findings.extend(rule(code, schema))
            else:
                findings.extend(rule(code))
        except Exception:
            logger.exception("layer1_static: rule %s failed", getattr(rule, "__name__", rule))
    return findings
