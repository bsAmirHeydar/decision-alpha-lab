#!/usr/bin/env python3
"""Run the bounded Phase 55 Python/static regression suite in parallel."""
from __future__ import annotations
from tools.repository_paths import find_repository_root

import argparse
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path

ROOT = find_repository_root(__file__)
COMMANDS = (
    [sys.executable, "-m", "unittest", "-v", "tests/flag_counting/test_nds_hook_864_cycle_r1_reference.py"],
    [sys.executable, "-m", "unittest", "-v", "tests/flag_counting/test_nds_hook_864_tester_log_analyzer.py"],
    [sys.executable, "-m", "unittest", "-v", "tests/flag_counting/test_nds_hook_864_exact_acceleration.py"],
    [sys.executable, "-m", "unittest", "-v", "tests/flag_counting/test_nds_hook_864_acceleration_log_compare.py"],
    [sys.executable, "contexts/legacy/tools/flag_counting/nds_hook_864_cycle_r1_contract_qa.py", "--root", "."],
    [sys.executable, "contexts/legacy/tools/flag_counting/nds_hook_trade_contract_qa.py", "--root", "."],
    [sys.executable, "contexts/legacy/tools/flag_counting/nds_lightweight_backtest_contract_qa.py"],
    [sys.executable, "contexts/legacy/tools/flag_counting/nds_entry_contract_qa.py", "--root", "."],
    [sys.executable, "contexts/legacy/tools/flag_counting/nds_hook_contract_qa.py", "--root", "."],
    [sys.executable, "contexts/legacy/tools/flag_counting/nds_tester_oninit_contract_qa.py"],
    [sys.executable, "contexts/legacy/tools/flag_counting/static_qa.py", "--root", "."],
)


@dataclass(frozen=True)
class CommandResult:
    index: int
    command: list[str]
    returncode: int
    stdout: str
    elapsed_seconds: float


def run_command(index: int, command: list[str]) -> CommandResult:
    started = time.perf_counter()
    completed = subprocess.run(
        command,
        cwd=ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    return CommandResult(
        index=index,
        command=command,
        returncode=completed.returncode,
        stdout=completed.stdout,
        elapsed_seconds=time.perf_counter() - started,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--jobs",
        type=int,
        default=min(len(COMMANDS), max(2, os.cpu_count() or 2)),
        help="maximum concurrent read-only QA subprocesses",
    )
    parser.add_argument(
        "--serial",
        action="store_true",
        help="run one command at a time for troubleshooting",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    jobs = 1 if args.serial else max(1, min(args.jobs, len(COMMANDS)))
    suite_started = time.perf_counter()
    results: dict[int, CommandResult] = {}

    print(f"Phase55 QA scheduling: commands={len(COMMANDS)} jobs={jobs}", flush=True)
    with ThreadPoolExecutor(max_workers=jobs, thread_name_prefix="phase55-qa") as pool:
        future_map = {
            pool.submit(run_command, index, list(command)): index
            for index, command in enumerate(COMMANDS, start=1)
        }
        for future in as_completed(future_map):
            result = future.result()
            results[result.index] = result
            state = "PASS" if result.returncode == 0 else "FAIL"
            print(
                f"[{state} {result.index}/{len(COMMANDS)}] "
                f"{result.elapsed_seconds:.2f}s {' '.join(result.command)}",
                flush=True,
            )

    # Preserve deterministic human-readable output order even though execution
    # was concurrent. Every command always completes; no fail-fast hides errors.
    first_failure = 0
    for index in range(1, len(COMMANDS) + 1):
        result = results[index]
        print(f"\n[Phase55 QA {index}/{len(COMMANDS)}] {' '.join(result.command)}")
        if result.stdout:
            print(result.stdout, end="" if result.stdout.endswith("\n") else "\n")
        if result.returncode != 0 and first_failure == 0:
            first_failure = result.returncode

    elapsed = time.perf_counter() - suite_started
    if first_failure:
        print(f"\nUCE Phase 55 bounded QA: FAIL elapsed={elapsed:.2f}s", file=sys.stderr)
        return first_failure

    print(f"\nUCE Phase 55 bounded QA: PASS elapsed={elapsed:.2f}s jobs={jobs}")
    print("MetaEditor/MT5/broker evidence: NOT EXECUTED by this runner")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
