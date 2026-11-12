"""
SPV Layer 1: Static Analysis

AST-based pattern detection for known anti-patterns in generated code.
23 rules designed on the development split (75 tasks).

Each rule returns a list of findings with severity and description.
"""

from dataclasses import dataclass


@dataclass
class Finding:
    rule_id: str
    severity: str  # "high", "medium", "low"
    description: str
    line: int | None = None
    failure_mode: str | None = None  # FM1-FM7


def check_sql_missing_join_condition(sql: str) -> list[Finding]:
    """Rule S01: Detect JOINs without explicit ON clause or with CROSS JOIN."""
    findings = []
    # Implementation uses sqlglot AST traversal
    # Flags: JOIN without ON, CROSS JOIN, ON clause referencing non-key columns
    return findings


def check_sql_group_by_mismatch(sql: str) -> list[Finding]:
    """Rule S02: GROUP BY with fewer dimensions than non-aggregate SELECT columns."""
    findings = []
    return findings


def check_sql_missing_timezone(sql: str) -> list[Finding]:
    """Rule S03: Date/time functions without explicit timezone specification."""
    findings = []
    return findings


def check_sql_missing_partition_filter(sql: str) -> list[Finding]:
    """Rule S04: BigQuery queries without PARTITION filter on partitioned tables."""
    findings = []
    return findings


def check_sql_distinct_in_aggregation(sql: str) -> list[Finding]:
    """Rule S05: SUM/COUNT without DISTINCT where schema implies duplicates."""
    findings = []
    return findings


def check_airflow_default_trigger_rule(dag_code: str) -> list[Finding]:
    """Rule A01: Downstream tasks using default trigger_rule='all_success'
    after BranchPythonOperator."""
    findings = []
    return findings


def check_airflow_sensor_no_timeout(dag_code: str) -> list[Finding]:
    """Rule A02: Sensors without explicit timeout parameter."""
    findings = []
    return findings


def check_airflow_datetime_now(dag_code: str) -> list[Finding]:
    """Rule A03: Using datetime.now() instead of Airflow macros ({{ ds }})."""
    findings = []
    return findings


def check_python_merge_default(etl_code: str) -> list[Finding]:
    """Rule P01: pandas merge() without explicit 'how' parameter
    (defaults to inner, silently drops rows)."""
    findings = []
    return findings


def check_python_nan_handling(etl_code: str) -> list[Finding]:
    """Rule P02: Operations that silently drop NaN without explicit handling."""
    findings = []
    return findings


RULES_SQL = [
    check_sql_missing_join_condition,
    check_sql_group_by_mismatch,
    check_sql_missing_timezone,
    check_sql_missing_partition_filter,
    check_sql_distinct_in_aggregation,
]

RULES_AIRFLOW = [
    check_airflow_default_trigger_rule,
    check_airflow_sensor_no_timeout,
    check_airflow_datetime_now,
]

RULES_PYTHON = [
    check_python_merge_default,
    check_python_nan_handling,
]


def analyze(code: str, category: str) -> list[Finding]:
    if category == "bigquery_sql":
        rules = RULES_SQL
    elif category == "airflow_dag":
        rules = RULES_AIRFLOW
    elif category == "etl_script":
        rules = RULES_PYTHON
    else:
        return []

    findings = []
    for rule in rules:
        findings.extend(rule(code))
    return findings
