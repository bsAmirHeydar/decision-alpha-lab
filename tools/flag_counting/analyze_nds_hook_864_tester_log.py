#!/usr/bin/env python3
"""Analyze NDS Hook 86.4 Strategy Tester Journal output.

The analyzer is diagnostic only. It reads a saved tester/Journal text file and
reports the first structural or execution gate that explains a zero-trade run.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
from typing import Any

KEY_VALUE = re.compile(r"(?P<key>[A-Za-z0-9_]+)=(?P<value>\{[^}]*\}|[^\s]+)")


def _parse_fields(line: str) -> dict[str, str]:
    return {match.group("key"): match.group("value").strip("{}") for match in KEY_VALUE.finditer(line)}


def _as_int(value: str | None) -> int:
    if value is None:
        return 0
    try:
        return int(value)
    except ValueError:
        return 0


def _parse_funnel(value: str | None) -> dict[str, str]:
    if not value:
        return {}
    fields: dict[str, str] = {}
    for item in value.split(";"):
        if "=" not in item:
            continue
        key, raw = item.split("=", 1)
        fields[key.strip()] = raw.strip()
    return fields


def analyze_text(text: str) -> dict[str, Any]:
    lines = text.splitlines()
    init_rows = [_parse_fields(line) for line in lines if "NDS_BT_INIT" in line]
    run_rows = [_parse_fields(line) for line in lines if "NDS_BT " in line or "NDS_BT\t" in line]
    session_rows = [_parse_fields(line) for line in lines if "NDS_BT_SESSION" in line]

    init = init_rows[-1] if init_rows else {}
    session = session_rows[-1] if session_rows else {}
    last_run = run_rows[-1] if run_rows else {}
    funnel = _parse_funnel(last_run.get("funnel"))

    findings: list[dict[str, str]] = []
    if not init:
        findings.append({"severity": "error", "code": "init_missing", "detail": "NDS_BT_INIT was not found; confirm the intended Expert was executed."})
    else:
        if init.get("trade_profile") != "HOOK_864_CYCLE_R1":
            findings.append({"severity": "error", "code": "wrong_trade_profile", "detail": "Set InpBTTradeProfile=HOOK_864_CYCLE_R1."})
        if init.get("runtime_profile") != "PARITY":
            findings.append({"severity": "warning", "code": "sparse_runtime_profile", "detail": "Use InpBTProfile=PARITY before concluding the rare setup has no candidates."})
        if init.get("orders") == "paper_only":
            findings.append({"severity": "warning", "code": "send_disabled", "detail": "Setup decisions may be recorded but tester orders are disabled."})

    blocker = funnel.get("blocker", "")
    blocker_details = {
        "no_phase02_sequences": "No canonical Hook Phase02 sequence was found in the scanned history/scales.",
        "all_sequences_invalid_or_failed": "Phase02 sequences exist but all are invalid or failed.",
        "no_valid_hook_family": "No existing HH/F3H valid family survived canonical Hook rules.",
        "hook_family_disabled_by_config": "The qualifying family is disabled by trade configuration.",
        "no_confirmed_terminal": "No candidate has a confirmed canonical Phase02 terminal.",
        "no_cycle_crown": "No candidate has a valid canonical cycle crown.",
        "no_x3_or_x4_sequence": "No canonical sequence has x_count exactly 3 or 4.",
        "no_mature_or_capped_sequence": "No x3/x4 sequence is in MATURE or CAPPED state.",
        "phase04_evidence_missing": "Canonical Phase03/04 produced no matching lifecycle evidence.",
        "phase04_x_not_closed": "Matching Phase04 records exist but the canonical 50% X closure has not occurred.",
        "all_closed_cycles_dead_by_origin_return": "All closed candidates were invalidated by origin-return death.",
        "first_864_arrival_already_consumed": "The first 86.4 arrival occurred on or after the closure candle before a new order could be placed.",
        "runtime_contract_rejected": "Visible funnel gates passed but an exact identity/config/runtime contract rejected the candidate.",
        "ready_candidate_exists": "The structural setup exists; inspect downstream exposure, one-attempt, price-side, broker-distance, volume, margin and session gates.",
    }
    if blocker:
        findings.append({"severity": "info", "code": blocker, "detail": blocker_details.get(blocker, "Review the detailed run reason and source gate counters.")})

    limits_sent = _as_int(session.get("limits_sent"))
    paper_ready = _as_int(session.get("paper_ready"))
    ready_runs = _as_int(session.get("ready_runs"))
    blocked = _as_int(session.get("blocked"))
    if session and limits_sent == 0:
        if ready_runs > 0 or paper_ready > 0:
            findings.append({"severity": "warning", "code": "ready_but_not_sent", "detail": "At least one setup reached readiness; the zero-order cause is downstream of Hook/closure selection."})
        elif blocked > 0:
            findings.append({"severity": "warning", "code": "blocked_runs_present", "detail": "Read the per-run status/reason for the first blocked execution gate."})

    return {
        "schema_version": "nds_hook_864_tester_log_diagnostic_v1",
        "init": init,
        "last_run": last_run,
        "funnel": funnel,
        "session": session,
        "trade_count_proxy": limits_sent,
        "findings": findings,
        "log_lines": len(lines),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("log", type=Path, help="Saved MT5 Strategy Tester/Journal text log")
    parser.add_argument("--output", type=Path, help="Optional JSON output path")
    args = parser.parse_args()
    result = analyze_text(args.log.read_text(encoding="utf-8-sig", errors="replace"))
    payload = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True)
    if args.output:
        args.output.write_text(payload + "\n", encoding="utf-8")
    print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
