from __future__ import annotations

import argparse
import shutil
import sys
import time
from dataclasses import asdict
from pathlib import Path
from types import SimpleNamespace

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools.export_m0001_to_mql import (
    DataFrameEngine,
    _Timeframe,
    default_output_path,
    load_cached_candles,
)
from lab.core.CP0001_structural_nodes.metrics.M0001_rtv.time_utils import normalize_ohlc
from lab.core.CP0001_structural_nodes.detectors.L_Rule import LRuleNodeDetector
from lab.core.CP0001_structural_nodes.metrics.M0001_rtv import (
    RTVConfig,
    build_visual_rows,
    compute_rtv_events,
    random_reference_points,
    reference_points_from_lrule_nodes,
    write_visual_csv,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Run the Python single-source M0001 engine and export a visual contract for MT5. "
            "Parquet is the Python-side artifact format. CSV is only a thin MQL render adapter."
        )
    )
    parser.add_argument("--symbol", default="GOLD")
    parser.add_argument("--timeframe", default="M15")
    parser.add_argument("--bars", type=int, default=1200)
    parser.add_argument("--L", type=int, default=5)
    parser.add_argument("--zone-ratio", type=float, default=0.9)
    parser.add_argument("--exit-gap", type=int, default=6)
    parser.add_argument("--mode", choices=["hunt", "touch"], default="hunt")
    parser.add_argument("--random", action="store_true")
    parser.add_argument("--random-count", type=int, default=None)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--output", default=None)
    parser.add_argument("--terminal-files-output", default=None, help="Optional absolute MT5 MQL5/Files output path.")
    parser.add_argument("--terminal-files-root", default=None, help="MT5 MQL5/Files root. Used with --mql-config relative output.")
    parser.add_argument("--mql-config", default=None, help="MQL-written key=value runtime config file.")
    parser.add_argument("--wait-for-config", action="store_true", help="Wait until --mql-config exists before computing.")
    parser.add_argument("--artifact-root", default=None, help="Optional parquet artifact directory.")
    parser.add_argument("--interval", type=float, default=2.0)
    parser.add_argument("--once", action="store_true")
    args = parser.parse_args()

    announced_wait = False
    runtime = None
    last_input_signature = None

    while True:
        try:
            runtime, config_meta = resolve_runtime_args(args)
            if runtime is None:
                if not announced_wait:
                    print(f"Waiting for MQL input config: {args.mql_config}")
                    announced_wait = True
                if args.once:
                    return 2
                time.sleep(max(0.05, float(args.interval)))
                continue

            input_signature = runtime_input_signature(runtime, args)
            if not args.once and input_signature == last_input_signature:
                time.sleep(max(0.05, float(runtime.interval)))
                continue
            last_input_signature = input_signature

            result = build_contract(runtime)
            rows = result.rows
            stats = result.stats

            parquet_paths = write_parquet_artifacts(runtime, result)

            # MQL5 cannot read Parquet natively. This CSV is only the render adapter
            # consumed by the MQL visual terminal; it is not the research artifact.
            output_path = write_visual_adapter_with_retries(runtime.output_path, rows)

            terminal_path = None
            if runtime.terminal_output_path:
                terminal_path = Path(runtime.terminal_output_path)
                terminal_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(output_path, terminal_path)

            if runtime.status_path:
                write_status_file(runtime.status_path, runtime, stats, rows, output_path, terminal_path, parquet_paths)

            print(
                "PYTHON M0001 BRAIN | "
                f"source={config_meta} data={runtime.data_source} request={runtime.request_id} "
                f"symbol={runtime.symbol} timeframe={runtime.timeframe} bars={stats['bars']} "
                f"L={runtime.L} zone={runtime.zone_ratio} gap={runtime.exit_gap} mode={runtime.mode} "
                f"random={int(runtime.random)} nodes={stats['actual_nodes']} events={stats['actual_events']} "
                f"rows={len(rows)} parquet={runtime.artifact_dir} adapter={terminal_path or output_path}"
            )
        except Exception as exc:
            print(f"PYTHON M0001 BRAIN ERROR | {type(exc).__name__}: {exc}", file=sys.stderr)
            if runtime is not None and getattr(runtime, "status_path", None):
                write_error_status_file(runtime.status_path, runtime, exc)

        if args.once:
            break

        time.sleep(max(0.05, float(getattr(runtime, "interval", args.interval) if runtime else args.interval)))

    return 0


def resolve_runtime_args(args) -> tuple[SimpleNamespace | None, str]:
    cfg = {}
    cfg_path = Path(args.mql_config) if args.mql_config else None
    if cfg_path is not None:
        if not cfg_path.exists():
            if args.wait_for_config:
                return None, "mql_config_wait"
        else:
            cfg = read_key_value_config(cfg_path)

    symbol = cfg.get("symbol", args.symbol)
    timeframe = cfg.get("timeframe", args.timeframe)
    bars = int_value(cfg.get("bars"), args.bars)
    L = int_value(cfg.get("L"), args.L)
    zone_ratio = float_value(cfg.get("zone_ratio"), args.zone_ratio)
    exit_gap = int_value(cfg.get("exit_gap"), args.exit_gap)
    mode = cfg.get("mode", args.mode)
    if mode not in {"hunt", "touch"}:
        mode = args.mode

    random_enabled = bool_value(cfg.get("random"), args.random)
    random_count = int_value(cfg.get("random_count"), args.random_count)
    if random_count is not None and random_count <= 0:
        random_count = None
    seed = int_value(cfg.get("seed"), args.seed)
    refresh_ms = int_value(cfg.get("refresh_ms"), None)
    interval = (refresh_ms / 1000.0) if refresh_ms is not None and refresh_ms > 0 else args.interval

    data_source = cfg.get("data_source", "cache")
    request_id = cfg.get("request_id", "cli")
    output_from_config = cfg.get("output")
    candles_from_config = cfg.get("candles_file")
    status_from_config = cfg.get("status_file")
    artifact_from_config = cfg.get("artifact_dir")
    terminal_output_path = None
    candles_path = None
    status_path = None

    if output_from_config:
        output_rel = normalize_relative_path(output_from_config)
        local_output = PROJECT_ROOT / "mql5" / "Files" / output_rel
        if args.terminal_files_root:
            terminal_output_path = Path(args.terminal_files_root) / output_rel
    else:
        local_output = Path(args.output) if args.output else default_output_path(symbol, timeframe)
        if args.terminal_files_output:
            terminal_output_path = Path(args.terminal_files_output)

    if candles_from_config and args.terminal_files_root:
        candles_path = Path(args.terminal_files_root) / normalize_relative_path(candles_from_config)
    elif candles_from_config:
        candles_path = PROJECT_ROOT / "mql5" / "Files" / normalize_relative_path(candles_from_config)

    if status_from_config and args.terminal_files_root:
        status_path = Path(args.terminal_files_root) / normalize_relative_path(status_from_config)
    elif status_from_config:
        status_path = PROJECT_ROOT / "mql5" / "Files" / normalize_relative_path(status_from_config)

    if args.artifact_root:
        artifact_dir = Path(args.artifact_root)
    elif artifact_from_config and args.terminal_files_root:
        artifact_dir = Path(args.terminal_files_root) / normalize_relative_path(artifact_from_config)
    elif artifact_from_config:
        artifact_dir = PROJECT_ROOT / "mql5" / "Files" / normalize_relative_path(artifact_from_config)
    else:
        artifact_dir = PROJECT_ROOT / "mql5" / "Files" / "DecisionAlphaLab" / "M0001" / "parquet" / f"{sanitize_path(symbol)}_{sanitize_path(timeframe)}"

    return SimpleNamespace(
        symbol=symbol,
        timeframe=timeframe,
        bars=bars,
        L=L,
        zone_ratio=zone_ratio,
        exit_gap=exit_gap,
        mode=mode,
        random=random_enabled,
        random_count=random_count,
        seed=seed,
        output_path=local_output,
        terminal_output_path=terminal_output_path,
        data_source=data_source,
        candles_path=candles_path,
        status_path=status_path,
        artifact_dir=artifact_dir,
        request_id=request_id,
        interval=interval,
    ), ("mql_inputs" if cfg else "cli_args")


def runtime_input_signature(runtime, cli_args) -> tuple:
    """Detect whether the bridge inputs actually changed.

    This prevents recomputing the same chart window every timer cycle. New bars,
    input changes, config changes, or candle-file updates create a new signature.
    """
    paths = [
        getattr(runtime, "candles_path", None),
        Path(cli_args.mql_config) if getattr(cli_args, "mql_config", None) else None,
    ]

    file_parts = []
    for path in paths:
        if path is None:
            file_parts.append(None)
            continue
        path = Path(path)
        if not path.exists():
            file_parts.append((str(path), None, None))
            continue
        stat = path.stat()
        file_parts.append((str(path), int(stat.st_mtime_ns), int(stat.st_size)))

    return (
        runtime.symbol,
        runtime.timeframe,
        runtime.bars,
        runtime.L,
        runtime.zone_ratio,
        runtime.exit_gap,
        runtime.mode,
        bool(runtime.random),
        runtime.random_count,
        runtime.seed,
        runtime.data_source,
        str(runtime.output_path),
        str(runtime.terminal_output_path),
        str(runtime.artifact_dir),
        tuple(file_parts),
    )


def build_contract(args) -> SimpleNamespace:
    if args.data_source == "mql_candles":
        if args.candles_path is None:
            raise FileNotFoundError("MQL candle source requested but no candles_file was provided in config")
        candles = load_mql_candles(args.candles_path, args.bars)
    else:
        candles = load_cached_candles(args.symbol, args.timeframe, args.bars)

    engine = DataFrameEngine(candles)
    detector = LRuleNodeDetector(engine=engine, L=args.L)
    nodes = detector.detect(args.symbol, _Timeframe(args.timeframe))

    config = RTVConfig(
        L=args.L,
        zone_ratio=args.zone_ratio,
        exit_gap=args.exit_gap,
        consumption_mode=args.mode,
    )

    refs = reference_points_from_lrule_nodes(nodes, candles, args.L)
    events = compute_rtv_events(candles, refs, config)

    all_refs = list(refs)
    all_events = list(events)
    random_refs = []
    random_events = []

    if args.random:
        count = args.random_count or max(1, len(refs))
        random_refs = random_reference_points(candles, count=count, L=args.L, seed=args.seed)
        random_events = compute_rtv_events(candles, random_refs, config)
        all_refs.extend(random_refs)
        all_events.extend(random_events)

    rows = build_visual_rows(all_refs, all_events, candles_df=candles, config=config)
    stats = {
        "bars": len(candles),
        "actual_nodes": len(refs),
        "actual_events": len(events),
        "random_nodes": len(random_refs),
        "random_events": len(random_events),
    }
    return SimpleNamespace(
        candles=candles,
        references=refs,
        events=events,
        random_references=random_refs,
        random_events=random_events,
        all_references=all_refs,
        all_events=all_events,
        rows=rows,
        stats=stats,
        config=config,
    )


def load_mql_candles(path: Path, bars: int) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"MQL candle file is not ready yet: {path}")

    last_exc: Exception | None = None
    for _ in range(8):
        try:
            df = pd.read_csv(path)
            if df.empty:
                raise ValueError(f"MQL candle file is empty: {path}")
            df = normalize_ohlc(df)
            if bars and bars > 0:
                df = df.tail(int(bars)).reset_index(drop=True)
            return df
        except Exception as exc:  # pragma: no cover - timing dependent
            last_exc = exc
            time.sleep(0.05)
    raise RuntimeError(f"Could not read stable MQL candle file {path}: {last_exc}")


def write_parquet_artifacts(runtime, result: SimpleNamespace) -> dict[str, Path]:
    root = Path(runtime.artifact_dir)
    root.mkdir(parents=True, exist_ok=True)

    paths = {
        "candles": root / "candles.parquet",
        "references": root / "references.parquet",
        "events": root / "events.parquet",
        "visual_rows": root / "visual_rows.parquet",
        "manifest": root / "manifest.parquet",
    }

    result.candles.to_parquet(paths["candles"], index=False)
    dataframe_from_dataclasses(result.all_references).to_parquet(paths["references"], index=False)
    pd.DataFrame([event.to_dict(include_visual_fields=True) for event in result.all_events]).to_parquet(paths["events"], index=False)
    visual_rows_dataframe(result.rows).to_parquet(paths["visual_rows"], index=False)
    pd.DataFrame(
        [
            {
                "request_id": runtime.request_id,
                "symbol": runtime.symbol,
                "timeframe": runtime.timeframe,
                "bars": result.stats.get("bars", 0),
                "L": runtime.L,
                "zone_ratio": runtime.zone_ratio,
                "exit_gap": runtime.exit_gap,
                "mode": runtime.mode,
                "random": bool(runtime.random),
                "seed": runtime.seed,
                "data_source": runtime.data_source,
                "artifact_dir": str(root),
                "mql_adapter": str(runtime.terminal_output_path or runtime.output_path),
                "created_at_utc": pd.Timestamp.now(tz="UTC").isoformat(),
            }
        ]
    ).to_parquet(paths["manifest"], index=False)
    return paths


def dataframe_from_dataclasses(items) -> pd.DataFrame:
    rows = []
    for item in items:
        try:
            rows.append(asdict(item))
        except TypeError:
            rows.append(dict(item))
    df = pd.DataFrame(rows)
    return parquet_safe_dataframe(df)


def visual_rows_dataframe(rows: list[dict]) -> pd.DataFrame:
    """Return a Parquet-safe visual rows DataFrame.

    Visual rows intentionally use blanks for non-applicable values because the
    MQL CSV adapter is a flat drawing protocol. Parquet needs stable column
    types, so blanks are converted to nullable values before writing.
    """
    df = pd.DataFrame(rows)
    return parquet_safe_dataframe(df)


def parquet_safe_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    out = df.copy()

    numeric_cols = [
        "price",
        "lower",
        "upper",
        "rtv",
        "node_id",
        "revisit_id",
        "entry_index",
        "exit_index",
        "candle_index",
        "value1",
        "value2",
        "node_price",
        "territory_lower",
        "territory_upper",
        "expansion_extreme",
        "mean_inside",
        "mean_before",
        "median_inside",
        "median_before",
        "RTV",
        "event_length",
        "hunt_index",
        "hunt_price",
        "ref_id",
        "index",
        "active_from_index",
    ]

    bool_cols = ["hunted", "confirmed", "random"]

    for col in numeric_cols:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col].replace("", pd.NA), errors="coerce")

    for col in bool_cols:
        if col in out.columns:
            out[col] = out[col].map(to_nullable_bool).astype("boolean")

    for col in out.columns:
        if col in numeric_cols or col in bool_cols:
            continue
        # Lists and other Python objects are converted to stable strings so
        # pyarrow never sees mixed object types.
        out[col] = out[col].map(lambda value: "" if value is None else (" ".join(str(x) for x in value) if isinstance(value, list) else str(value)))

    return out


def to_nullable_bool(value):
    if value is None or value is pd.NA or value == "":
        return pd.NA
    if isinstance(value, bool):
        return value
    text = str(value).strip().lower()
    if text in {"1", "true", "yes", "y", "on"}:
        return True
    if text in {"0", "false", "no", "n", "off"}:
        return False
    return pd.NA


def write_visual_adapter_with_retries(path: Path, rows: list[dict], attempts: int = 20, delay: float = 0.05) -> Path:
    """Write the thin MQL CSV adapter without failing when MT5 is reading it.

    MQL5 may open the adapter file while Python is refreshing it. We write to a
    temporary file first, then replace/copy with retries. The authoritative
    artifacts are Parquet; this file is only the visual render adapter.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")

    last_exc: Exception | None = None
    for _ in range(max(1, attempts)):
        try:
            write_visual_csv(tmp, rows)
            try:
                tmp.replace(path)
            except PermissionError:
                # Some Windows/MQL read handles still block replace. Retry shortly.
                raise
            return path
        except PermissionError as exc:
            last_exc = exc
            time.sleep(delay)

    # Last attempt: direct write, so any remaining error is explicit in logs.
    write_visual_csv(path, rows)
    if tmp.exists():
        try:
            tmp.unlink()
        except OSError:
            pass
    return path


def write_status_file(path: Path, runtime, stats: dict, rows: list[dict], output_path: Path, terminal_path: Path | None, parquet_paths: dict[str, Path]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f"request_id={runtime.request_id}",
        "status=ok",
        "artifact_format=parquet",
        "mql_visual_adapter=csv",
        f"data_source={runtime.data_source}",
        f"symbol={runtime.symbol}",
        f"timeframe={runtime.timeframe}",
        f"bars={stats.get('bars', 0)}",
        f"L={runtime.L}",
        f"zone_ratio={runtime.zone_ratio}",
        f"exit_gap={runtime.exit_gap}",
        f"mode={runtime.mode}",
        f"actual_nodes={stats.get('actual_nodes', 0)}",
        f"actual_events={stats.get('actual_events', 0)}",
        f"random_nodes={stats.get('random_nodes', 0)}",
        f"random_events={stats.get('random_events', 0)}",
        f"visual_rows={len(rows)}",
        f"artifact_dir={runtime.artifact_dir}",
        f"candles_parquet={parquet_paths.get('candles', '')}",
        f"events_parquet={parquet_paths.get('events', '')}",
        f"visual_rows_parquet={parquet_paths.get('visual_rows', '')}",
        f"mql_adapter={terminal_path or output_path}",
        f"updated_at_utc={pd.Timestamp.now(tz="UTC").isoformat()}",
    ]
    atomic_write_text(path, "\n".join(lines) + "\n")


def write_error_status_file(path: Path, runtime, exc: Exception) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f"request_id={getattr(runtime, 'request_id', 'unknown')}",
        "status=error",
        f"error_type={type(exc).__name__}",
        f"error={str(exc)}",
        f"artifact_dir={getattr(runtime, 'artifact_dir', '')}",
        f"updated_at_utc={pd.Timestamp.now(tz="UTC").isoformat()}",
    ]
    atomic_write_text(path, "\n".join(lines) + "\n")


def atomic_write_text(path: Path, text: str) -> None:
    path = Path(path)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


def read_key_value_config(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        data[key.strip()] = value.strip()
    return data


def normalize_relative_path(value: str) -> Path:
    text = str(value).strip().replace("\\", "/")
    parts = [part for part in text.split("/") if part and part not in {".", ".."}]
    return Path(*parts)


def sanitize_path(value: str) -> str:
    return str(value).replace("#", "IDX").replace("/", "_").replace("\\", "_").replace(" ", "_").replace(":", "_")


def int_value(value, default):
    if value is None or value == "":
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def float_value(value, default):
    if value is None or value == "":
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def bool_value(value, default=False) -> bool:
    if value is None or value == "":
        return bool(default)
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y", "on"}


if __name__ == "__main__":
    raise SystemExit(main())
