#!/usr/bin/env python3
"""Static QA for NDS Phase 52.1 Strategy Tester OnInit hotfix."""
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    ea_rel = "mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5"
    doc_rel = "docs/nds_entry_architecture/phase52_hook_limit_f123_execution/09_strategy_tester_license_gate.md"
    ea_path = root / ea_rel
    doc_path = root / doc_rel
    ea = ea_path.read_text(encoding="utf-8", errors="ignore") if ea_path.is_file() else ""

    checks: list[Check] = []

    def has(check_id: str, needle: str, detail: str) -> None:
        checks.append(Check(check_id, "PASS" if needle in ea else "FAIL", ea_rel, detail))

    checks.append(Check("P521_EA_EXISTS", "PASS" if ea_path.is_file() else "FAIL", ea_rel,
                        "central Phoenix EA exists"))
    checks.append(Check("P521_DOC_EXISTS", "PASS" if doc_path.is_file() else "FAIL", doc_rel,
                        "tester license authority note exists"))
    has("P521_VERSION", '#property version   "18.41"', "EA version identifies tester hotfix")
    has("P521_TESTER_INPUT", "InpLicenseAllowStrategyTesterBypass = true",
        "Strategy Tester bypass is explicit and enabled by default for research")
    has("P521_OPT_INPUT", "InpLicenseAllowOptimizationBypass = true",
        "optimization-agent bypass is explicit")
    has("P521_TESTER_FLAG", "MQLInfoInteger(MQL_TESTER)",
        "runtime tester property gates the bypass")
    has("P521_OPT_FLAG", "MQLInfoInteger(MQL_OPTIMIZATION)",
        "runtime optimization property gates the bypass")
    has("P521_VISUAL_CONTEXT", "MQLInfoInteger(MQL_VISUAL_MODE)",
        "visual tester context is audited")
    has("P521_BYPASS_BEFORE_LICENSE", "if(FP_OfflineLicenseTesterBypassAllowed(tester_runtime_context))",
        "tester authority is evaluated before signed license validation")
    has("P521_LIVE_PATH_PRESERVED", "FP_CheckOfflineLicenseWithReport(g_fp_license_cfg, g_fp_license_report)",
        "normal signed fail-closed license path remains present")
    has("P521_INIT_GATE", "if(!FP_EnsureOfflineLicense(true))\n      return INIT_FAILED;",
        "OnInit still fails closed when no tester bypass and license is invalid")
    has("P521_AUDIT", "live_license_enforcement=unchanged",
        "tester bypass emits a precise one-time audit message")

    for check in checks:
        print(f"{check.status}\t{check.check_id}\t{check.path}\t{check.detail}")
    return 1 if any(c.status == "FAIL" for c in checks) else 0


if __name__ == "__main__":
    raise SystemExit(main())
