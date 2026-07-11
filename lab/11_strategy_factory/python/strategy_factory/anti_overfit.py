"""Anti-overfitting and research-selection controls.

The implementations here are deliberately transparent.  They are not a
substitute for methodological judgment, but they prevent the most common
failure modes: row-level pseudo-independence, repeated testing without trial
accounting, fragile best-trade dependence, cost sensitivity, and selection on
one historical partition.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from math import erf, exp, log, sqrt
from typing import Callable, Dict, Iterable, Mapping, Optional, Sequence, Tuple

import numpy as np
import pandas as pd


def normal_cdf(x: float) -> float:
    return 0.5 * (1.0 + erf(x / sqrt(2.0)))


def benjamini_hochberg(p_values: Sequence[float], alpha: float = 0.05) -> pd.DataFrame:
    """Benjamini-Hochberg false-discovery control with adjusted q-values."""
    values = np.asarray(p_values, dtype=float)
    if np.any((values < 0) | (values > 1)):
        raise ValueError("p-values must be within [0, 1]")
    m = len(values)
    if m == 0:
        return pd.DataFrame(columns=["index", "p_value", "q_value", "rejected"])
    order = np.argsort(values)
    ranked = values[order]
    raw_q = ranked * m / np.arange(1, m + 1)
    monotone_q = np.minimum.accumulate(raw_q[::-1])[::-1]
    monotone_q = np.clip(monotone_q, 0.0, 1.0)
    rejected_ranked = ranked <= alpha * np.arange(1, m + 1) / m
    rejected = np.zeros(m, dtype=bool)
    q_values = np.zeros(m, dtype=float)
    rejected[order] = rejected_ranked
    q_values[order] = monotone_q
    return pd.DataFrame(
        {
            "index": np.arange(m),
            "p_value": values,
            "q_value": q_values,
            "rejected": rejected,
        }
    )


def cluster_bootstrap(
    frame: pd.DataFrame,
    *,
    value_col: str,
    cluster_col: str,
    statistic: Callable[[np.ndarray], float] = np.mean,
    iterations: int = 2000,
    confidence: float = 0.95,
    random_seed: int = 7,
) -> Mapping[str, float]:
    """Bootstrap whole market-event clusters rather than individual rows."""
    if value_col not in frame or cluster_col not in frame:
        raise KeyError("value_col and cluster_col must exist")
    groups = [g[value_col].dropna().to_numpy(dtype=float) for _, g in frame.groupby(cluster_col, dropna=False)]
    groups = [g for g in groups if len(g)]
    if not groups:
        raise ValueError("no non-empty clusters")
    rng = np.random.default_rng(random_seed)
    estimates = []
    for _ in range(iterations):
        picks = rng.integers(0, len(groups), size=len(groups))
        sample = np.concatenate([groups[i] for i in picks])
        estimates.append(float(statistic(sample)))
    lower_q = (1.0 - confidence) / 2.0
    upper_q = 1.0 - lower_q
    actual = float(statistic(np.concatenate(groups)))
    return {
        "estimate": actual,
        "lower": float(np.quantile(estimates, lower_q)),
        "upper": float(np.quantile(estimates, upper_q)),
        "bootstrap_std": float(np.std(estimates, ddof=1)),
        "iterations": float(iterations),
        "cluster_count": float(len(groups)),
    }


def block_bootstrap_mean(
    values: Sequence[float],
    *,
    block_size: int,
    iterations: int = 2000,
    confidence: float = 0.95,
    random_seed: int = 7,
) -> Mapping[str, float]:
    """Moving-block bootstrap for serially dependent returns."""
    arr = np.asarray(values, dtype=float)
    n = len(arr)
    if n == 0:
        raise ValueError("values cannot be empty")
    if block_size <= 0 or block_size > n:
        raise ValueError("block_size must be in [1, len(values)]")
    starts = np.arange(0, n - block_size + 1)
    rng = np.random.default_rng(random_seed)
    estimates = []
    blocks_needed = int(np.ceil(n / block_size))
    for _ in range(iterations):
        selected = rng.choice(starts, size=blocks_needed, replace=True)
        sample = np.concatenate([arr[s : s + block_size] for s in selected])[:n]
        estimates.append(float(np.mean(sample)))
    alpha = (1.0 - confidence) / 2.0
    return {
        "estimate": float(np.mean(arr)),
        "lower": float(np.quantile(estimates, alpha)),
        "upper": float(np.quantile(estimates, 1.0 - alpha)),
        "bootstrap_std": float(np.std(estimates, ddof=1)),
    }


def permutation_test(
    observed: Sequence[float],
    comparator: Sequence[float] | None = None,
    *,
    iterations: int = 5000,
    alternative: str = "greater",
    random_seed: int = 7,
) -> Mapping[str, float]:
    """Permutation test for a mean or paired uplift."""
    x = np.asarray(observed, dtype=float)
    if comparator is None:
        differences = x
    else:
        y = np.asarray(comparator, dtype=float)
        if len(x) != len(y):
            raise ValueError("paired samples must have equal length")
        differences = x - y
    differences = differences[np.isfinite(differences)]
    if len(differences) == 0:
        raise ValueError("no finite differences")
    observed_stat = float(np.mean(differences))
    rng = np.random.default_rng(random_seed)
    permuted = np.empty(iterations, dtype=float)
    for i in range(iterations):
        signs = rng.choice((-1.0, 1.0), size=len(differences))
        permuted[i] = np.mean(differences * signs)
    if alternative == "greater":
        p = (1.0 + np.sum(permuted >= observed_stat)) / (iterations + 1.0)
    elif alternative == "less":
        p = (1.0 + np.sum(permuted <= observed_stat)) / (iterations + 1.0)
    elif alternative == "two-sided":
        p = (1.0 + np.sum(np.abs(permuted) >= abs(observed_stat))) / (iterations + 1.0)
    else:
        raise ValueError("alternative must be greater, less, or two-sided")
    return {"observed": observed_stat, "p_value": float(p), "iterations": float(iterations)}


def best_trade_removal(values: Sequence[float], fractions: Sequence[float] = (0.01, 0.05, 0.10)) -> pd.DataFrame:
    arr = np.asarray(values, dtype=float)
    arr = arr[np.isfinite(arr)]
    rows = []
    for fraction in fractions:
        remove = int(np.ceil(len(arr) * fraction))
        reduced = np.sort(arr)[: max(0, len(arr) - remove)]
        rows.append(
            {
                "removed_fraction": fraction,
                "removed_count": remove,
                "remaining_count": len(reduced),
                "mean_r": float(np.mean(reduced)) if len(reduced) else np.nan,
                "total_r": float(np.sum(reduced)) if len(reduced) else np.nan,
                "positive": bool(len(reduced) and np.mean(reduced) > 0),
            }
        )
    return pd.DataFrame(rows)


def cost_stress(values: Sequence[float], base_cost_r: Sequence[float] | float, multipliers: Sequence[float] = (1.0, 1.5, 2.0, 3.0)) -> pd.DataFrame:
    returns = np.asarray(values, dtype=float)
    costs = np.asarray(base_cost_r, dtype=float)
    if costs.ndim == 0:
        costs = np.full_like(returns, float(costs))
    if len(costs) != len(returns):
        raise ValueError("base_cost_r must be scalar or match return length")
    rows = []
    # values are assumed to already include 1x cost.  Add incremental stress.
    for multiplier in multipliers:
        stressed = returns - costs * (multiplier - 1.0)
        rows.append(
            {
                "cost_multiplier": multiplier,
                "mean_r": float(np.mean(stressed)),
                "total_r": float(np.sum(stressed)),
                "win_rate": float(np.mean(stressed > 0)),
                "positive": bool(np.mean(stressed) > 0),
            }
        )
    return pd.DataFrame(rows)


def delayed_entry_stress(
    original_r: Sequence[float],
    delayed_r_by_bars: Mapping[int, Sequence[float]],
) -> pd.DataFrame:
    base = np.asarray(original_r, dtype=float)
    rows = [
        {
            "delay_bars": 0,
            "sample_count": len(base),
            "mean_r": float(np.mean(base)),
            "total_r": float(np.sum(base)),
            "uplift_vs_base": 0.0,
        }
    ]
    base_mean = float(np.mean(base))
    for delay, values in sorted(delayed_r_by_bars.items()):
        arr = np.asarray(values, dtype=float)
        rows.append(
            {
                "delay_bars": int(delay),
                "sample_count": len(arr),
                "mean_r": float(np.mean(arr)),
                "total_r": float(np.sum(arr)),
                "uplift_vs_base": float(np.mean(arr) - base_mean),
            }
        )
    return pd.DataFrame(rows)


def probabilistic_sharpe_ratio(
    observed_sharpe: float,
    benchmark_sharpe: float,
    sample_count: int,
    skewness: float = 0.0,
    excess_kurtosis: float = 0.0,
) -> float:
    """Approximate probability that observed Sharpe exceeds a benchmark."""
    if sample_count <= 1:
        return 0.5
    denominator = sqrt(
        max(
            1e-12,
            (1.0 - skewness * observed_sharpe + ((excess_kurtosis + 2.0) / 4.0) * observed_sharpe**2)
            / (sample_count - 1),
        )
    )
    return float(normal_cdf((observed_sharpe - benchmark_sharpe) / denominator))


def expected_max_sharpe(number_of_trials: int, sharpe_std: float = 1.0) -> float:
    """Approximate expected maximum of N standard-normal Sharpe trials."""
    if number_of_trials <= 1:
        return 0.0
    # Extreme-value approximation using Euler-Mascheroni adjustment.
    gamma = 0.5772156649015329
    a = sqrt(2.0 * log(number_of_trials))
    b = a - (log(log(number_of_trials)) + log(4.0 * np.pi)) / (2.0 * a)
    return float(sharpe_std * (b + gamma / max(a, 1e-12)))


def deflated_sharpe_ratio(
    observed_sharpe: float,
    sample_count: int,
    number_of_trials: int,
    skewness: float = 0.0,
    excess_kurtosis: float = 0.0,
    trial_sharpe_std: float = 1.0,
) -> Mapping[str, float]:
    benchmark = expected_max_sharpe(number_of_trials, trial_sharpe_std)
    probability = probabilistic_sharpe_ratio(
        observed_sharpe,
        benchmark,
        sample_count,
        skewness=skewness,
        excess_kurtosis=excess_kurtosis,
    )
    return {
        "observed_sharpe": float(observed_sharpe),
        "deflation_benchmark": float(benchmark),
        "deflated_probability": float(probability),
        "number_of_trials": float(number_of_trials),
    }


def probability_of_backtest_overfitting(
    performance_matrix: np.ndarray,
    *,
    train_metric: Callable[[np.ndarray], np.ndarray] = lambda x: np.mean(x, axis=0),
    test_metric: Callable[[np.ndarray], np.ndarray] = lambda x: np.mean(x, axis=0),
    max_combinations: int = 5000,
    random_seed: int = 7,
) -> Mapping[str, float]:
    """Combinatorial symmetric cross-validation estimate of PBO.

    Rows are ordered time blocks and columns are candidate strategies/models.
    For each symmetric split, select the in-sample winner and record its
    out-of-sample rank.  PBO is the fraction whose OOS rank is below median.
    """
    matrix = np.asarray(performance_matrix, dtype=float)
    if matrix.ndim != 2 or matrix.shape[0] < 4 or matrix.shape[1] < 2:
        raise ValueError("performance_matrix requires >=4 rows and >=2 strategies")
    blocks = matrix.shape[0]
    half = blocks // 2
    all_combos = list(combinations(range(blocks), half))
    rng = np.random.default_rng(random_seed)
    if len(all_combos) > max_combinations:
        selected = rng.choice(len(all_combos), size=max_combinations, replace=False)
        all_combos = [all_combos[i] for i in selected]
    logits = []
    failures = 0
    for train_blocks in all_combos:
        train_set = set(train_blocks)
        test_blocks = [i for i in range(blocks) if i not in train_set]
        if len(test_blocks) != len(train_blocks):
            continue
        train_scores = train_metric(matrix[list(train_blocks), :])
        winner = int(np.nanargmax(train_scores))
        test_scores = test_metric(matrix[test_blocks, :])
        rank_order = np.argsort(np.argsort(test_scores))
        percentile = (rank_order[winner] + 1.0) / matrix.shape[1]
        clipped = np.clip(percentile, 1e-6, 1 - 1e-6)
        logits.append(log(clipped / (1.0 - clipped)))
        failures += int(percentile <= 0.5)
    if not logits:
        raise ValueError("no valid symmetric combinations")
    return {
        "pbo": failures / len(logits),
        "median_logit": float(np.median(logits)),
        "combination_count": float(len(logits)),
    }


def white_reality_check(
    returns_matrix: np.ndarray,
    *,
    iterations: int = 2000,
    block_size: int = 5,
    random_seed: int = 7,
) -> Mapping[str, float]:
    """Simplified block-bootstrap reality check across many candidates.

    Columns are strategies/candidates, rows are time-ordered cluster returns.
    The null centers each strategy at zero and bootstraps blocks, comparing the
    observed best mean with the distribution of the bootstrapped maximum.
    """
    matrix = np.asarray(returns_matrix, dtype=float)
    if matrix.ndim != 2 or matrix.shape[0] < 2 or matrix.shape[1] < 1:
        raise ValueError("returns_matrix must be 2D")
    n, k = matrix.shape
    centered = matrix - np.nanmean(matrix, axis=0, keepdims=True)
    observed_best = float(np.nanmax(np.nanmean(matrix, axis=0)))
    starts = np.arange(max(1, n - block_size + 1))
    blocks_needed = int(np.ceil(n / block_size))
    rng = np.random.default_rng(random_seed)
    maxima = np.empty(iterations, dtype=float)
    for i in range(iterations):
        chosen = rng.choice(starts, size=blocks_needed, replace=True)
        sample = np.concatenate([centered[s : s + block_size, :] for s in chosen], axis=0)[:n, :]
        maxima[i] = np.nanmax(np.nanmean(sample, axis=0))
    p = (1.0 + np.sum(maxima >= observed_best)) / (iterations + 1.0)
    return {
        "observed_best_mean": observed_best,
        "p_value": float(p),
        "iterations": float(iterations),
        "candidate_count": float(k),
    }


@dataclass(frozen=True)
class TrialRecord:
    trial_id: str
    family_id: str
    started_at: str
    hypothesis_hash: str
    dataset_hash: str
    feature_set_hash: str
    candidate_set_hash: str
    selection_metric: str
    result_status: str


class TrialRegistry:
    """Immutable in-memory registry used to count the true research search surface."""

    def __init__(self) -> None:
        self._records: Dict[str, TrialRecord] = {}

    def register(self, record: TrialRecord) -> None:
        if record.trial_id in self._records:
            raise ValueError(f"duplicate trial_id: {record.trial_id}")
        self._records[record.trial_id] = record

    def count(self, family_id: Optional[str] = None) -> int:
        if family_id is None:
            return len(self._records)
        return sum(record.family_id == family_id for record in self._records.values())

    def records(self) -> Sequence[TrialRecord]:
        return tuple(self._records.values())
