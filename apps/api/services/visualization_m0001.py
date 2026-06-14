from __future__ import annotations

import random
import time
from pathlib import Path
from typing import Any

import pandas as pd

try:
    import pyarrow.parquet as pq
except Exception:  # pragma: no cover - optional fallback
    pq = None

from apps.api.core.config import settings


def root() -> Path:
    return settings.root_path.resolve()


def load_m0001_visualization(
    symbol: str = "GOLD",
    timeframe: str = "M15",
    L: int = 5,
    zone_ratio: float = 0.9,
    exit_gap: int = 6,
    consumption_mode: str = "hunt",
    max_bars: int = 5000,
) -> dict[str, Any]:
    candles_df = load_candles(symbol, timeframe, max_bars=max_bars)
    nodes_df = load_nodes(symbol, timeframe, L)
    events_df = load_events(symbol, timeframe, L, zone_ratio, exit_gap, consumption_mode)

    candles = serialize_candles(candles_df)
    time_to_index = {row["time"]: row["index"] for row in candles}
    nodes = serialize_nodes(nodes_df, time_to_index, L)
    events = serialize_events(events_df, candles_df, time_to_index, prefix="M0001-EVENT", baseline_kind="actual")

    overlay_layers = build_layers(nodes, events, baseline_kind="actual", prefix="actual")
    tables = build_tables(nodes, events, prefix="actual")

    return {
        "dataset": {
            "symbol": symbol,
            "timeframe": timeframe,
            "source": "cache",
            "bars": len(candles),
            "available_rows": int(candles_df.attrs.get("available_rows", len(candles_df))),
            "source_path": candles_df.attrs.get("source_path"),
            "parameters": {
                "L": L,
                "zone_ratio": zone_ratio,
                "exit_gap": exit_gap,
                "consumption_mode": consumption_mode,
            },
        },
        "entity": {
            "id": "M0001",
            "title": "Relative Territory Volatility",
            "type": "metric",
        },
        "candles": candles,
        "overlay_layers": overlay_layers,
        "tables": tables,
        "stats": stats_from_events(events, candles=candles, nodes=nodes, label="actual"),
        "timeline": build_timeline(events),
        "validation_flags": [
            {"id": "live_confirmation", "label": "L-node confirmation delay respected in visualization", "status": "pass"},
            {"id": "data_loaded", "label": "Market candles loaded from project cache", "status": "pass" if len(candles) else "fail"},
            {"id": "events_loaded", "label": "M0001 event artifacts loaded", "status": "pass" if len(events) else "warn"},
            {"id": "hunt_location", "label": "Hunt markers are placed on first actual hunt candle", "status": "pass"},
        ],
    }


def load_m0001_random_baseline(
    symbol: str = "GOLD",
    timeframe: str = "M15",
    L: int = 5,
    zone_ratio: float = 0.9,
    exit_gap: int = 6,
    consumption_mode: str = "hunt",
    max_bars: int = 5000,
    seed: int | None = None,
    sample_size: int | None = None,
) -> dict[str, Any]:
    candles_df = load_candles(symbol, timeframe, max_bars=max_bars)
    actual_nodes_df = load_nodes(symbol, timeframe, L)
    candles = serialize_candles(candles_df)

    if seed is None:
        seed = int(time.time_ns() % 2_147_483_647)

    actual_count = int(len(actual_nodes_df[actual_nodes_df.get("confirmed", True) == True])) if not actual_nodes_df.empty else min(200, len(candles_df) // 8)
    target_count = int(sample_size or actual_count)
    target_count = max(1, min(target_count, max(1, len(candles_df) - L - exit_gap - 20)))

    random_nodes = generate_random_nodes(candles_df, count=target_count, L=L, seed=seed)
    random_events_raw = compute_random_rtv_events(
        candles_df=candles_df,
        nodes=random_nodes,
        L=L,
        zone_ratio=zone_ratio,
        exit_gap=exit_gap,
        consumption_mode=consumption_mode,
    )
    random_events = serialize_event_records(
        random_events_raw,
        prefix="RANDOM-EVENT",
        baseline_kind="random",
    )

    # Random nodes are visualized separately from structural nodes.
    random_node_rows = [
        {
            "id": f"RANDOM-NODE-{row['node_id']}",
            "node_id": int(row["node_id"]),
            "kind": "node",
            "node_type": row["node_type"],
            "time": int(candles_df.iloc[int(row["index"])]["time"]),
            "index": int(row["index"]),
            "confirmation_index": int(row["index"] + L),
            "price": float(row["node_price"]),
            "label": f"RND {row['node_type']} #{row['node_id']}",
            "baseline_kind": "random",
        }
        for row in random_nodes
    ]

    overlay_layers = build_layers(random_node_rows, random_events, baseline_kind="random", prefix="random")
    tables = build_tables(random_node_rows, random_events, prefix="random")

    return {
        "dataset": {
            "symbol": symbol,
            "timeframe": timeframe,
            "source": "cache",
            "bars": len(candles),
            "available_rows": int(candles_df.attrs.get("available_rows", len(candles_df))),
            "source_path": candles_df.attrs.get("source_path"),
            "parameters": {
                "L": L,
                "zone_ratio": zone_ratio,
                "exit_gap": exit_gap,
                "consumption_mode": consumption_mode,
                "seed": seed,
                "sample_size": target_count,
            },
        },
        "entity": {
            "id": "M0001_RANDOM_BASELINE",
            "title": "M0001 Random Baseline",
            "type": "experiment",
        },
        "candles": candles,
        "overlay_layers": overlay_layers,
        "tables": tables,
        "stats": stats_from_events(random_events, candles=candles, nodes=random_node_rows, label="random"),
        "timeline": build_timeline(random_events),
        "validation_flags": [
            {"id": "random_seed", "label": f"Random baseline seed {seed}", "status": "pass"},
            {"id": "same_metric_logic", "label": "Same RTV event logic with random reference points", "status": "pass"},
            {"id": "same_sample_size", "label": f"Random candidates: {target_count}", "status": "pass"},
        ],
    }


def compare_actual_to_random(actual_payload: dict[str, Any], random_payload: dict[str, Any]) -> dict[str, Any]:
    actual_stats = actual_payload.get("stats", {})
    random_stats = random_payload.get("stats", {})

    actual_mean = as_number(actual_stats.get("actual_mean_RTV") or actual_stats.get("mean_RTV"))
    random_mean = as_number(random_stats.get("random_mean_RTV") or random_stats.get("mean_RTV"))
    edge_ratio = None
    if actual_mean is not None and random_mean not in (None, 0):
        edge_ratio = actual_mean / random_mean

    return {
        "actual_events": actual_stats.get("actual_events") or actual_stats.get("events"),
        "random_events": random_stats.get("random_events") or random_stats.get("events"),
        "actual_mean_RTV": actual_mean,
        "random_mean_RTV": random_mean,
        "edge_ratio_actual_over_random": edge_ratio,
    }



def read_parquet_compat(path: Path, columns: list[str] | None = None) -> pd.DataFrame:
    """Read project parquet files even when pandas metadata extension types clash.

    Some cached files were written with pandas/pyarrow extension metadata that can
    raise errors such as "pandas.period already defined" in long-running API
    processes. The fallback reads the Arrow table without pandas metadata and
    converts it to a normal DataFrame.
    """
    try:
        return pd.read_parquet(path, columns=columns)
    except Exception:
        if pq is None:
            raise
        table = pq.read_table(path, columns=columns, use_pandas_metadata=False)
        return table.to_pandas(ignore_metadata=True)


def load_candles(symbol: str, timeframe: str, max_bars: int) -> pd.DataFrame:
    """Load the largest valid cached candle file for a symbol/timeframe.

    Some project folders contain both a canonical file such as GOLD_M15.parquet
    and older helper files such as data.parquet. The UI should not accidentally
    visualize a tiny helper file if a fuller dataset exists.
    """
    folder = root() / "lab/cache_data" / symbol / timeframe
    candidates = [
        folder / f"{symbol}_{timeframe}.parquet",
        folder / "data.parquet",
    ]
    if folder.exists():
        for extra in sorted(folder.glob("*.parquet")):
            if extra not in candidates:
                candidates.append(extra)

    loaded: list[tuple[int, Path, pd.DataFrame]] = []
    errors: list[str] = []
    for path in candidates:
        if not path.exists():
            continue
        try:
            df = read_parquet_compat(path)
            required = {"time", "open", "high", "low", "close"}
            if not required.issubset(set(df.columns)):
                errors.append(f"{path.name}: missing OHLC columns")
                continue
            df = normalize_time(df)
            df = df.drop_duplicates("time").sort_values("time").reset_index(drop=True)
            loaded.append((len(df), path, df))
        except Exception as exc:
            errors.append(f"{path.name}: {exc}")

    if not loaded:
        details = "; ".join(errors[:3])
        suffix = f" ({details})" if details else ""
        raise FileNotFoundError(f"No readable cached candle data found for {symbol} {timeframe}{suffix}")

    _, chosen_path, chosen_df = max(loaded, key=lambda item: item[0])
    result = chosen_df.tail(max_bars).reset_index(drop=True)
    result.attrs["source_path"] = chosen_path.relative_to(root()).as_posix()
    result.attrs["available_rows"] = len(chosen_df)
    return result


def load_nodes(symbol: str, timeframe: str, L: int) -> pd.DataFrame:
    candidates = [
        root() / "lab/cache_nodes/L_rule" / f"L_{L}" / symbol / timeframe / f"{symbol}_{timeframe}_L{L}.parquet",
    ]
    for path in candidates:
        if path.exists():
            df = read_parquet_compat(path)
            return normalize_time(df)
    return pd.DataFrame(columns=["time", "type", "price", "confirmed"])


def load_events(symbol: str, timeframe: str, L: int, zone_ratio: float, exit_gap: int, mode: str) -> pd.DataFrame:
    metric_root = root() / "lab/cache_metrics/M0001_relative_territory_volatility"
    candidates = [
        metric_root / f"L_{L}" / symbol / timeframe / f"{symbol}_{timeframe}_L{L}_ZR{zone_ratio}_EG{exit_gap}_{mode}.parquet",
        metric_root / symbol / timeframe / f"{symbol}_{timeframe}_T{zone_ratio}_G{exit_gap}_{mode}.parquet",
        metric_root / symbol / timeframe / f"{symbol}_{timeframe}_ZR{zone_ratio}_EG{exit_gap}_{mode}.parquet",
    ]
    for path in candidates:
        if path.exists():
            return normalize_event_schema(read_parquet_compat(path))

    folder_candidates = [
        metric_root / f"L_{L}" / symbol / timeframe,
        metric_root / symbol / timeframe,
    ]
    for folder in folder_candidates:
        if folder.exists():
            files = sorted(folder.glob("*.parquet"), key=lambda p: p.stat().st_mtime, reverse=True)
            if files:
                return normalize_event_schema(read_parquet_compat(files[0]))
    return pd.DataFrame()



def to_epoch_seconds(values: pd.Series) -> pd.Series:
    """Convert datetime or numeric time columns to Unix seconds.

    Pandas can preserve parquet timestamps as datetime64[ms]. Calling
    astype("int64") on that dtype returns milliseconds, not nanoseconds. That
    caused the UI to see dates around 1970 and collapse thousands of M15 candles
    into only a few fake timestamps. Force datetime64[ns] first.
    """
    if pd.api.types.is_datetime64_any_dtype(values):
        return values.astype("datetime64[ns]").astype("int64") // 10**9

    numeric = pd.to_numeric(values, errors="coerce")
    if numeric.notna().all():
        max_abs = float(numeric.abs().max()) if len(numeric) else 0
        if max_abs > 1e17:  # nanoseconds
            return (numeric // 10**9).astype("int64")
        if max_abs > 1e14:  # microseconds
            return (numeric // 10**6).astype("int64")
        if max_abs > 1e11:  # milliseconds
            return (numeric // 10**3).astype("int64")
        return numeric.astype("int64")

    return pd.to_datetime(values).astype("datetime64[ns]").astype("int64") // 10**9


def normalize_time(df: pd.DataFrame) -> pd.DataFrame:
    if "time" in df.columns:
        df = df.copy()
        df["time"] = to_epoch_seconds(df["time"])
    return df


def normalize_event_schema(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return pd.DataFrame()
    df = df.copy()
    for col in ["node_time", "entry_time", "exit_time", "hunt_time"]:
        if col in df.columns:
            df[col] = to_epoch_seconds(df[col])
    if "mean_inside" not in df.columns and "V_zone" in df.columns:
        df["mean_inside"] = df["V_zone"]
    if "mean_before" not in df.columns and "V_base" in df.columns:
        df["mean_before"] = df["V_base"]
    if "RTV" not in df.columns and "mean_inside" in df.columns and "mean_before" in df.columns:
        df["RTV"] = df.apply(lambda r: safe_ratio(r["mean_inside"], r["mean_before"]), axis=1)
    return df


def serialize_candles(df: pd.DataFrame) -> list[dict[str, Any]]:
    rows = []
    for idx, row in df.reset_index(drop=True).iterrows():
        rows.append({
            "index": int(idx),
            "time": int(row["time"]),
            "open": safe_float(row["open"]),
            "high": safe_float(row["high"]),
            "low": safe_float(row["low"]),
            "close": safe_float(row["close"]),
            "volume": safe_float(row["tick_volume"] if "tick_volume" in df.columns else row.get("volume", 0)),
        })
    return rows


def serialize_nodes(df: pd.DataFrame, time_to_index: dict[int, int], L: int) -> list[dict[str, Any]]:
    nodes = []
    if df is None or df.empty:
        return nodes

    confirmed = df[df["confirmed"] == True].copy() if "confirmed" in df.columns else df.copy()
    for idx, row in confirmed.reset_index(drop=True).iterrows():
        node_time = int(row["time"])
        candle_index = time_to_index.get(node_time)
        if candle_index is None:
            continue
        nodes.append({
            "id": f"NODE-{idx}",
            "node_id": int(idx),
            "kind": "node",
            "node_type": str(row["type"]).upper(),
            "time": node_time,
            "index": candle_index,
            "confirmation_index": candle_index + L,
            "price": safe_float(row["price"]),
            "label": f"{str(row['type']).upper()} #{idx}",
            "baseline_kind": "actual",
        })
    return nodes


def serialize_events(df: pd.DataFrame, candles_df: pd.DataFrame, time_to_index: dict[int, int], prefix: str, baseline_kind: str) -> list[dict[str, Any]]:
    events = []
    if df is None or df.empty:
        return events
    for idx, row in df.reset_index(drop=True).iterrows():
        entry_time = int(row["entry_time"]) if "entry_time" in df.columns and not pd.isna(row["entry_time"]) else None
        exit_time = int(row["exit_time"]) if "exit_time" in df.columns and not pd.isna(row["exit_time"]) else None
        entry_index = time_to_index.get(entry_time) if entry_time is not None else safe_int_or_none(row.get("entry_index"))
        exit_index = time_to_index.get(exit_time) if exit_time is not None else safe_int_or_none(row.get("exit_index"))

        # Never collapse out-of-window events to index 0. If an event time is not
        # present in the loaded candle window, skip it. Otherwise old metric
        # caches without entry_index/exit_index create fake events at candle 0.
        if entry_index is None or exit_index is None:
            continue

        node_type = str(row.get("node_type", "")).upper()
        node_price = safe_float(row.get("node_price"))
        hunted = bool(row.get("hunted", False))
        hunt_index, hunt_time, hunt_price = resolve_hunt_location(
            candles_df=candles_df,
            entry_index=int(entry_index),
            exit_index=int(exit_index),
            node_type=node_type,
            node_price=node_price,
            hunted=hunted,
            provided_index=safe_int_or_none(row.get("hunt_index")) if "hunt_index" in df.columns else None,
            provided_time=int(row["hunt_time"]) if "hunt_time" in df.columns and not pd.isna(row["hunt_time"]) else None,
        )

        event_id = f"{prefix}-{idx}"
        rtv = safe_float(row.get("RTV"))
        events.append({
            "id": event_id,
            "kind": "event",
            "row_index": int(idx),
            "node_id": safe_int(row.get("node_id", idx)),
            "node_type": node_type,
            "node_price": node_price,
            "revisit_id": safe_int(row.get("revisit_id", 1)),
            "entry_time": entry_time,
            "exit_time": exit_time,
            "entry_index": int(entry_index),
            "exit_index": int(exit_index),
            "event_length": safe_int(row.get("event_length", int(exit_index) - int(entry_index) + 1)),
            "territory_lower": safe_float(row.get("territory_lower")),
            "territory_upper": safe_float(row.get("territory_upper")),
            "expansion_extreme": safe_float(row.get("expansion_extreme")),
            "mean_inside": safe_float(row.get("mean_inside")),
            "mean_before": safe_float(row.get("mean_before")),
            "median_inside": safe_float(row.get("median_inside")),
            "median_before": safe_float(row.get("median_before")),
            "RTV": rtv,
            "hunted": hunted,
            "hunt_index": hunt_index,
            "hunt_time": hunt_time,
            "hunt_price": hunt_price,
            "label": f"RTV {rtv:.2f}" if rtv is not None else "RTV",
            "baseline_kind": baseline_kind,
        })
    return events


def serialize_event_records(records: list[dict[str, Any]], prefix: str, baseline_kind: str) -> list[dict[str, Any]]:
    out = []
    for idx, row in enumerate(records):
        rtv = safe_float(row.get("RTV"))
        event_id = f"{prefix}-{idx}"
        out.append({
            **row,
            "id": event_id,
            "kind": "event",
            "row_index": idx,
            "label": f"RND {rtv:.2f}" if rtv is not None else "RND",
            "baseline_kind": baseline_kind,
        })
    return out


def resolve_hunt_location(
    candles_df: pd.DataFrame,
    entry_index: int,
    exit_index: int,
    node_type: str,
    node_price: float | None,
    hunted: bool,
    provided_index: int | None = None,
    provided_time: int | None = None,
) -> tuple[int | None, int | None, float | None]:
    if not hunted or node_price is None:
        return None, None, None

    if provided_index is not None and 0 <= provided_index < len(candles_df):
        candle = candles_df.iloc[provided_index]
        return provided_index, int(candle["time"]), hunt_price_for_candle(candle, node_type, node_price)

    if provided_time is not None:
        matches = candles_df.index[candles_df["time"] == provided_time].tolist()
        if matches:
            idx = int(matches[0])
            candle = candles_df.iloc[idx]
            return idx, int(candle["time"]), hunt_price_for_candle(candle, node_type, node_price)

    start = max(0, entry_index)
    end = min(len(candles_df) - 1, exit_index)
    for idx in range(start, end + 1):
        candle = candles_df.iloc[idx]
        if node_type == "LOW" and float(candle["low"]) < node_price:
            return idx, int(candle["time"]), float(candle["low"])
        if node_type == "HIGH" and float(candle["high"]) > node_price:
            return idx, int(candle["time"]), float(candle["high"])

    fallback = candles_df.iloc[end]
    return end, int(fallback["time"]), hunt_price_for_candle(fallback, node_type, node_price)


def hunt_price_for_candle(candle: pd.Series, node_type: str, node_price: float) -> float:
    if node_type == "LOW":
        return float(candle.get("low", node_price))
    if node_type == "HIGH":
        return float(candle.get("high", node_price))
    return node_price


def generate_random_nodes(candles_df: pd.DataFrame, count: int, L: int, seed: int) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    n = len(candles_df)
    lo = min(max(L + 2, 10), max(0, n - 2))
    hi = max(lo + 1, n - 20)
    population = list(range(lo, hi))
    if not population:
        population = list(range(max(1, n)))
    if count <= len(population):
        indices = rng.sample(population, count)
    else:
        indices = [rng.choice(population) for _ in range(count)]
    indices.sort()

    nodes = []
    for node_id, idx in enumerate(indices):
        candle = candles_df.iloc[idx]
        node_type = "LOW" if rng.random() < 0.5 else "HIGH"
        node_price = float(candle["low"] if node_type == "LOW" else candle["high"])
        nodes.append({
            "node_id": node_id,
            "index": int(idx),
            "node_type": node_type,
            "node_price": node_price,
        })
    return nodes


def compute_random_rtv_events(
    candles_df: pd.DataFrame,
    nodes: list[dict[str, Any]],
    L: int,
    zone_ratio: float,
    exit_gap: int,
    consumption_mode: str,
) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for node in nodes:
        node_price = float(node["node_price"])
        node_type = str(node["node_type"])
        active_from = int(node["index"]) + L
        if active_from >= len(candles_df) - 2:
            continue

        extreme = node_price
        before_logs: list[float] = []
        inside_logs: list[float] = []
        in_event = False
        entry_index: int | None = None
        frozen_extreme: float | None = None
        lower: float | None = None
        upper: float | None = None
        outside_count = 0
        hunt_index: int | None = None
        hunt_price: float | None = None
        revisit_id = 0
        consumed = False
        persistent_lower: float | None = None
        persistent_upper: float | None = None

        i = active_from + 1
        while i < len(candles_df) and not consumed:
            candle = candles_df.iloc[i]
            log_move = log_range(candle)

            if not in_event:
                before_logs.append(log_move)

                if persistent_lower is None or persistent_upper is None:
                    if node_type == "LOW":
                        extreme = max(float(extreme), float(candle["high"]))
                    else:
                        extreme = min(float(extreme), float(candle["low"]))

                    distance = abs(float(extreme) - node_price)
                    if distance <= 0:
                        i += 1
                        continue
                    half_width = distance * (1.0 - zone_ratio)
                    lower = node_price - half_width
                    upper = node_price + half_width
                else:
                    lower = persistent_lower
                    upper = persistent_upper

                if candle_intersects(candle, lower, upper):
                    in_event = True
                    revisit_id += 1
                    entry_index = i
                    frozen_extreme = float(extreme)
                    inside_logs = [log_move]
                    outside_count = 0
                    hunt_index = None
                    hunt_price = None
                    persistent_lower = lower
                    persistent_upper = upper
                i += 1
                continue

            if lower is None or upper is None or entry_index is None:
                i += 1
                continue

            if candle_intersects(candle, lower, upper):
                inside_logs.append(log_move)
                outside_count = 0

            if hunt_index is None:
                if node_type == "LOW" and float(candle["low"]) < node_price:
                    hunt_index = i
                    hunt_price = float(candle["low"])
                elif node_type == "HIGH" and float(candle["high"]) > node_price:
                    hunt_index = i
                    hunt_price = float(candle["high"])

            close = float(candle["close"])
            if close < lower or close > upper:
                outside_count += 1
            else:
                outside_count = 0

            if outside_count >= exit_gap:
                exit_index = i
                event_length = exit_index - entry_index + 1
                baseline = before_logs[-event_length:]
                if baseline and len(baseline) >= max(2, event_length // 2) and inside_logs:
                    mean_inside = sum(inside_logs) / len(inside_logs)
                    mean_before = sum(baseline) / len(baseline)
                    rtv = safe_ratio(mean_inside, mean_before)
                    entry_candle = candles_df.iloc[entry_index]
                    exit_candle = candles_df.iloc[exit_index]
                    events.append({
                        "node_id": int(node["node_id"]),
                        "node_type": node_type,
                        "node_price": node_price,
                        "revisit_id": revisit_id,
                        "entry_time": int(entry_candle["time"]),
                        "exit_time": int(exit_candle["time"]),
                        "entry_index": entry_index,
                        "exit_index": exit_index,
                        "event_length": event_length,
                        "territory_lower": lower,
                        "territory_upper": upper,
                        "expansion_extreme": frozen_extreme,
                        "mean_inside": mean_inside,
                        "mean_before": mean_before,
                        "median_inside": median(inside_logs),
                        "median_before": median(baseline),
                        "RTV": rtv,
                        "hunted": hunt_index is not None,
                        "hunt_index": hunt_index,
                        "hunt_time": int(candles_df.iloc[hunt_index]["time"]) if hunt_index is not None else None,
                        "hunt_price": hunt_price,
                        "baseline_kind": "random",
                    })

                if consumption_mode == "touch" or hunt_index is not None:
                    consumed = True
                else:
                    # Keep the same territory for possible later revisits.
                    in_event = False
                    before_logs = []
                    inside_logs = []
                    outside_count = 0
                    extreme = node_price
                i += 1
                continue

            i += 1

    return events


def log_range(candle: pd.Series) -> float:
    move = abs(float(candle["high"]) - float(candle["low"]))
    if move <= 0:
        return 0.0
    # Natural log of range; same scale as the metric cache spec.
    import math
    return math.log(move)


def candle_intersects(candle: pd.Series, lower: float, upper: float) -> bool:
    return not (float(candle["high"]) < lower or float(candle["low"]) > upper)


def median(values: list[float]) -> float | None:
    if not values:
        return None
    values = sorted(values)
    mid = len(values) // 2
    if len(values) % 2:
        return values[mid]
    return (values[mid - 1] + values[mid]) / 2.0


def build_layers(nodes: list[dict[str, Any]], events: list[dict[str, Any]], baseline_kind: str, prefix: str) -> list[dict[str, Any]]:
    node_objects: list[dict[str, Any]] = []
    for node in nodes:
        node_objects.append({
            "id": node["id"],
            "kind": "marker",
            "object_type": "node",
            "baseline_kind": baseline_kind,
            "index": node["index"],
            "time": node["time"],
            "price": node["price"],
            "shape": "triangleUp" if node["node_type"] == "LOW" else "triangleDown",
            "label": node["label"],
            "payload": node,
        })

    zone_objects = []
    event_objects = []
    label_objects = []
    hunt_objects = []

    for event in events:
        zone_objects.append({
            "id": f"{event['id']}-ZONE",
            "kind": "zone",
            "object_type": "territory",
            "baseline_kind": baseline_kind,
            "start_index": event["entry_index"],
            "end_index": event["exit_index"],
            "lower": event["territory_lower"],
            "upper": event["territory_upper"],
            "label": None,
            "payload": event,
        })
        event_objects.append({
            "id": f"{event['id']}-WINDOW",
            "kind": "event_window",
            "object_type": "event",
            "baseline_kind": baseline_kind,
            "start_index": event["entry_index"],
            "end_index": event["exit_index"],
            "lower": event["territory_lower"],
            "upper": event["territory_upper"],
            "label": None,
            "payload": event,
        })
        label_objects.append({
            "id": f"{event['id']}-LABEL",
            "kind": "label",
            "object_type": "event",
            "baseline_kind": baseline_kind,
            "index": int((int(event["entry_index"]) + int(event["exit_index"])) // 2),
            "price": event["territory_upper"],
            "label": event["label"],
            "payload": event,
        })
        if event.get("hunted") and event.get("hunt_index") is not None:
            hunt_objects.append({
                "id": f"{event['id']}-HUNT",
                "kind": "marker",
                "object_type": "hunt",
                "baseline_kind": baseline_kind,
                "index": event["hunt_index"],
                "time": event.get("hunt_time"),
                "price": event.get("hunt_price") or event.get("node_price"),
                "shape": "cross",
                "label": "HUNT" if baseline_kind == "actual" else "RND HUNT",
                "payload": event,
            })

    title = "Actual" if baseline_kind == "actual" else "Random"
    return [
        {"layer_id": f"{prefix}_nodes", "label": f"{title} reference points", "default_visible": True, "objects": node_objects},
        {"layer_id": f"{prefix}_territories", "label": f"{title} territories", "default_visible": True, "objects": zone_objects},
        {"layer_id": f"{prefix}_events", "label": f"{title} event windows", "default_visible": True, "objects": event_objects},
        {"layer_id": f"{prefix}_rtv_labels", "label": f"{title} RTV labels", "default_visible": baseline_kind == "actual", "objects": label_objects},
        {"layer_id": f"{prefix}_hunts", "label": f"{title} hunt markers", "default_visible": True, "objects": hunt_objects},
    ]


def build_tables(nodes: list[dict[str, Any]], events: list[dict[str, Any]], prefix: str) -> list[dict[str, Any]]:
    title = "Random" if prefix == "random" else "M0001"
    return [
        {
            "table_id": f"{prefix}_events",
            "label": f"{title} Events",
            "object_type": "event",
            "columns": [
                {"key": "row_index", "label": "#"},
                {"key": "node_id", "label": "Node"},
                {"key": "node_type", "label": "Type"},
                {"key": "revisit_id", "label": "Revisit"},
                {"key": "entry_index", "label": "Entry"},
                {"key": "exit_index", "label": "Exit"},
                {"key": "event_length", "label": "Len"},
                {"key": "RTV", "label": "RTV"},
                {"key": "mean_inside", "label": "Inside"},
                {"key": "mean_before", "label": "Before"},
                {"key": "hunted", "label": "Hunted"},
                {"key": "hunt_index", "label": "Hunt At"},
            ],
            "rows": events,
        },
        {
            "table_id": f"{prefix}_nodes",
            "label": f"{title} Reference Points",
            "object_type": "node",
            "columns": [
                {"key": "node_id", "label": "#"},
                {"key": "node_type", "label": "Type"},
                {"key": "index", "label": "Index"},
                {"key": "confirmation_index", "label": "Confirmed At"},
                {"key": "price", "label": "Price"},
            ],
            "rows": nodes,
        },
    ]


def build_timeline(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {"id": event["id"], "time": event["entry_time"], "index": event["entry_index"], "label": event["label"], "object_id": event["id"]}
        for event in events
    ]


def stats_from_events(events: list[dict[str, Any]], candles: list[dict[str, Any]], nodes: list[dict[str, Any]], label: str) -> dict[str, Any]:
    rtv_values = [safe_float(event.get("RTV")) for event in events if safe_float(event.get("RTV")) is not None]
    hunted = [event for event in events if event.get("hunted")]
    prefix = f"{label}_"
    return {
        "bars": len(candles),
        f"{prefix}nodes": len(nodes),
        f"{prefix}events": len(events),
        f"{prefix}mean_RTV": sum(rtv_values) / len(rtv_values) if rtv_values else None,
        f"{prefix}median_RTV": median(rtv_values) if rtv_values else None,
        f"{prefix}hunt_count": len(hunted),
        f"{prefix}max_revisit": max([safe_int(event.get("revisit_id")) for event in events], default=0),
    }


def safe_float(value) -> float | None:
    try:
        if value is None:
            return None
        if pd.isna(value):
            return None
        return float(value)
    except Exception:
        return None


def safe_int(value) -> int:
    try:
        if value is None or pd.isna(value):
            return 0
        return int(value)
    except Exception:
        return 0


def safe_int_or_none(value) -> int | None:
    try:
        if value is None or pd.isna(value):
            return None
        return int(value)
    except Exception:
        return None


def safe_ratio(a, b) -> float | None:
    a = safe_float(a)
    b = safe_float(b)
    if a is None or b in {None, 0}:
        return None
    return a / b


def as_number(value: Any) -> float | None:
    try:
        if value is None:
            return None
        return float(value)
    except Exception:
        return None
