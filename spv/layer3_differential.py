"""
SPV Layer 3: Differential Testing

Cross-generator comparison: each task is submitted to all three generators;
a solution is flagged if its output differs from both others (minority/singleton).

This layer operates without access to ground truth.
"""

import pandas as pd
import numpy as np


def compare_outputs(
    output_a: pd.DataFrame,
    output_b: pd.DataFrame,
    tolerance: float = 1e-6,
) -> bool:
    """Check if two outputs are equivalent (order-independent, float-tolerant)."""
    if set(output_a.columns) != set(output_b.columns):
        return False

    cols = sorted(output_a.columns)
    a = output_a[cols].sort_values(cols).reset_index(drop=True)
    b = output_b[cols].sort_values(cols).reset_index(drop=True)

    if len(a) != len(b):
        return False

    for col in cols:
        if a[col].dtype in (np.float64, np.float32):
            if not np.allclose(
                a[col].values, b[col].values, atol=tolerance, equal_nan=True
            ):
                return False
        else:
            if not (a[col] == b[col]).all():
                return False
    return True


def differential_test(
    outputs: dict[str, pd.DataFrame],
    tolerance: float = 1e-6,
) -> dict[str, bool]:
    """
    Given outputs from multiple generators for the same task,
    flag solutions that are in the minority.

    Args:
        outputs: {generator_name: output_dataframe}

    Returns:
        {generator_name: is_flagged}
    """
    generators = list(outputs.keys())
    n = len(generators)
    flags = {g: False for g in generators}

    if n < 2:
        return flags

    agreement_matrix = {}
    for i, g1 in enumerate(generators):
        for j, g2 in enumerate(generators):
            if i < j:
                agree = compare_outputs(outputs[g1], outputs[g2], tolerance)
                agreement_matrix[(g1, g2)] = agree

    if n == 3:
        g1, g2, g3 = generators
        agree_12 = agreement_matrix.get((g1, g2), False)
        agree_13 = agreement_matrix.get((g1, g3), False)
        agree_23 = agreement_matrix.get((g2, g3), False)

        if agree_12 and agree_13 and agree_23:
            pass  # all agree, no flags
        elif agree_12 and not agree_13 and not agree_23:
            flags[g3] = True  # g3 is the singleton
        elif agree_13 and not agree_12 and not agree_23:
            flags[g2] = True  # g2 is the singleton
        elif agree_23 and not agree_12 and not agree_13:
            flags[g1] = True  # g1 is the singleton
        else:
            # all three disagree
            flags = {g: True for g in generators}

    elif n == 2:
        g1, g2 = generators
        if not agreement_matrix.get((g1, g2), False):
            flags = {g: True for g in generators}

    return flags
