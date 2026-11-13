# Silent Data Corruption in AI-Generated Pipeline Code

Replication package for:

> **Silent Data Corruption in AI-Generated Pipeline Code: A Multi-Artifact Empirical Study**
> Timur Rakhmatullin, Softline Solutions

## Overview

This repository contains the task corpus, evaluation scripts, and Semantic Pipeline Verification (SPV) framework described in the paper. The study evaluates 150 data engineering tasks (450 generated solutions) across BigQuery SQL, Apache Airflow DAGs, and Python ETL scripts, finding a 24-percentage-point *silent failure gap* between standard QA pass rates (78%) and semantic correctness (54%).

## Repository Structure

```
corpus/                  # Synthetic task corpus (150 tasks)
  bigquery_sql/          # 70 BigQuery SQL transformation tasks
  airflow_dags/          # 40 Airflow DAG definition tasks
  etl_scripts/           # 40 Python ETL transformation tasks
solutions/               # Generated solutions (450 files)
  bigquery_sql/          # 70 × 3 generators = 210 SQL files
  airflow_dags/          # 40 × 3 generators = 120 Python files
  etl_scripts/           # 40 × 3 generators = 120 Python files
evaluation/              # Evaluation framework
  evaluate.py            # Main 4-level evaluation pipeline
  metrics.py             # Silent failure gap and derived metrics
spv/                     # Semantic Pipeline Verification framework
  layer1_static.py       # Layer 1: AST-based static analysis (23 rules)
  layer2_semantic.py     # Layer 2: Domain-specific semantic validation
  layer3_differential.py # Layer 3: Cross-generator differential testing
prompts/                 # Standardized generation prompts
taxonomy/                # FM1-FM7 failure mode taxonomy
```

## Solutions

Each task has three generated solutions from different LLMs:
- **GPT-5** (`gpt5.sql` / `gpt5.py`)
- **Claude Sonnet 4** (`claude_sonnet4.sql` / `claude_sonnet4.py`)
- **DeepSeek-V3** (`deepseek_v3.sql` / `deepseek_v3.py`)

Solutions are stored in `solutions/<category>/<task_id>/` with generation metadata in file headers.

## Task Format

Each task is a JSON file containing:
- `task_id`: Unique identifier
- `category`: One of `bigquery_sql`, `airflow_dag`, `etl_script`
- `description`: Natural language task description
- `schema`: Database schema with column types and descriptions
- `test_data_sample`: Sample rows from the test dataset
- `expected_output_sample`: Expected output rows
- `edge_cases`: Documented edge cases in the test data

## Evaluation Levels

1. **Syntactic validity**: AST/sqlglot parsing
2. **Execution success**: Runtime on test dataset
3. **Standard QA pass**: Schema match, row count, no NULL violations, no duplicate keys
4. **Semantic correctness**: Exact match against reference output (float tolerance 1e-6)

## Failure Mode Taxonomy

| Code | Name | Description |
|------|------|-------------|
| FM1 | Join Semantics | Unintentional many-to-many joins inflating aggregations |
| FM2 | Temporal Boundary Drift | Off-by-one in date ranges, timezone mishandling |
| FM3 | Aggregation Scope | Incorrect GROUP BY granularity, missing DISTINCT |
| FM4 | Dialect Misinterpretation | BigQuery-specific syntax misused |
| FM5 | Schema Evolution | Incorrect handling of NULLable or renamed columns |
| FM6 | Orchestration Logic | DAG dependency errors, incorrect trigger rules |
| FM7 | Validation Gaps | Missing or incorrect data quality checks |

## Key Results

- 78% of generated code passes conventional QA checks
- Only 54% is semantically correct (24 pp silent failure gap)
- SPV detects 86% of silent failures (bootstrap 95% CI: [76%, 92%])
- FM1 (join semantics) and FM2 (temporal drift) affect 44% of incorrect solutions

## Requirements

```
pip install -r requirements.txt
```

## License

Apache License 2.0
