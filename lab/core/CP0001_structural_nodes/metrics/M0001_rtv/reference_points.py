from __future__ import annotations

import random
from typing import Iterable

import pandas as pd

from .schemas import ReferencePoint


def reference_points_from_lrule_nodes(nodes_df: pd.DataFrame, candles_df: pd.DataFrame, L: int) -> list[ReferencePoint]:
    if nodes_df is None or nodes_df.empty:
        return []

    required = {"time", "type", "price", "confirmed"}
    missing = required.difference(nodes_df.columns)
    if missing:
        raise ValueError(f"nodes_df missing columns: {sorted(missing)}")

    time_to_index = {pd.Timestamp(time): int(i) for i, time in enumerate(candles_df["time"])}
    confirmed = nodes_df[nodes_df["confirmed"] == True].copy().sort_values("time").reset_index(drop=True)

    refs: list[ReferencePoint] = []
    for ref_id, row in confirmed.iterrows():
        ts = pd.Timestamp(row["time"])
        index = time_to_index.get(ts)
        if index is None:
            continue
        confirmation_index = int(index) + int(L)
        if confirmation_index >= len(candles_df):
            continue
        ref_type = str(row["type"]).upper()
        if ref_type not in {"LOW", "HIGH"}:
            continue
        refs.append(
            ReferencePoint(
                ref_id=int(ref_id),
                time=row["time"],
                index=int(index),
                ref_type=ref_type,
                price=float(row["price"]),
                confirmed=True,
                active_from_index=confirmation_index,
                baseline_kind="actual",
            )
        )
    return refs


def random_reference_points(
    candles_df: pd.DataFrame,
    count: int,
    L: int,
    seed: int | None = None,
    start_padding: int | None = None,
    end_padding: int | None = None,
) -> list[ReferencePoint]:
    if candles_df is None or candles_df.empty:
        return []

    rng = random.Random(seed)
    start_padding = int(start_padding if start_padding is not None else L + 5)
    end_padding = int(end_padding if end_padding is not None else L + 10)
    first = max(0, start_padding)
    last = max(first, len(candles_df) - end_padding - 1)
    candidates = list(range(first, last + 1))
    if not candidates:
        return []

    count = max(1, min(int(count), len(candidates)))
    sampled = sorted(rng.sample(candidates, count))

    refs: list[ReferencePoint] = []
    for ref_id, index in enumerate(sampled):
        candle = candles_df.iloc[index]
        ref_type = "LOW" if rng.random() < 0.5 else "HIGH"
        price = float(candle["low"] if ref_type == "LOW" else candle["high"])
        refs.append(
            ReferencePoint(
                ref_id=int(ref_id),
                time=candle["time"],
                index=int(index),
                ref_type=ref_type,
                price=price,
                confirmed=True,
                active_from_index=int(index) + int(L),
                baseline_kind="random",
            )
        )
    return refs
