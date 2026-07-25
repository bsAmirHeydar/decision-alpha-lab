#!/usr/bin/env python3
"""Run the exact repository engineering-policy checks locally and in GitHub Actions.

This is the single entry point for the Engineering Policy workflow.  It keeps the
local pre-push command and CI behavior identical and prints the failing stage in a
clear summary.
"""
from __future__ import annotations

import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Check:
    name: str
    command: tuple[str, ...]


def _run(check: Check, root: Path) -> tuple[int, str]:
    proc = subprocess.run(
        check.command,
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return proc.returncode, proc.stdout


def _write_github_summary(results: list[tuple[Check, int]]) -> None:
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_path:
        return
    lines = [
        "## Engineering Policy",
        "",
        "| Check | Result |",
        "|---|---|",
    ]
    for check, code in results:
        lines.append(f"| {check.name} | {'PASS' if code == 0 else 'FAIL'} |")
    lines.append("")
    lines.append(
        "A failed check means the repository preflight failed; it does not mean the Git commit itself is corrupt."
    )
    Path(summary_path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def _checks(python: str) -> tuple[Check, ...]:
    """Return the single ordered preflight contract used locally and in CI."""
    return (
        Check(
            "Repository policy",
            (python, "tools/engineering/validate_alpha_lab_policy.py", "."),
        ),
        Check(
            "Obsidian operating system",
            (
                python,
                "docs/alpha_lab_master_architecture/ai_algorithm_engineering_os/tools/validate_vault.py",
                "docs/alpha_lab_master_architecture/ai_algorithm_engineering_os",
            ),
        ),
        Check(
            "Unified consolidation Obsidian program",
            (
                python,
                "docs/alpha_lab_master_architecture/01_UNIFIED_CONSOLIDATION_AND_PLATFORM_SEAL/tools/validate_program_vault.py",
                "docs/alpha_lab_master_architecture/01_UNIFIED_CONSOLIDATION_AND_PLATFORM_SEAL",
            ),
        ),
        Check(
            "MQL5 compatibility",
            (python, "tools/engineering/check_mql5_compatibility.py", "."),
        ),
        Check(
            "Repository layout",
            (python, "tools/engineering/audit_repository_layout.py", "."),
        ),
    )


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    checks = _checks(sys.executable)

    results: list[tuple[Check, int]] = []
    for check in checks:
        print(f"\n::group::{check.name}")
        code, output = _run(check, root)
        print(output.rstrip())
        print("::endgroup::")
        results.append((check, code))

    print("\nEngineering Policy Summary")
    print("=" * 27)
    for check, code in results:
        print(f"{'PASS' if code == 0 else 'FAIL':4}  {check.name}")

    _write_github_summary(results)
    failed = [check.name for check, code in results if code != 0]
    if failed:
        print("\nFailed stages: " + ", ".join(failed))
        return 1
    print("\nAll engineering-policy checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
