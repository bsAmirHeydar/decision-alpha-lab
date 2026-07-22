from __future__ import annotations

import argparse
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

from .config import build_symbol_selection_config, load_mt5_activation_config
from .orchestrator import RTHPMT5Automation
from .verify import verify_mt5_run


def _safe(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", value.strip()).strip("_") or "SYMBOL"


def _default_output_root(primary: str, secondary: str) -> Path:
    override = os.environ.get("ALPHA_LAB_RUN_ROOT")
    if override:
        base = Path(override).expanduser()
    else:
        local = os.environ.get("LOCALAPPDATA")
        base = Path(local) / "AlphaLab" / "runs" if local else Path.home() / ".alpha_lab" / "runs"
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return (base / "rthp_mt5" / f"{_safe(primary)}__{_safe(secondary)}" / stamp).resolve()


def _add_symbol_args(command: argparse.ArgumentParser) -> None:
    command.add_argument("--primary", required=True, help="Primary MetaTrader symbol exactly as exposed by the terminal.")
    command.add_argument("--secondary", required=True, help="Secondary MetaTrader symbol exactly as exposed by the terminal.")
    command.add_argument("--output-root", help="Optional immutable output directory. Defaults outside the repository.")
    command.add_argument("--terminal-path", help="Optional terminal64.exe path. Omit for MetaTrader auto-discovery.")
    command.add_argument("--lookback-days", type=int, default=730)
    command.add_argument("--minimum-common-days", type=int, default=30)
    command.add_argument("--no-train", action="store_true", help="Acquire, validate and freeze M1 data without training.")
    command.add_argument("--task-id", action="append", default=[], help="Optional task id; repeat to select multiple tasks.")
    command.add_argument("--family", action="append", default=[], help="Optional RTHP family filter; repeat as needed.")


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="rthp-mt5", description="Read-only MT5 M1 acquisition and one-click RTHP train activation.")
    subparsers = root.add_subparsers(dest="command", required=True)
    for name in ("validate-config", "preflight", "run"):
        command = subparsers.add_parser(name)
        command.add_argument("--config", required=True)
    for name in ("preflight-symbols", "run-symbols"):
        _add_symbol_args(subparsers.add_parser(name))
    verify = subparsers.add_parser("verify-run")
    verify.add_argument("--run-root", required=True)
    return root


def _config_from_symbols(args: argparse.Namespace):
    output = Path(args.output_root).expanduser().resolve() if args.output_root else _default_output_root(args.primary, args.secondary)
    return build_symbol_selection_config(
        args.primary,
        args.secondary,
        output,
        terminal_path=args.terminal_path,
        lookback_days=args.lookback_days,
        minimum_common_days=args.minimum_common_days,
        train_enabled=not args.no_train,
        selected_task_ids=tuple(args.task_id),
        family_filter=tuple(args.family),
    )


def main(argv=None) -> int:
    args = parser().parse_args(argv)
    if args.command == "verify-run":
        result = verify_mt5_run(args.run_root)
    elif args.command in {"preflight-symbols", "run-symbols"}:
        config = _config_from_symbols(args)
        automation = RTHPMT5Automation(config)
        result = automation.preflight() if args.command == "preflight-symbols" else automation.run()
        result["resolved_output_root"] = config.output_root.as_posix()
    else:
        config = load_mt5_activation_config(args.config)
        if args.command == "validate-config":
            result = {
                "status": "PASS",
                "config_digest": config.digest,
                "canonical_source_timeframe": "M1_CLOSED_BARS",
                "sub_m1_allowed": False,
            }
        elif args.command == "preflight":
            result = RTHPMT5Automation(config).preflight()
        else:
            result = RTHPMT5Automation(config).run()
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0 if result.get("status") == "PASS" or str(result.get("status", "")).startswith("PASS_") else 2


if __name__ == "__main__":
    raise SystemExit(main())
