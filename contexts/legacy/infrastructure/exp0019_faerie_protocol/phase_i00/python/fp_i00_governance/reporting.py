"""Writers for FP-I00 governed artifacts."""
from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
import json

from .models import ValidationReport
from .scanner import scan_dependencies, scan_tests, scan_ownership, write_csv


def write_artifacts(repo: Path, policy: dict, report: ValidationReport) -> None:
    artifacts = repo / policy["artifacts_root"]
    artifacts.mkdir(parents=True, exist_ok=True)
    dependencies = scan_dependencies(repo, policy)
    tests = scan_tests(repo, policy)
    ownership = scan_ownership(policy)

    dependency_rows = [asdict(record) for record in dependencies]
    write_csv(
        artifacts / "FP_I00_SHARED_CORE_DEPENDENCY_INVENTORY.csv",
        dependency_rows,
        ["dependency_id", "semantic_owner", "reuse_classification", "relative_root", "file_count", "aggregate_sha256", "exact_version", "required_for_phase", "mutation_allowed"],
    )
    (artifacts / "FP_I00_SHARED_CORE_DEPENDENCY_INVENTORY.json").write_text(json.dumps(dependency_rows, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    test_rows = [asdict(record) for record in tests]
    write_csv(
        artifacts / "FP_I00_PREVIOUS_CONTEXT_TEST_INVENTORY.csv",
        test_rows,
        ["context_id", "test_id", "test_type", "relative_path", "exists", "compile_required", "execution_command"],
    )
    ownership_rows = [asdict(record) for record in ownership]
    write_csv(
        artifacts / "FP_I00_PHASE_FILE_OWNERSHIP.csv",
        ownership_rows,
        ["path_prefix", "owner_phase", "ownership_class", "mutation_policy", "rollback_policy"],
    )
    (artifacts / "FP_I00_VALIDATION_REPORT.json").write_text(json.dumps(report.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
