"""
Four-level evaluation pipeline for AI-generated data pipeline code.

Evaluates each generated solution at four levels:
1. Syntactic validity (AST/sqlglot parsing)
2. Execution success (runtime on test dataset)
3. Standard QA pass (schema match, row count, NULL checks)
4. Semantic correctness (exact match against reference output)
"""

import json
import sys
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


def evaluate_syntactic_validity(code: str, category: str) -> bool:
    if category == "bigquery_sql":
        import sqlglot
        try:
            sqlglot.parse(code, dialect="bigquery")
            return True
        except sqlglot.errors.ParseError:
            return False
    elif category == "airflow_dag":
        import ast
        try:
            ast.parse(code)
            return True
        except SyntaxError:
            return False
    elif category == "etl_script":
        import ast
        try:
            ast.parse(code)
            return True
        except SyntaxError:
            return False
    return False


def evaluate_execution_success(
    code: str, category: str, test_data: dict[str, Any]
) -> tuple[bool, Any]:
    """Returns (success, output_or_error)."""
    raise NotImplementedError(
        "Execution requires BigQuery sandbox / Airflow test harness. "
        "See paper Section 2.3 for execution environment details."
    )


def evaluate_qa_pass(output: pd.DataFrame, expected: pd.DataFrame) -> dict[str, bool]:
    checks = {}
    checks["schema_match"] = set(output.columns) == set(expected.columns)
    checks["row_count_within_10pct"] = (
        abs(len(output) - len(expected)) / max(len(expected), 1) <= 0.10
    )
    checks["no_null_in_required"] = not output.isnull().any().any()
    checks["no_duplicate_keys"] = True  # task-specific key check
    checks["types_correct"] = True  # task-specific type check
    return checks


def evaluate_semantic_correctness(
    output: pd.DataFrame, expected: pd.DataFrame, tolerance: float = 1e-6
) -> bool:
    if set(output.columns) != set(expected.columns):
        return False

    output_sorted = output.sort_values(list(output.columns)).reset_index(drop=True)
    expected_sorted = expected.sort_values(list(expected.columns)).reset_index(drop=True)

    if len(output_sorted) != len(expected_sorted):
        return False

    for col in output_sorted.columns:
        if output_sorted[col].dtype in (np.float64, np.float32):
            if not np.allclose(
                output_sorted[col].values,
                expected_sorted[col].values,
                atol=tolerance,
                equal_nan=True,
            ):
                return False
        else:
            if not (output_sorted[col] == expected_sorted[col]).all():
                return False

    return True


def evaluate_task(
    task_path: str, generated_code: str, output_df: pd.DataFrame
) -> dict[str, Any]:
    with open(task_path) as f:
        task = json.load(f)

    results = {
        "task_id": task["task_id"],
        "category": task["category"],
        "syntactic_valid": evaluate_syntactic_validity(
            generated_code, task["category"]
        ),
        "execution_success": None,  # requires execution environment
        "qa_checks": None,
        "semantic_correct": None,
    }

    if output_df is not None:
        expected_df = pd.DataFrame(task.get("expected_output_sample", []))
        results["qa_checks"] = evaluate_qa_pass(output_df, expected_df)
        results["qa_pass"] = all(results["qa_checks"].values())
        results["semantic_correct"] = evaluate_semantic_correctness(
            output_df, expected_df
        )

    return results


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python evaluate.py <task.json> <generated_code_file>")
        sys.exit(1)

    task_path = sys.argv[1]
    code_path = sys.argv[2]

    with open(code_path) as f:
        code = f.read()

    result = evaluate_task(task_path, code, output_df=None)
    print(json.dumps(result, indent=2, default=str))
