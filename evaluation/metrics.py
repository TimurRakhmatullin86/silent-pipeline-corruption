"""
Derived metrics from the four-level evaluation.

Computes:
- Silent failure gap = QA pass rate - Semantic correctness rate
- Conditional silent failure rate = (QA pass AND NOT semantic correct) / QA pass
- Bootstrap confidence intervals
"""

import numpy as np


def silent_failure_gap(qa_pass: np.ndarray, semantic_correct: np.ndarray) -> float:
    return qa_pass.mean() - semantic_correct.mean()


def conditional_silent_failure_rate(
    qa_pass: np.ndarray, semantic_correct: np.ndarray
) -> float:
    qa_pass_mask = qa_pass.astype(bool)
    if qa_pass_mask.sum() == 0:
        return 0.0
    silent_failures = qa_pass_mask & ~semantic_correct.astype(bool)
    return silent_failures.sum() / qa_pass_mask.sum()


def bootstrap_ci(
    statistic_fn,
    *arrays: np.ndarray,
    n_bootstrap: int = 10000,
    ci: float = 0.95,
    seed: int = 42,
) -> tuple[float, float, float]:
    rng = np.random.default_rng(seed)
    n = len(arrays[0])
    stats = []

    for _ in range(n_bootstrap):
        idx = rng.integers(0, n, size=n)
        resampled = tuple(arr[idx] for arr in arrays)
        stats.append(statistic_fn(*resampled))

    stats = np.array(stats)
    alpha = (1 - ci) / 2
    lower = np.percentile(stats, alpha * 100)
    upper = np.percentile(stats, (1 - alpha) * 100)
    point = statistic_fn(*arrays)

    return point, lower, upper


if __name__ == "__main__":
    # Example with paper's overall results
    n = 450
    rng = np.random.default_rng(42)

    # Simulate: 78% QA pass, 54% semantic correct
    qa = (rng.random(n) < 0.78).astype(int)
    sem = (rng.random(n) < 0.54).astype(int)
    # Enforce: semantic correct implies QA pass
    sem = sem & qa

    gap, gap_lo, gap_hi = bootstrap_ci(silent_failure_gap, qa, sem)
    csfr, csfr_lo, csfr_hi = bootstrap_ci(
        conditional_silent_failure_rate, qa, sem
    )

    print(f"Silent failure gap: {gap:.1%} (95% CI: [{gap_lo:.1%}, {gap_hi:.1%}])")
    print(
        f"Conditional silent failure rate: {csfr:.1%} "
        f"(95% CI: [{csfr_lo:.1%}, {csfr_hi:.1%}])"
    )
