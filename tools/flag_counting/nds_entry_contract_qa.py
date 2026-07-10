#!/usr/bin/env python3
"""Static contract QA for the NDS Entry Transition scaffold.

The scanner validates separation, fail-closed defaults, traceability, and the
no-send boundary. It deliberately does not encode unresolved Zone, Entry,
Stop, Target, sizing, or broker doctrine.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Check:
    check_id: str
    status: str
    path: str
    detail: str


REQUIRED_FILES = (
    "mql5/Include/FlagCountingPhoenix/FP_NDSStructureSnapshot.mqh",
    "mql5/Include/FlagCountingPhoenix/FP_NDSEntryTypes.mqh",
    "mql5/Include/FlagCountingPhoenix/FP_NDSEntryRules.mqh",
    "mql5/Include/FlagCountingPhoenix/FP_NDSEntryExport.mqh",
    "mql5/Include/FlagCountingPhoenix/FP_NDSEntryEngine.mqh",
    "docs/nds_entry_architecture/README.md",
    "docs/nds_entry_architecture/03_zone_adapter_contract.md",
    "docs/nds_entry_architecture/06_command_preview_contract.md",
    "docs/nds_entry_architecture/10_validation_and_release_plan.md",
    "docs/obsidian_hook/00_mocs/NDS_ENTRY_EXECUTION_MOC.md",
    "docs/obsidian_hook/03_architecture/Phase 51 NDS Entry Transition Architecture.md",
    "docs/obsidian_hook/05_templates/NDS Setup Review Template.md",
)


def read(root: Path, rel: str) -> str:
    return (root / rel).read_text(encoding="utf-8", errors="ignore")


def check_contains(checks: list[Check], root: Path, rel: str, needle: str,
                   check_id: str, detail: str) -> None:
    ok = needle in read(root, rel)
    checks.append(Check(check_id, "PASS" if ok else "FAIL", rel, detail))


def check_excludes(checks: list[Check], text: str, path: str, needle: str,
                   check_id: str, detail: str) -> None:
    ok = needle not in text
    checks.append(Check(check_id, "PASS" if ok else "FAIL", path, detail))


def run(root: Path) -> list[Check]:
    checks: list[Check] = []
    for rel in REQUIRED_FILES:
        checks.append(Check(
            "NDS_ENTRY_REQUIRED_FILE",
            "PASS" if (root / rel).is_file() else "FAIL",
            rel,
            "required NDS Entry implementation or authority file",
        ))

    ea = "mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5"
    hook_engine = "mql5/Include/FlagCountingPhoenix/FP_HookPhase02Engine.mqh"
    snapshot = "mql5/Include/FlagCountingPhoenix/FP_NDSStructureSnapshot.mqh"
    types = "mql5/Include/FlagCountingPhoenix/FP_NDSEntryTypes.mqh"
    rules = "mql5/Include/FlagCountingPhoenix/FP_NDSEntryRules.mqh"
    export = "mql5/Include/FlagCountingPhoenix/FP_NDSEntryExport.mqh"

    check_contains(checks, root, ea, '#property version   "18.40"',
                   "NDS_ENTRY_EA_VERSION", "central EA contains Phase 51 scaffold and Phase 52 overlay")
    check_contains(checks, root, ea,
                   "InpNDSEntryContractProfile = FP_NDS_ENTRY_PROFILE_PRE_CANON_BLOCKED",
                   "NDS_ENTRY_FAIL_CLOSED_PROFILE", "default profile blocks before Zone Canon")
    check_contains(checks, root, ea,
                   "InpNDSTradeDirectionPolicy = FP_NDS_TRADE_DIRECTION_UNRESOLVED",
                   "NDS_ENTRY_DIRECTION_UNRESOLVED", "trade direction is not inferred silently")
    for field, check_id in (
        ("InpNDSEntryZoneCanonLocked = false", "NDS_ENTRY_ZONE_LOCK_FALSE"),
        ("InpNDSEntryTradeContractLocked = false", "NDS_ENTRY_TRADE_LOCK_FALSE"),
        ("InpNDSEntryCommandPreviewOnly = true", "NDS_ENTRY_PREVIEW_LOCK_TRUE"),
    ):
        check_contains(checks, root, ea, field, check_id, "safe authority default")

    check_contains(checks, root, hook_engine, "FP_NDSClearStructureSnapshot",
                   "NDS_ENTRY_SNAPSHOT_CLEAR", "snapshot is cleared before Hook reconstruction")
    check_contains(checks, root, hook_engine, "FP_NDSCaptureStructureSnapshot",
                   "NDS_ENTRY_SNAPSHOT_CAPTURE", "annotated Hook sequences are captured")
    check_contains(checks, root, snapshot, "FP_NDSStructureSnapshotMatches",
                   "NDS_ENTRY_SNAPSHOT_SCOPE", "snapshot is scoped by symbol and timeframe")

    check_contains(checks, root, rules, "FP_NDSSequenceBaseEligible",
                   "NDS_ENTRY_VALID_HOOK_GATE", "source selection uses explicit Hook eligibility")
    check_contains(checks, root, rules, "FP_NDSBuildCanonicalZoneAdapter",
                   "NDS_ENTRY_ZONE_ADAPTER", "Zone Canon has a single adapter seam")
    check_contains(checks, root, rules, "NDS_ZONE_CANON_ADAPTER_PENDING",
                   "NDS_ENTRY_CANON_PENDING", "unimplemented Canon blocks explicitly")
    check_contains(checks, root, rules, "manual_entry_must_be_inside_manual_zone",
                   "NDS_ENTRY_DIAGNOSTIC_ENTRY_ZONE_GATE", "manual entry must lie in diagnostic Zone")
    check_contains(checks, root, rules, "Surface the earliest failing authority boundary",
                   "NDS_ENTRY_FIRST_FAILURE", "pipeline reports first authority failure")
    check_contains(checks, root, rules, "command.volume = 0.0",
                   "NDS_ENTRY_ZERO_VOLUME", "command preview always uses zero volume")
    check_contains(checks, root, rules, "command.send_allowed = false",
                   "NDS_ENTRY_SEND_FALSE", "command preview cannot authorize send")
    check_contains(checks, root, rules, 'command.command_action = "PREVIEW_ONLY_NO_SEND"',
                   "NDS_ENTRY_ACTION_PREVIEW", "command action states no-send contract")

    check_contains(checks, root, types, "requested_risk_fraction",
                   "NDS_ENTRY_RISK_FIELD", "Trade Plan exposes risk boundary fields")
    check_contains(checks, root, types, "FP_NDSCommandPreviewRow",
                   "NDS_ENTRY_COMMAND_ENVELOPE", "broker-neutral command envelope exists")

    for filename in (
        "nds_entry_structure_snapshot.csv",
        "nds_entry_setup_candidate.csv",
        "nds_entry_trade_plan.csv",
        "nds_entry_command_preview.csv",
        "nds_entry_pipeline_summary.csv",
    ):
        check_contains(checks, root, export, filename,
                       "NDS_ENTRY_AUDIT_FILE", f"audit export includes {filename}")

    scope_files = (snapshot, types, rules, export,
                   "mql5/Include/FlagCountingPhoenix/FP_NDSEntryEngine.mqh")
    scope = "\n".join(read(root, rel) for rel in scope_files)
    forbidden = (
        "OrderSend(",
        "OrderSendAsync(",
        "CTrade",
        ".Buy(",
        ".Sell(",
        "TRADE_ACTION_DEAL",
        "TRADE_ACTION_PENDING",
    )
    for token in forbidden:
        check_excludes(
            checks, scope,
            "mql5/Include/FlagCountingPhoenix/FP_NDS*.mqh",
            token,
            "NDS_ENTRY_NO_BROKER_SEND",
            f"entry-transition scope excludes broker-send token {token}",
        )

    if not any(item.status == "FAIL" for item in checks):
        checks.append(Check(
            "NDS_ENTRY_CONTRACT_QA", "PASS", ".",
            "all Phase 51 fail-closed and no-send contracts passed",
        ))
    return checks


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    checks = run(root)
    for item in checks:
        print(f"{item.status}\t{item.check_id}\t{item.path}\t{item.detail}")
    return 1 if any(item.status == "FAIL" for item in checks) else 0


if __name__ == "__main__":
    raise SystemExit(main())
