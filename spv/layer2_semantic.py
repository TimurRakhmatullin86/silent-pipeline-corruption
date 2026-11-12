"""
SPV Layer 2: Semantic Validation

Domain-specific invariant checks applied to execution output.
These checks operate without access to ground truth.
"""

import numpy as np
import pandas as pd
from scipy import stats


def check_row_count_conservation(
    input_df: pd.DataFrame,
    output_df: pd.DataFrame,
    join_type: str,
    input_cardinalities: dict[str, int] | None = None,
) -> dict[str, bool | str]:
    """Check that output row count is bounded by theoretical maximum
    given input cardinalities and join type."""
    result = {"check": "row_count_conservation", "passed": True, "detail": ""}

    if join_type == "inner":
        if input_cardinalities:
            max_rows = min(input_cardinalities.values())
            if len(output_df) > max_rows:
                result["passed"] = False
                result["detail"] = (
                    f"Output has {len(output_df)} rows but inner join "
                    f"max is {max_rows}"
                )
    elif join_type == "cross":
        pass  # no bound violation possible
    return result


def check_sum_preservation(
    input_df: pd.DataFrame,
    output_df: pd.DataFrame,
    column: str,
    tolerance: float = 0.01,
) -> dict[str, bool | str]:
    """Check that SUM of a column is preserved through transformation."""
    result = {"check": "sum_preservation", "passed": True, "detail": ""}

    if column in input_df.columns and column in output_df.columns:
        input_sum = input_df[column].sum()
        output_sum = output_df[column].sum()
        if abs(input_sum - output_sum) / max(abs(input_sum), 1e-10) > tolerance:
            result["passed"] = False
            result["detail"] = (
                f"Sum of {column}: input={input_sum:.2f}, "
                f"output={output_sum:.2f}"
            )
    return result


def check_temporal_consistency(
    input_df: pd.DataFrame,
    output_df: pd.DataFrame,
    date_column: str,
) -> dict[str, bool | str]:
    """Check that output date range is bounded by input date range."""
    result = {"check": "temporal_consistency", "passed": True, "detail": ""}

    if date_column in input_df.columns and date_column in output_df.columns:
        input_min = pd.to_datetime(input_df[date_column]).min()
        input_max = pd.to_datetime(input_df[date_column]).max()
        output_min = pd.to_datetime(output_df[date_column]).min()
        output_max = pd.to_datetime(output_df[date_column]).max()

        if output_min < input_min or output_max > input_max:
            result["passed"] = False
            result["detail"] = (
                f"Output date range [{output_min}, {output_max}] "
                f"exceeds input [{input_min}, {input_max}]"
            )
    return result


def check_distribution_stability(
    input_df: pd.DataFrame,
    output_df: pd.DataFrame,
    column: str,
    alpha: float = 0.01,
) -> dict[str, bool | str]:
    """KS test for distribution stability of a numeric column."""
    result = {"check": "distribution_stability", "passed": True, "detail": ""}

    if column in input_df.columns and column in output_df.columns:
        input_vals = input_df[column].dropna().values
        output_vals = output_df[column].dropna().values

        if len(input_vals) > 5 and len(output_vals) > 5:
            ks_stat, p_value = stats.ks_2samp(input_vals, output_vals)
            if p_value < alpha:
                result["passed"] = False
                result["detail"] = (
                    f"KS test for {column}: stat={ks_stat:.3f}, "
                    f"p={p_value:.4f}"
                )
    return result


def validate(
    input_df: pd.DataFrame,
    output_df: pd.DataFrame,
    checks_config: list[dict],
) -> list[dict]:
    results = []
    for check_cfg in checks_config:
        check_type = check_cfg["type"]
        if check_type == "sum_preservation":
            results.append(
                check_sum_preservation(
                    input_df, output_df, check_cfg["column"]
                )
            )
        elif check_type == "temporal_consistency":
            results.append(
                check_temporal_consistency(
                    input_df, output_df, check_cfg["date_column"]
                )
            )
        elif check_type == "distribution_stability":
            results.append(
                check_distribution_stability(
                    input_df, output_df, check_cfg["column"]
                )
            )
    return results
