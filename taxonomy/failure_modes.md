# Failure Mode Taxonomy (FM1-FM7)

## FM1: Join Semantics Errors

AI generates SQL joins that are syntactically correct but semantically wrong for the data's cardinality. The most common pattern is an unintentional many-to-many join producing a cross product that inflates aggregation results.

**Example:** A revenue report joining `orders` and `payments` on `order_id` without accounting for multiple payment attempts per order, inflating total revenue by 2.3x.

**Detection:** Layer 2 cardinality-bound checks (95% detection rate on held-out data).

## FM2: Temporal Boundary Drift

Generated code mishandles time boundaries through off-by-one errors in date ranges, incorrect timezone conversions, or wrong inclusive/exclusive boundary logic.

**Example:** `WHERE date >= '2025-01-01' AND date < '2025-02-01'` vs. `WHERE date BETWEEN '2025-01-01' AND '2025-01-31'` behaves differently for TIMESTAMP columns.

**Detection:** Layer 2 temporal consistency checks (68% detection rate -- weakest category).

## FM3: Aggregation Scope Errors

Incorrect GROUP BY granularity or missing DISTINCT in aggregations. The code produces the right column names but wrong numbers.

**Example:** `COUNT(order_id)` instead of `COUNT(DISTINCT order_id)` when orders have multiple line items.

**Detection:** Layer 1 static rules + Layer 2 conservation checks (87% detection rate).

## FM4: Dialect Misinterpretation

BigQuery-specific syntax or semantics misapplied. Common in LLMs trained on mixed SQL dialects.

**Example:** Using `DATE_TRUNC(date_column, MONTH)` (PostgreSQL syntax) instead of `DATE_TRUNC(date_column, MONTH)` (BigQuery accepts this but with different NULL handling behavior).

**Detection:** Layer 1 dialect-specific static rules (83% detection rate).

## FM5: Schema Evolution Errors

Incorrect handling of NULLable columns, renamed fields, or schema changes over time.

**Example:** Accessing a nested field that may be NULL without COALESCE, causing silent row loss in downstream joins.

**Detection:** Layer 1 NULL-handling rules (n=2 in held-out; 100% but unreliable due to sample size).

## FM6: Orchestration Logic Errors

DAG dependency errors, incorrect trigger rules, sensor misconfiguration, or missing error handling in workflow definitions.

**Example:** Using default `trigger_rule='all_success'` on a task downstream of `BranchPythonOperator`, causing the task to be skipped when non-selected branches are marked as skipped.

**Detection:** Layer 1 Airflow-specific static rules (80% detection rate).

## FM7: Validation Gaps

Missing or incorrect data quality checks that allow corrupt data to pass through.

**Example:** Checking `COUNT(*) > 0` instead of comparing against expected row count ranges, allowing a query that returns a single aggregated row to pass.

**Detection:** Layer 1 validation pattern rules (80% detection rate).
