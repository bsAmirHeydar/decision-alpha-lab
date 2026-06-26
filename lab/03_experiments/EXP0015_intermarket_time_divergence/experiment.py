"""EXP0015 Intermarket Candle + Session Divergence.

Backtest/research runner for two-symbol divergence using candle references and
session references. It is source-agnostic: broker export, CME historical export,
Databento/vendor export, or bridge-updated CSV all work once normalized to:

    time,open,high,low,close,volume

Example:
    python lab/03_experiments/EXP0015_intermarket_time_divergence/experiment.py \
      --a data/cme/bars/ES_M1.csv --b data/cme/bars/NQ_M1.csv \
      --symbol-a ES --symbol-b NQ --level-family current_session \
      --output-dir lab/03_experiments/EXP0015_intermarket_time_divergence/out
"""
from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal

import pandas as pd

Side = Literal["HIGH", "LOW"]
Bias = Literal["BUY", "SELL"]
LevelFamily = Literal["previous_candle", "rolling", "current_session", "previous_session"]
TriggerMode = Literal["wick_touch", "close_break", "hunt_reject_close"]


@dataclass
class DivergenceEvent:
    event_id: int
    pair_label: str
    origin_symbol: str
    destination_symbol: str
    bar_index: int
    evaluation_time: str
    valid_from_time: str
    valid_until_time: str
    side: str
    suggested_bias: str
    level_family: str
    trigger_mode: str
    step_every_bars: int
    step_offset_bars: int
    destination_lag_bars: int
    signal_valid_bars: int
    origin_ref_price: float
    destination_ref_price: float
    origin_ref_time: str
    destination_ref_time: str
    origin_ref_index: int
    destination_ref_index: int
    origin_break_points: float
    destination_break_points: float
    divergence_gap_points: float
    destination_late_confirmed: bool
    destination_confirm_time: str
    entry_close: float
    mfe_points: float
    mae_points: float
    return_points: float
    bars_to_mfe: int
    bars_to_mae: int
    note: str


def load_bars(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    time_col = "time"
    if time_col not in df.columns:
        for candidate in ("time_utc", "datetime", "date"):
            if candidate in df.columns:
                time_col = candidate
                break
    required = {time_col, "open", "high", "low", "close"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"{path} missing columns: {sorted(missing)}")
    if "volume" not in df.columns:
        df["volume"] = 0
    df = df.rename(columns={time_col: "time"}).copy()
    df["time"] = pd.to_datetime(df["time"], utc=False)
    for col in ["open", "high", "low", "close", "volume"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["time", "open", "high", "low", "close"]).sort_values("time")
    df = df.drop_duplicates(subset=["time"], keep="last").reset_index(drop=True)
    return df[["time", "open", "high", "low", "close", "volume"]]


def align(a: pd.DataFrame, b: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    merged = a[["time"]].merge(b[["time"]], on="time", how="inner")
    a2 = merged.merge(a, on="time", how="left")
    b2 = merged.merge(b, on="time", how="left")
    return a2.reset_index(drop=True), b2.reset_index(drop=True)


def minute_of_day(ts: pd.Timestamp) -> int:
    return int(ts.hour) * 60 + int(ts.minute)


def in_session(ts: pd.Timestamp, start_minute: int, end_minute: int) -> bool:
    m = minute_of_day(ts)
    if start_minute == end_minute:
        return True
    if start_minute < end_minute:
        return start_minute <= m < end_minute
    return m >= start_minute or m < end_minute


def ref_levels(
    df: pd.DataFrame,
    i: int,
    family: LevelFamily,
    rolling: int,
    session_start: int,
    session_end: int,
) -> dict | None:
    if i <= 0 or i >= len(df):
        return None
    if family == "previous_candle":
        j = i - 1
        return {"high": df.at[j, "high"], "low": df.at[j, "low"], "high_i": j, "low_i": j,
                "high_time": df.at[j, "time"], "low_time": df.at[j, "time"]}
    if family == "rolling":
        start = max(0, i - max(1, rolling))
        w = df.iloc[start:i]
        if w.empty:
            return None
        hi_i = int(w["high"].idxmax())
        lo_i = int(w["low"].idxmin())
        return {"high": df.at[hi_i, "high"], "low": df.at[lo_i, "low"], "high_i": hi_i, "low_i": lo_i,
                "high_time": df.at[hi_i, "time"], "low_time": df.at[lo_i, "time"]}
    if family == "current_session":
        day = df.at[i, "time"].date()
        mask = [False] * i
        for k in range(i):
            ts = df.at[k, "time"]
            mask[k] = ts.date() == day and in_session(ts, session_start, session_end)
        w = df.iloc[:i][mask]
        if w.empty:
            return None
        hi_i = int(w["high"].idxmax())
        lo_i = int(w["low"].idxmin())
        return {"high": df.at[hi_i, "high"], "low": df.at[lo_i, "low"], "high_i": hi_i, "low_i": lo_i,
                "high_time": df.at[hi_i, "time"], "low_time": df.at[lo_i, "time"]}
    if family == "previous_session":
        current_day = df.at[i, "time"].date()
        prev_days = []
        for k in range(i):
            ts = df.at[k, "time"]
            if ts.date() != current_day and in_session(ts, session_start, session_end):
                prev_days.append(ts.date())
        if not prev_days:
            return None
        prev_day = prev_days[-1]
        mask = []
        for k in range(i):
            ts = df.at[k, "time"]
            mask.append(ts.date() == prev_day and in_session(ts, session_start, session_end))
        w = df.iloc[:i][mask]
        if w.empty:
            return None
        hi_i = int(w["high"].idxmax())
        lo_i = int(w["low"].idxmin())
        return {"high": df.at[hi_i, "high"], "low": df.at[lo_i, "low"], "high_i": hi_i, "low_i": lo_i,
                "high_time": df.at[hi_i, "time"], "low_time": df.at[lo_i, "time"]}
    raise ValueError(f"unknown level family: {family}")


def triggered(row: pd.Series, side: Side, mode: TriggerMode, level: float) -> tuple[bool, float]:
    if side == "HIGH":
        if mode == "wick_touch" and row.high >= level:
            return True, float(row.high - level)
        if mode == "close_break" and row.close > level:
            return True, float(row.close - level)
        if mode == "hunt_reject_close" and row.high >= level and row.close < level:
            return True, float(row.high - level)
    else:
        if mode == "wick_touch" and row.low <= level:
            return True, float(level - row.low)
        if mode == "close_break" and row.close < level:
            return True, float(level - row.close)
        if mode == "hunt_reject_close" and row.low <= level and row.close > level:
            return True, float(level - row.low)
    return False, 0.0


def outcome(df: pd.DataFrame, start: int, horizon: int, bias: Bias) -> dict:
    end = min(len(df) - 1, start + max(1, horizon))
    entry = float(df.at[start, "close"])
    best_mfe = best_mae = 0.0
    bars_to_mfe = bars_to_mae = 0
    for k in range(start, end + 1):
        if bias == "BUY":
            mfe = float(df.at[k, "high"] - entry)
            mae = float(entry - df.at[k, "low"])
        else:
            mfe = float(entry - df.at[k, "low"])
            mae = float(df.at[k, "high"] - entry)
        if mfe > best_mfe:
            best_mfe, bars_to_mfe = mfe, k - start
        if mae > best_mae:
            best_mae, bars_to_mae = mae, k - start
    ret = float(df.at[end, "close"] - entry) if bias == "BUY" else float(entry - df.at[end, "close"])
    return {"entry_close": entry, "mfe_points": best_mfe, "mae_points": best_mae,
            "return_points": ret, "bars_to_mfe": bars_to_mfe, "bars_to_mae": bars_to_mae}


def detect_origin_destination(
    pair_label: str,
    origin_symbol: str,
    destination_symbol: str,
    origin: pd.DataFrame,
    destination: pd.DataFrame,
    level_family: LevelFamily,
    trigger_mode: TriggerMode,
    rolling: int,
    session_start: int,
    session_end: int,
    step_every: int,
    step_offset: int,
    lag_bars: int,
    valid_bars: int,
    start_after: int,
    outcome_horizon: int,
    start_id: int,
) -> list[DivergenceEvent]:
    events: list[DivergenceEvent] = []
    n = min(len(origin), len(destination))
    for i in range(max(1, start_after), n - lag_bars):
        if (i - step_offset) % max(1, step_every) != 0:
            continue
        ol = ref_levels(origin, i, level_family, rolling, session_start, session_end)
        dl = ref_levels(destination, i, level_family, rolling, session_start, session_end)
        if not ol or not dl:
            continue
        for side in ("HIGH", "LOW"):
            origin_level = float(ol["high"] if side == "HIGH" else ol["low"])
            dest_level = float(dl["high"] if side == "HIGH" else dl["low"])
            origin_hit, obp = triggered(origin.iloc[i], side, trigger_mode, origin_level)
            if not origin_hit:
                continue
            dest_hit = False
            dest_bp = 0.0
            for j in range(i, min(n, i + lag_bars + 1)):
                dest_hit, dest_bp = triggered(destination.iloc[j], side, trigger_mode, dest_level)
                if dest_hit:
                    break
            if dest_hit:
                continue
            valid_from = min(n - 1, i + lag_bars)
            valid_until = min(n - 1, valid_from + max(1, valid_bars))
            bias: Bias = "SELL" if side == "HIGH" else "BUY"
            late = False
            late_time = ""
            for j in range(valid_from + 1, valid_until + 1):
                late, _ = triggered(destination.iloc[j], side, trigger_mode, dest_level)
                if late:
                    late_time = str(destination.at[j, "time"])
                    break
            out = outcome(origin, valid_from, outcome_horizon, bias)
            evt = DivergenceEvent(
                event_id=start_id + len(events), pair_label=pair_label,
                origin_symbol=origin_symbol, destination_symbol=destination_symbol,
                bar_index=i, evaluation_time=str(origin.at[i, "time"]),
                valid_from_time=str(origin.at[valid_from, "time"]),
                valid_until_time=str(origin.at[valid_until, "time"]),
                side=f"{side}_DIVERGENCE", suggested_bias=bias,
                level_family=level_family, trigger_mode=trigger_mode,
                step_every_bars=step_every, step_offset_bars=step_offset,
                destination_lag_bars=lag_bars, signal_valid_bars=valid_bars,
                origin_ref_price=origin_level, destination_ref_price=dest_level,
                origin_ref_time=str(ol["high_time"] if side == "HIGH" else ol["low_time"]),
                destination_ref_time=str(dl["high_time"] if side == "HIGH" else dl["low_time"]),
                origin_ref_index=int(ol["high_i"] if side == "HIGH" else ol["low_i"]),
                destination_ref_index=int(dl["high_i"] if side == "HIGH" else dl["low_i"]),
                origin_break_points=obp, destination_break_points=dest_bp,
                divergence_gap_points=abs(origin_level - dest_level),
                destination_late_confirmed=late, destination_confirm_time=late_time,
                note="origin took reference; destination failed inside lag",
                **out,
            )
            events.append(evt)
    return events


def run(args: argparse.Namespace) -> None:
    a = load_bars(Path(args.a))
    b = load_bars(Path(args.b))
    a, b = align(a, b)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    events: list[DivergenceEvent] = []
    if args.scan_a_as_origin:
        events.extend(detect_origin_destination(args.pair_label, args.symbol_a, args.symbol_b, a, b,
                                                args.level_family, args.trigger_mode, args.rolling_lookback,
                                                args.session_start_minute, args.session_end_minute,
                                                args.step_every_bars, args.step_offset_bars,
                                                args.destination_lag_bars, args.signal_valid_bars,
                                                args.start_after_bars, args.outcome_horizon_bars,
                                                len(events) + 1))
    if args.scan_b_as_origin:
        events.extend(detect_origin_destination(args.pair_label, args.symbol_b, args.symbol_a, b, a,
                                                args.level_family, args.trigger_mode, args.rolling_lookback,
                                                args.session_start_minute, args.session_end_minute,
                                                args.step_every_bars, args.step_offset_bars,
                                                args.destination_lag_bars, args.signal_valid_bars,
                                                args.start_after_bars, args.outcome_horizon_bars,
                                                len(events) + 1))
    events_df = pd.DataFrame([asdict(e) for e in events])
    events_path = out_dir / "imd001_divergence_events.csv"
    events_df.to_csv(events_path, index=False)
    summary = {
        "pair_label": args.pair_label,
        "symbol_a": args.symbol_a,
        "symbol_b": args.symbol_b,
        "aligned_bars": len(a),
        "events": len(events),
        "high_divergences": int((events_df["side"] == "HIGH_DIVERGENCE").sum()) if not events_df.empty else 0,
        "low_divergences": int((events_df["side"] == "LOW_DIVERGENCE").sum()) if not events_df.empty else 0,
        "buy_bias": int((events_df["suggested_bias"] == "BUY").sum()) if not events_df.empty else 0,
        "sell_bias": int((events_df["suggested_bias"] == "SELL").sum()) if not events_df.empty else 0,
        "late_destination_confirms": int(events_df["destination_late_confirmed"].sum()) if not events_df.empty else 0,
        "mean_mfe_points": float(events_df["mfe_points"].mean()) if not events_df.empty else 0.0,
        "mean_mae_points": float(events_df["mae_points"].mean()) if not events_df.empty else 0.0,
        "mean_return_points": float(events_df["return_points"].mean()) if not events_df.empty else 0.0,
    }
    (out_dir / "imd001_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    pd.DataFrame([summary]).to_csv(out_dir / "imd001_summary.csv", index=False)
    print(json.dumps(summary, indent=2))
    print("events:", events_path)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--a", required=True, help="CSV for symbol A")
    p.add_argument("--b", required=True, help="CSV for symbol B")
    p.add_argument("--symbol-a", default="ES")
    p.add_argument("--symbol-b", default="NQ")
    p.add_argument("--pair-label", default="ES_NQ")
    p.add_argument("--output-dir", default="lab/03_experiments/EXP0015_intermarket_time_divergence/out")
    p.add_argument("--level-family", choices=["previous_candle", "rolling", "current_session", "previous_session"], default="current_session")
    p.add_argument("--trigger-mode", choices=["wick_touch", "close_break", "hunt_reject_close"], default="wick_touch")
    p.add_argument("--rolling-lookback", type=int, default=20)
    p.add_argument("--session-start-minute", type=int, default=570)
    p.add_argument("--session-end-minute", type=int, default=960)
    p.add_argument("--step-every-bars", type=int, default=1)
    p.add_argument("--step-offset-bars", type=int, default=0)
    p.add_argument("--destination-lag-bars", type=int, default=2)
    p.add_argument("--signal-valid-bars", type=int, default=12)
    p.add_argument("--start-after-bars", type=int, default=100)
    p.add_argument("--outcome-horizon-bars", type=int, default=12)
    p.add_argument("--scan-a-as-origin", action=argparse.BooleanOptionalAction, default=True)
    p.add_argument("--scan-b-as-origin", action=argparse.BooleanOptionalAction, default=True)
    return p.parse_args()


if __name__ == "__main__":
    run(parse_args())
