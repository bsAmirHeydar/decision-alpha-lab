#!/usr/bin/env python3
"""Validate the EXP0019 FP-I00 delivery package."""
from __future__ import annotations

from pathlib import Path
import ast
import csv
import json
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
errors: list[str] = []
phase_root = root / "contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i00"
doc_root = root / "docs/operations/execution/EXP0019_faerie_protocol_contextual_divergence/implementation_program/phase_deliveries/fp_i00"
concept_root = root / "docs/history/obsidian/deep/01_concepts"

required = [
    "releases/history/exp0019/readmes/README_EXP0019_FAERIE_PROTOCOL_FP_I00.md",
    "releases/history/exp0019/installers/INSTALL_EXP0019_FAERIE_PROTOCOL_FP_I00.md",
    "COMMIT_MESSAGE.md",
    "releases/history/exp0019/indexes/EXP0019_FP_I00_FILE_INDEX.txt",
    "releases/history/exp0019/hashes/EXP0019_FP_I00_FILE_HASHES.sha256",
    "releases/history/exp0019/manifests/EXP0019_FP_I00_PATCH_MANIFEST.json",
    "releases/history/exp0019/reports/EXP0019_FP_I00_QA_REPORT.json",
    "contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i00/README.md",
    "contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i00/run_phase_i00.py",
    "contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i00/config/FP_I00_GOVERNANCE_POLICY.v1.json",
    "contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i00/artifacts/FP_I00_BASELINE_MANIFEST.v1.json",
    "contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i00/artifacts/FP_I00_SHARED_CORE_DEPENDENCY_INVENTORY.csv",
    "contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i00/artifacts/FP_I00_PREVIOUS_CONTEXT_TEST_INVENTORY.csv",
    "contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i00/artifacts/FP_I00_PHASE_FILE_OWNERSHIP.csv",
    "contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i00/artifacts/FP_I00_VALIDATION_REPORT.json",
    "contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i00/artifacts/FP_I00_PHASE_STATUS.json",
    "contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i00/artifacts/FP_I00_HANDOFF_TO_FP_I01.json",
    "docs/operations/execution/EXP0019_faerie_protocol_contextual_divergence/implementation_program/phase_deliveries/fp_i00/00_FP_I00_DELIVERY_MOC.md",
    "contexts/legacy/tools/exp0019/validate_fp_i00_delivery.py",
    "contexts/legacy/tools/exp0019/build_fp_i00_release.py"
]
for rel in required:
    if not (root / rel).is_file():
        errors.append(f"missing: {rel}")

expected_modules = {
    "__init__.py", "baseline_diff.py", "canonical.py", "cli.py", "git_capture.py",
    "manifest.py", "models.py", "reporting.py", "scanner.py", "source_verify.py", "validator.py",
}
actual_modules = {p.name for p in (phase_root / "python/fp_i00_governance").glob("*.py")}
if actual_modules != expected_modules:
    errors.append(f"python module mismatch missing={sorted(expected_modules-actual_modules)} extra={sorted(actual_modules-expected_modules)}")

tests = sorted((phase_root / "tests").glob("test_*.py"))
if len(tests) != 9:
    errors.append(f"expected 9 test modules, got {len(tests)}")

docs = sorted(doc_root.rglob("*.md")) if doc_root.exists() else []
if len(docs) != 27:
    errors.append(f"expected 27 FP-I00 delivery notes, got {len(docs)}")
for path in docs:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        errors.append(f"missing frontmatter: {path.relative_to(root)}")
    if path.parent == doc_root and path.name != "00_FP_I00_DELIVERY_MOC.md" and len(text.splitlines()) < 90:
        errors.append(f"delivery chapter too short: {path.relative_to(root)}")

concepts = sorted(concept_root.glob("EXP0019_FP_I00_*.md"))
if len(concepts) != 6:
    errors.append(f"expected 6 FP-I00 atomic concepts, got {len(concepts)}")

try:
    policy = json.loads((phase_root / "config/FP_I00_GOVERNANCE_POLICY.v1.json").read_text(encoding="utf-8"))
    if policy.get("phase_id") != "FP-I00" or policy.get("phase_version") != "1.0.0":
        errors.append("policy phase identity mismatch")
    if len(policy.get("shared_dependencies", [])) != 19:
        errors.append("policy must define 19 dependencies")
    if len(policy.get("previous_context_tests", [])) != 12:
        errors.append("policy must define 12 previous-context tests")
    if len(policy.get("phase_ownership", [])) != 4:
        errors.append("policy must define 4 ownership records")
except Exception as exc:
    errors.append(f"invalid policy: {exc}")

for rel in [
    "contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i00/artifacts/FP_I00_BASELINE_MANIFEST.v1.json",
    "contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i00/artifacts/FP_I00_SHARED_CORE_DEPENDENCY_INVENTORY.json",
    "contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i00/artifacts/FP_I00_VALIDATION_REPORT.json",
    "contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i00/artifacts/FP_I00_PHASE_STATUS.json",
    "contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i00/artifacts/FP_I00_HANDOFF_TO_FP_I01.json",
    "releases/history/exp0019/manifests/EXP0019_FP_I00_PATCH_MANIFEST.json",
    "releases/history/exp0019/reports/EXP0019_FP_I00_QA_REPORT.json",
]:
    path = root / rel
    if path.exists():
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"invalid JSON {rel}: {exc}")

try:
    report = json.loads((phase_root / "artifacts/FP_I00_VALIDATION_REPORT.json").read_text(encoding="utf-8"))
    if report.get("health") != "READY" or report.get("passed") is not True:
        errors.append("FP-I00 validation report is not READY")
    if report.get("checks_run") != 139:
        errors.append(f"expected 139 governance checks, got {report.get('checks_run')}")
except Exception as exc:
    errors.append(f"invalid validation report: {exc}")

try:
    deps = list(csv.DictReader((phase_root / "artifacts/FP_I00_SHARED_CORE_DEPENDENCY_INVENTORY.csv").open(encoding="utf-8")))
    if len(deps) != 19 or any(not row.get("aggregate_sha256") for row in deps):
        errors.append("shared-core dependency inventory is incomplete")
    if any(row.get("mutation_allowed") not in {"False", "false"} for row in deps):
        errors.append("shared-core mutation must remain false")
except Exception as exc:
    errors.append(f"invalid dependency inventory: {exc}")

try:
    prior = list(csv.DictReader((phase_root / "artifacts/FP_I00_PREVIOUS_CONTEXT_TEST_INVENTORY.csv").open(encoding="utf-8")))
    if len(prior) != 12 or any(row.get("exists") not in {"True", "true"} for row in prior):
        errors.append("previous-context test inventory is incomplete")
except Exception as exc:
    errors.append(f"invalid previous-context inventory: {exc}")

try:
    status = json.loads((phase_root / "artifacts/FP_I00_PHASE_STATUS.json").read_text(encoding="utf-8"))
    expected = {
        "python_module_count": 11,
        "python_test_module_count": 9,
        "phase_test_count": 26,
        "governance_check_count": 139,
        "shared_dependency_count": 19,
        "previous_context_test_record_count": 12,
        "delivery_note_count": 27,
        "atomic_concept_count": 6,
    }
    metrics = status.get("metrics", {})
    for key, value in expected.items():
        if metrics.get(key) != value:
            errors.append(f"status metric {key}={metrics.get(key)!r}, expected {value}")
    if status.get("runtime_authority") != "NONE" or status.get("mql5_runtime_files_added") != 0:
        errors.append("FP-I00 runtime authority boundary violated")
except Exception as exc:
    errors.append(f"invalid phase status: {exc}")

for cache in phase_root.rglob("__pycache__"):
    errors.append(f"release cache directory exists: {cache.relative_to(root)}")
for pyc in phase_root.rglob("*.pyc"):
    errors.append(f"release pyc exists: {pyc.relative_to(root)}")

if errors:
    print("\n".join(errors))
    raise SystemExit(1)
print("FP-I00 delivery validation PASS: 11 modules, 9 test modules/26 tests, 139 governance checks, 19 dependencies, 12 prior-context tests, 27 delivery notes, 6 concepts, zero runtime authority.")
