#!/usr/bin/env python3
"""Run the bounded Phase 55 Python/static regression suite."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COMMANDS = (
    [sys.executable, "-m", "unittest", "-v", "tests/flag_counting/test_nds_hook_864_cycle_r1_reference.py"],
    [sys.executable, "-m", "unittest", "-v", "tests/flag_counting/test_nds_hook_864_tester_log_analyzer.py"],
    [sys.executable, "tools/flag_counting/nds_hook_864_cycle_r1_contract_qa.py", "--root", "."],
    [sys.executable, "tools/flag_counting/nds_hook_trade_contract_qa.py", "--root", "."],
    [sys.executable, "tools/flag_counting/nds_lightweight_backtest_contract_qa.py"],
    [sys.executable, "tools/flag_counting/nds_entry_contract_qa.py", "--root", "."],
    [sys.executable, "tools/flag_counting/nds_hook_contract_qa.py", "--root", "."],
    [sys.executable, "tools/flag_counting/nds_tester_oninit_contract_qa.py"],
    [sys.executable, "tools/flag_counting/static_qa.py", "--root", "."],
)


def main() -> int:
    for index, command in enumerate(COMMANDS, start=1):
        print(f"\n[Phase55 QA {index}/{len(COMMANDS)}] {' '.join(command)}", flush=True)
        completed = subprocess.run(command, cwd=ROOT, check=False)
        if completed.returncode != 0:
            print(f"FAILED: {' '.join(command)}", file=sys.stderr)
            return completed.returncode
    print("\nUCE Phase 55 bounded QA: PASS")
    print("MetaEditor/MT5/broker evidence: NOT EXECUTED by this runner")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
