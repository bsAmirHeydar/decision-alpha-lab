"""Standard statistical pack for every strategy and candidate family."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Dict, Iterable, Mapping, Optional, Sequence
import math

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class PerformanceSummary:
    sample_count: int
    filled_count: int
    fill_rate: float
    win_rate: float
    loss_rate: float
    average_win_r: float
    average_loss_r: float
    expectancy_r: float
    median_r: float
    std_r: float
    profit_factor: float
    total_r: float
    max_drawdown_r: float
    sharpe_like: float
    average_mfe_r: float
    average_mae_r: float
    average_holding_seconds: float
    tail_share: float
    best_trade_share: float

    def to_dict(self) -> Dict[str, float | int]:
        return asdict(self)


def max_drawdown(values: Sequence[float]) -> float:
    if not values:
        return 0.0
    curve = np.cumsum(np.asarray(values, dtype=float))
    peaks = np.maximum.accumulate(np.concatenate(([0.0], curve)))
    extended = np.concatenate(([0.0], curve))
    drawdowns = extended - peaks
    return float(abs(np.min(drawdowns)))


def summarize(frame: pd.DataFrame, *, return_col: str = "net_r", filled_col: str = "filled") -> PerformanceSummary:
    if return_col not in frame.columns:
        raise KeyError(return_col)
    sample_count = len(frame)
    if sample_count == 0:
        return PerformanceSummary(
            sample_count=0, filled_count=0, fill_rate=0.0, win_rate=0.0, loss_rate=0.0,
            average_win_r=0.0, average_loss_r=0.0, expectancy_r=0.0, median_r=0.0,
            std_r=0.0, profit_factor=0.0, total_r=0.0, max_drawdown_r=0.0,
            sharpe_like=0.0, average_mfe_r=0.0, average_mae_r=0.0,
            average_holding_seconds=0.0, tail_share=0.0, best_trade_share=0.0,
        )
    filled_mask = frame[filled_col].astype(bool) if filled_col in frame.columns else pd.Series(True, index=frame.index)
    filled = frame.loc[filled_mask].copy()
    values = filled[return_col].astype(float).replace([np.inf, -np.inf], np.nan).dropna()
    filled_count = len(values)
    if filled_count == 0:
        return PerformanceSummary(
            sample_count=sample_count,
            filled_count=0,
            fill_rate=0.0,
            win_rate=0.0,
            loss_rate=0.0,
            average_win_r=0.0,
            average_loss_r=0.0,
            expectancy_r=0.0,
            median_r=0.0,
            std_r=0.0,
            profit_factor=0.0,
            total_r=0.0,
            max_drawdown_r=0.0,
            sharpe_like=0.0,
            average_mfe_r=0.0,
            average_mae_r=0.0,
            average_holding_seconds=0.0,
            tail_share=0.0,
            best_trade_share=0.0,
        )
    wins = values[values > 0]
    losses = values[values < 0]
    gross_profit = float(wins.sum())
    gross_loss = abs(float(losses.sum()))
    total = float(values.sum())
    std = float(values.std(ddof=1)) if filled_count > 1 else 0.0
    sharpe_like = float(values.mean() / std * math.sqrt(filled_count)) if std > 0 else 0.0
    tail_threshold = float(values.quantile(0.95)) if filled_count >= 20 else float(values.max())
    tail_profit = float(values[values >= tail_threshold].clip(lower=0).sum())
    positive_total = max(gross_profit, 1e-12)
    best_trade = max(float(values.max()), 0.0)
    return PerformanceSummary(
        sample_count=sample_count,
        filled_count=filled_count,
        fill_rate=filled_count / sample_count,
        win_rate=len(wins) / filled_count,
        loss_rate=len(losses) / filled_count,
        average_win_r=float(wins.mean()) if len(wins) else 0.0,
        average_loss_r=float(losses.mean()) if len(losses) else 0.0,
        expectancy_r=float(values.mean()),
        median_r=float(values.median()),
        std_r=std,
        profit_factor=(gross_profit / gross_loss) if gross_loss > 0 else (math.inf if gross_profit > 0 else 0.0),
        total_r=total,
        max_drawdown_r=max_drawdown(values.tolist()),
        sharpe_like=sharpe_like,
        average_mfe_r=float(filled["mfe_r"].mean()) if "mfe_r" in filled else 0.0,
        average_mae_r=float(filled["mae_r"].mean()) if "mae_r" in filled else 0.0,
        average_holding_seconds=float(filled["holding_seconds"].mean()) if "holding_seconds" in filled else 0.0,
        tail_share=tail_profit / positive_total,
        best_trade_share=best_trade / positive_total,
    )


def grouped_summary(
    frame: pd.DataFrame,
    group_cols: Sequence[str],
    *,
    return_col: str = "net_r",
    minimum_samples: int = 1,
) -> pd.DataFrame:
    missing = [col for col in group_cols if col not in frame.columns]
    if missing:
        raise KeyError(f"missing group columns: {missing}")
    rows = []
    for keys, group in frame.groupby(list(group_cols), dropna=False, sort=True):
        if len(group) < minimum_samples:
            continue
        summary = summarize(group, return_col=return_col).to_dict()
        if not isinstance(keys, tuple):
            keys = (keys,)
        row = dict(zip(group_cols, keys))
        row.update(summary)
        rows.append(row)
    return pd.DataFrame(rows)


def distribution_quantiles(values: Iterable[float], quantiles: Optional[Sequence[float]] = None) -> Mapping[str, float]:
    series = pd.Series(list(values), dtype=float).dropna()
    if series.empty:
        return {}
    quantiles = quantiles or (0.01, 0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99)
    return {f"q{int(q * 100):02d}": float(series.quantile(q)) for q in quantiles}
