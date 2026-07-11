"""Purged and embargoed time-series splitters."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator, Sequence, Tuple

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class Fold:
    fold_id: int
    train_index: np.ndarray
    test_index: np.ndarray
    train_start: pd.Timestamp
    train_end: pd.Timestamp
    test_start: pd.Timestamp
    test_end: pd.Timestamp


class PurgedWalkForwardSplitter:
    """Anchored or rolling walk-forward with label-horizon purge and embargo."""

    def __init__(
        self,
        n_splits: int = 5,
        test_size: int | None = None,
        min_train_size: int | None = None,
        embargo: pd.Timedelta | str = "0s",
        rolling_train_size: int | None = None,
    ) -> None:
        if n_splits <= 0:
            raise ValueError("n_splits must be positive")
        self.n_splits = n_splits
        self.test_size = test_size
        self.min_train_size = min_train_size
        self.embargo = pd.Timedelta(embargo)
        self.rolling_train_size = rolling_train_size

    def split(
        self,
        frame: pd.DataFrame,
        *,
        time_col: str = "known_time_utc",
        label_end_col: str = "label_end_time_utc",
        cluster_col: str | None = "market_event_cluster_id",
    ) -> Iterator[Fold]:
        if time_col not in frame or label_end_col not in frame:
            raise KeyError(f"frame requires {time_col} and {label_end_col}")
        work = frame.copy()
        work[time_col] = pd.to_datetime(work[time_col], utc=True)
        work[label_end_col] = pd.to_datetime(work[label_end_col], utc=True)
        work["__row_index"] = np.arange(len(work))
        work = work.sort_values(time_col, kind="stable").reset_index(drop=True)

        if cluster_col and cluster_col in work.columns:
            cluster_times = (
                work.groupby(cluster_col, dropna=False)[time_col]
                .min()
                .sort_values(kind="stable")
            )
            units = cluster_times.index.tolist()
            unit_count = len(units)
            test_size = self.test_size or max(1, unit_count // (self.n_splits + 1))
            min_train = self.min_train_size or max(test_size, unit_count - self.n_splits * test_size)
            for fold_id in range(self.n_splits):
                test_begin = min_train + fold_id * test_size
                test_units = units[test_begin : test_begin + test_size]
                if not test_units:
                    break
                test_mask = work[cluster_col].isin(test_units)
                test_start = work.loc[test_mask, time_col].min()
                test_end = work.loc[test_mask, time_col].max()
                train_mask = work[time_col] < test_start
                # Purge any training observation whose outcome reaches test start.
                train_mask &= work[label_end_col] < test_start
                # Embargo observations immediately adjacent to the test boundary.
                train_mask &= work[time_col] < (test_start - self.embargo)
                if self.rolling_train_size is not None:
                    candidate_positions = np.flatnonzero(train_mask.to_numpy())
                    keep = candidate_positions[-self.rolling_train_size :]
                    rolling_mask = np.zeros(len(work), dtype=bool)
                    rolling_mask[keep] = True
                    train_mask = pd.Series(rolling_mask, index=work.index)
                train_idx = work.loc[train_mask, "__row_index"].to_numpy(dtype=int)
                test_idx = work.loc[test_mask, "__row_index"].to_numpy(dtype=int)
                if len(train_idx) == 0 or len(test_idx) == 0:
                    continue
                yield Fold(
                    fold_id=fold_id,
                    train_index=train_idx,
                    test_index=test_idx,
                    train_start=work.loc[train_mask, time_col].min(),
                    train_end=work.loc[train_mask, time_col].max(),
                    test_start=test_start,
                    test_end=test_end,
                )
        else:
            count = len(work)
            test_size = self.test_size or max(1, count // (self.n_splits + 1))
            min_train = self.min_train_size or max(test_size, count - self.n_splits * test_size)
            for fold_id in range(self.n_splits):
                test_begin = min_train + fold_id * test_size
                test_end_pos = min(count, test_begin + test_size)
                if test_begin >= count:
                    break
                test_slice = work.iloc[test_begin:test_end_pos]
                test_start = test_slice[time_col].min()
                test_end = test_slice[time_col].max()
                train_mask = (work[time_col] < test_start) & (work[label_end_col] < test_start)
                train_mask &= work[time_col] < (test_start - self.embargo)
                if self.rolling_train_size is not None:
                    candidate_positions = np.flatnonzero(train_mask.to_numpy())
                    keep = candidate_positions[-self.rolling_train_size :]
                    rolling_mask = np.zeros(len(work), dtype=bool)
                    rolling_mask[keep] = True
                    train_mask = pd.Series(rolling_mask, index=work.index)
                train_idx = work.loc[train_mask, "__row_index"].to_numpy(dtype=int)
                test_idx = test_slice["__row_index"].to_numpy(dtype=int)
                if len(train_idx) == 0 or len(test_idx) == 0:
                    continue
                yield Fold(
                    fold_id=fold_id,
                    train_index=train_idx,
                    test_index=test_idx,
                    train_start=work.loc[train_mask, time_col].min(),
                    train_end=work.loc[train_mask, time_col].max(),
                    test_start=test_start,
                    test_end=test_end,
                )
