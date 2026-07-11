import numpy as np
import pandas as pd

from strategy_factory.anti_overfit import (
    benjamini_hochberg,
    best_trade_removal,
    cluster_bootstrap,
    cost_stress,
    probability_of_backtest_overfitting,
    white_reality_check,
)


def test_bh_q_values_are_monotone_in_ranked_space():
    result = benjamini_hochberg([0.001, 0.01, 0.20, 0.9], alpha=0.05)
    ranked = result.sort_values("p_value")
    assert np.all(np.diff(ranked["q_value"]) >= -1e-12)
    assert result.loc[0, "rejected"]


def test_cluster_bootstrap_returns_interval():
    frame = pd.DataFrame({"cluster": ["a", "a", "b", "b", "c", "c"], "r": [1, 0, -1, 0, 2, 1]})
    result = cluster_bootstrap(frame, value_col="r", cluster_col="cluster", iterations=100)
    assert result["lower"] <= result["estimate"] <= result["upper"]


def test_fragility_stresses_execute():
    removal = best_trade_removal([1, 1, 1, 10], fractions=[0.25])
    assert removal.iloc[0]["remaining_count"] == 3
    stress = cost_stress([0.2, 0.3], [0.1, 0.1], multipliers=[1, 2])
    assert stress.iloc[1]["mean_r"] < stress.iloc[0]["mean_r"]


def test_pbo_and_reality_check_return_probabilities():
    matrix = np.array(
        [
            [0.1, 0.0, -0.1],
            [0.2, 0.1, 0.0],
            [-0.1, 0.2, 0.1],
            [0.3, -0.1, 0.0],
            [0.0, 0.1, 0.2],
            [0.1, 0.0, -0.2],
        ]
    )
    pbo = probability_of_backtest_overfitting(matrix)
    reality = white_reality_check(matrix, iterations=100, block_size=2)
    assert 0 <= pbo["pbo"] <= 1
    assert 0 <= reality["p_value"] <= 1
