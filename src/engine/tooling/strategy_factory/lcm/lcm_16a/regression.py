from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

LFS_PATHS = (
    "registry/history/lcm/documentation_authority_mappings/"
    "DOCMAP_2AB7C99DBD273C8F29BCD6D455431658/records/documentation_records.jsonl",
    "registry/history/lcm/documentation_authority_mappings/"
    "DOCMAP_2AB7C99DBD273C8F29BCD6D455431658/unknowns/documentation_unknowns.jsonl",
)


@dataclass(frozen=True)
class Suite:
    suite_id: str
    args: tuple[str, ...]
    cwd: str = "."
    extra_python_paths: tuple[str, ...] = ()
    requires_lfs: bool = False
    lfs_dependent_tests: tuple[str, ...] = ()


def _pytest(
    suite_id: str,
    path: str,
    *,
    cwd: str = ".",
    extra: tuple[str, ...] = (),
    requires_lfs: bool = False,
    ignores: tuple[str, ...] = (),
    lfs_dependent_tests: tuple[str, ...] = (),
) -> Suite:
    args = (
        sys.executable,
        "-m",
        "pytest",
        "-q",
        path,
        *sum((("--ignore", item) for item in ignores), ()),
    )
    return Suite(suite_id, args, cwd, extra, requires_lfs, lfs_dependent_tests)


def suite_matrix() -> tuple[Suite, ...]:
    suites: list[Suite] = [
        Suite("ENGINEERING_POLICY", (sys.executable, "tools/engineering/run_engineering_policy.py", ".")),
    ]
    migration = "tests/legacy/strategy_factory/migration"
    for name in (
        "tests_lcm_09b", "tests_lcm_10a", "tests_lcm_10b", "tests_lcm_10c",
        "tests_lcm_11a", "tests_lcm_11b", "tests_lcm_12a", "tests_lcm_12b",
        "tests_lcm_13a", "tests_lcm_13b", "tests_lcm_13c", "tests_lcm_14a",
        "tests_lcm_14b", "tests_lcm_15a", "tests_lcm_15b", "tests_lcm_15c",
    ):
        ignores: tuple[str, ...] = ()
        if name == "tests_lcm_10a":
            ignores = (f"{migration}/{name}/test_rebuild_determinism.py",)
        elif name == "tests_lcm_10b":
            ignores = (f"{migration}/{name}/test_rebuild.py",)
        elif name == "tests_lcm_12a":
            ignores = (f"{migration}/{name}/test_package_verify.py",)
        lfs_dependent_tests: tuple[str, ...] = ()
        if name == "tests_lcm_12a":
            lfs_dependent_tests = (
                f"{migration}/{name}/test_authority.py",
                f"{migration}/{name}/test_references.py",
                f"{migration}/{name}/test_unknowns.py",
            )
        suites.append(
            _pytest(
                name.upper(),
                f"{migration}/{name}",
                requires_lfs=name == "tests_lcm_12a",
                ignores=ignores,
                lfs_dependent_tests=lfs_dependent_tests,
            )
        )

    for phase in range(16):
        suites.append(
            _pytest(
                f"ACL_OS_{phase:02d}",
                f"src/engine/legacy/acl_os_reference/tests_acl_{phase:02d}",
                extra=("src/engine/packages",),
            )
        )

    core = (
        ("SF_PHASE01", "phase01_contracts"), ("SF_PHASE03", "phase03_market"),
        ("SF_PHASE09", "phase09_outcome"), ("SF_PHASE10", "phase10_research"),
        ("SF_PHASE11", "phase11_statistics"), ("SF_PHASE12", "phase12_validation"),
        ("SF_PHASE13", "phase13_training"), ("SF_PHASE14", "phase14_governance"),
        ("SF_PHASE15", "phase15_inference"), ("SF_PHASE17", "phase17_execution"),
        ("SF_PHASE18", "phase18_live"), ("SF_PHASE19", "phase19_monitoring"),
        ("SF_PHASE20", "phase20_integration"),
    )
    for suite_id, directory in core:
        suites.append(_pytest(
            suite_id,
            ".",
            cwd=f"tests/legacy/strategy_factory/v1/{directory}",
            extra=("src/engine/packages",),
        ))

    for suite_id, directory in (
        ("UCE_I14", "phase_uce_i14_runtime_compilation"),
        ("UCE_I16", "phase_uce_i16_context_onboarding"),
        ("UCE_I19", "phase_uce_i19_production_operations"),
        ("SAED_V4_31", "phase_saed_v4_31_formal_verification_safety_case"),
        ("SAED_V4_38", "phase_saed_v4_38_immutable_runtime_mql5_parity"),
        ("SAED_V4_39", "phase_saed_v4_39_prospective_shadow_micro_live"),
        ("SAED_V4_41", "phase_saed_v4_41_continuous_surveillance_retirement"),
        ("RTHP_CONTEXT", "rthp_context"),
        ("RTHP_AI_INPUT", "rthp_ai_input"),
        ("RTHP_TRAIN", "rthp_train_activation"),
        ("RTHP_MT5", "rthp_mt5_activation"),
    ):
        suites.append(_pytest(
            suite_id,
            f"tests/legacy/strategy_factory/v1/{directory}",
            extra=("src/engine/packages",),
        ))

    suites.append(_pytest(
        "FP_I15_AND_NDS_864",
        "contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i15/tests",
        extra=(
            "src/engine/packages",
            "contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i15/python",
        ),
    ))
    suites.append(_pytest(
        "NDS_864_REFERENCE",
        "tests/flag_counting/test_nds_hook_864_cycle_r1_reference.py",
    ))
    suites.append(_pytest(
        "NDS_864_ACCELERATION",
        "tests/flag_counting/test_nds_hook_864_exact_acceleration.py",
    ))
    return tuple(suites)


def lfs_materialized(repo_root: Path) -> tuple[bool, list[str]]:
    pointers: list[str] = []
    marker = b"version https://git-lfs.github.com/spec/v1"
    for relative in LFS_PATHS:
        path = repo_root / relative
        if not path.is_file() or path.read_bytes()[:128].startswith(marker):
            pointers.append(relative)
    return not pointers, pointers


def _run_suite(repo_root: Path, suite: Suite, allow_missing_lfs: bool) -> dict:
    lfs_ok, pointers = lfs_materialized(repo_root)
    partial_lfs_run = suite.requires_lfs and not lfs_ok and allow_missing_lfs
    if suite.requires_lfs and not lfs_ok and not allow_missing_lfs:
        return {
            "suite_id": suite.suite_id,
            "status": "BLOCKED",
            "reason": "GIT_LFS_OBJECTS_NOT_MATERIALIZED",
            "blocked_paths": pointers,
            "blocked_tests": list(suite.lfs_dependent_tests),
            "passed": 0,
            "failed": 0,
            "exit_code": None,
        }
    env = dict(os.environ)
    python_paths = [str(repo_root), *(str(repo_root / item) for item in suite.extra_python_paths)]
    if env.get("PYTHONPATH"):
        python_paths.append(env["PYTHONPATH"])
    env["PYTHONPATH"] = os.pathsep.join(python_paths)
    command = suite.args
    if partial_lfs_run:
        command = (
            *command,
            *sum((("--ignore", item) for item in suite.lfs_dependent_tests), ()),
        )
    process = subprocess.run(
        command,
        cwd=repo_root / suite.cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    output = process.stdout
    passed = sum(int(value) for value in re.findall(r"(\d+) passed", output))
    failed = sum(int(value) for value in re.findall(r"(\d+) failed", output))
    status = "PASS" if process.returncode == 0 else "FAILED"
    if partial_lfs_run and process.returncode == 0:
        status = "PASS_WITH_BLOCKED_EVIDENCE"
    result = {
        "suite_id": suite.suite_id,
        "status": status,
        "command": list(command),
        "working_directory": suite.cwd,
        "passed": passed,
        "failed": failed,
        "exit_code": process.returncode,
        "output_tail": output[-4000:],
    }
    if partial_lfs_run:
        result.update(
            {
                "reason": "GIT_LFS_OBJECTS_NOT_MATERIALIZED",
                "blocked_paths": pointers,
                "blocked_tests": list(suite.lfs_dependent_tests),
            }
        )
    return result


def run(repo_root: Path, allow_missing_lfs: bool = False) -> dict:
    results = [_run_suite(repo_root, suite, allow_missing_lfs) for suite in suite_matrix()]
    failed = [item["suite_id"] for item in results if item["status"] == "FAILED"]
    blocked = [item["suite_id"] for item in results if item["status"] == "BLOCKED"]
    blocked_evidence = [
        item["suite_id"]
        for item in results
        if item["status"] == "PASS_WITH_BLOCKED_EVIDENCE"
    ]
    validation = "PASS" if not failed and (allow_missing_lfs or not blocked) else "FAILED"
    return {
        "schema_version": "1.0.0",
        "phase_id": "LCM-16A",
        "suite_count": len(results),
        "passed_test_count": sum(item["passed"] for item in results),
        "failed_test_count": sum(item["failed"] for item in results),
        "failed_suites": failed,
        "blocked_suites": blocked,
        "blocked_evidence_suites": blocked_evidence,
        "results": results,
        "validation_status": validation,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output")
    parser.add_argument("--allow-missing-lfs", action="store_true")
    args = parser.parse_args()
    report = run(Path(args.repo_root).resolve(), args.allow_missing_lfs)
    payload = json.dumps(report, sort_keys=True, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0 if report["validation_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
