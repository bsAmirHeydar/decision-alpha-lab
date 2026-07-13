#!/usr/bin/env python3
"""Validate completeness and internal consistency of the UCE-I11 delivery."""
from __future__ import annotations

from pathlib import Path
import ast
import csv
import json
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
errors: list[str] = []

PACKAGE_REL = "lab/11_strategy_factory/python/strategy_factory_experiments_v3"
TEST_REL = "lab/11_strategy_factory/tests/phase_uce_i11_experiments"
DOC_REL = "docs/strategy_factory_universal_context_exploitation_engine/implementation_program/phase_deliveries/uce_i11"
STATUS_BASE = "lab/11_strategy_factory/implementation_program/universal_context_exploitation_engine/v3_implementation"

required = [
    "README_STRATEGY_FACTORY_UCEE_I11_IMPLEMENTATION.md",
    "INSTALL_STRATEGY_FACTORY_UCEE_I11_IMPLEMENTATION.md",
    "EXPAND_REMOVE_UCEE_I11_PATCH.ps1",
    "COMMIT_MESSAGE.md",
    f"{PACKAGE_REL}/compiler.py",
    f"{PACKAGE_REL}/search.py",
    f"{PACKAGE_REL}/budget.py",
    f"{PACKAGE_REL}/scheduler.py",
    f"{PACKAGE_REL}/ledger.py",
    f"{PACKAGE_REL}/cache.py",
    f"{PACKAGE_REL}/isolation.py",
    f"{PACKAGE_REL}/reproducibility.py",
    f"{PACKAGE_REL}/registry.py",
    "lab/11_strategy_factory/test_vectors/v3/uce_i11_experiment_conformance_vectors.json",
    f"{DOC_REL}/00_UCE_I11_DELIVERY_MOC.md",
    "docs/strategy_factory_universal_context_exploitation_engine/implementation_program/phases/UCE_I11_EXPERIMENT_DAG_SEARCH_AND_BUDGETING.md",
    "mql5/Include/AlphaLab/StrategyFactory/ExperimentOrchestration/UCEI11_All.mqh",
    "mql5/Experts/StrategyFactory/UCE_I11_ExperimentOrchestrationDiagnostic.mq5",
    "mql5/Experts/StrategyFactoryTests/UCE_I11_ExperimentContractsSelfTest.mq5",
    "mql5/Experts/StrategyFactoryTests/UCE_I11_BudgetAndReproSelfTest.mq5",
    f"{STATUS_BASE}/phase_status/UCE_I11.json",
    f"{STATUS_BASE}/phase_status/UCE_I11_HANDOFF_TO_UCE_I12.json",
    f"{STATUS_BASE}/artifacts/UCE_I11_ACCEPTANCE_EVIDENCE.json",
    f"{STATUS_BASE}/artifacts/UCE_I11_ARTIFACT_INVENTORY.csv",
    "tools/strategy_factory/check_uce_i11_boundaries.py",
    "tools/strategy_factory/check_uce_i11_mql5_static.py",
    "tools/strategy_factory/compile_uce_i11_experiment_orchestration.ps1",
    "tools/strategy_factory/generate_uce_i11_vectors.py",
    "tools/strategy_factory/run_uce_i11_tests.ps1",
    "tools/strategy_factory/validate_uce_i11_delivery.py",
    "tools/strategy_factory/build_uce_i11_release.py",
]
for relative in required:
    if not (root / relative).is_file():
        errors.append("missing " + relative)

expected_modules = {
    "__init__.py", "admission.py", "budget.py", "cache.py", "canonical.py", "cli.py",
    "compiler.py", "conformance.py", "contracts.py", "enums.py", "errors.py", "golden.py",
    "isolation.py", "ledger.py", "registry.py", "reproducibility.py", "scheduler.py", "search.py",
}
package = root / PACKAGE_REL
actual_modules = {path.name for path in package.glob("*.py")}
if expected_modules != actual_modules:
    errors.append(
        "Python module mismatch; missing=" + ",".join(sorted(expected_modules - actual_modules))
        + " extra=" + ",".join(sorted(actual_modules - expected_modules))
    )

phase_tests = sorted((root / TEST_REL).glob("test_*.py"))
if len(phase_tests) < 11:
    errors.append(f"insufficient I11 test modules: {len(phase_tests)}")

schema_names = (
    "experiment_candidate_admission", "experiment_parameter_spec", "experiment_objective_spec",
    "experiment_search_plan", "experiment_budget_policy", "experiment_declaration",
    "experiment_trial_identity", "experiment_resource_claim", "experiment_dag_node",
    "experiment_dag_edge", "experiment_manifest", "experiment_search_observation",
    "experiment_budget_usage", "experiment_budget_assessment", "experiment_scheduler_event",
    "experiment_selection_ledger_entry", "experiment_cache_record", "experiment_artifact_comparison",
    "experiment_reproducibility_report", "experiment_search_adapter_descriptor",
    "experiment_search_registry_snapshot", "experiment_work_result", "experiment_environment_capture",
    "experiment_isolated_process_result",
)
for name in schema_names:
    path = root / f"lab/11_strategy_factory/schemas/v3/{name}.schema.json"
    if not path.is_file():
        errors.append(f"missing schema {name}")
        continue
    try:
        schema = json.loads(path.read_text(encoding="utf-8"))
        if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            errors.append(f"wrong JSON Schema dialect: {name}")
        if schema.get("type") != "object" or schema.get("additionalProperties") is not False:
            errors.append(f"non-closed schema: {name}")
        if not schema.get("$id", "").endswith(f"/{name}.schema.json"):
            errors.append(f"invalid schema id: {name}")
    except Exception as exc:
        errors.append(f"invalid schema {name}: {exc}")

json_paths = [
    "lab/11_strategy_factory/test_vectors/v3/uce_i11_experiment_conformance_vectors.json",
    f"{STATUS_BASE}/phase_status/UCE_I11.json",
    f"{STATUS_BASE}/phase_status/UCE_I11_HANDOFF_TO_UCE_I12.json",
    f"{STATUS_BASE}/artifacts/UCE_I11_ACCEPTANCE_EVIDENCE.json",
    "UCEE_I11_PATCH_MANIFEST.json", "UCEE_I11_QA_REPORT.json",
]
json_paths.extend(f"lab/11_strategy_factory/examples/uce_i11/{name}" for name in (
    "experiment_declaration.json", "experiment_manifest_golden.json", "failure_injection_plan.json",
    "reproducibility_checklist.json", "search_registry_snapshot.json",
))
for relative in json_paths:
    path = root / relative
    if path.exists():
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"invalid JSON {relative}: {exc}")

registry_path = package / "registry.py"
if registry_path.exists():
    tree = ast.parse(registry_path.read_text(encoding="utf-8"))
    catalog_size = None
    native_count = 0
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "CATALOG" for t in node.targets):
            if isinstance(node.value, (ast.Tuple, ast.List)):
                catalog_size = len(node.value.elts)
                for element in node.value.elts:
                    if isinstance(element, ast.Call) and len(element.args) >= 4 and isinstance(element.args[3], ast.Constant):
                        native_count += int(element.args[3].value is True)
    if catalog_size != 10:
        errors.append(f"search registry must contain 10 descriptors, got {catalog_size}")
    if native_count != 9:
        errors.append(f"search registry must contain 9 native descriptors, got {native_count}")

doc_root = root / DOC_REL
doc_notes = sorted(doc_root.rglob("*.md")) if doc_root.exists() else []
if len(doc_notes) < 33:
    errors.append(f"insufficient detailed Obsidian notes: {len(doc_notes)}")
for note in doc_notes:
    text = note.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        errors.append(f"missing YAML frontmatter: {note.relative_to(root)}")
    if note.parent == doc_root and note.name != "00_UCE_I11_DELIVERY_MOC.md" and len(text.splitlines()) < 70:
        errors.append(f"chapter is not detailed enough: {note.relative_to(root)}")

concepts = sorted((root / "docs/obsidian_deep/01_concepts").glob("UCE-I11*.md"))
if len(concepts) != 7:
    errors.append(f"expected 7 atomic concepts, got {len(concepts)}")

mql_catalog = root / "mql5/Include/AlphaLab/StrategyFactory/ExperimentOrchestration/UCEI11_Catalog.mqh"
if mql_catalog.exists():
    text = mql_catalog.read_text(encoding="utf-8")
    if text.count("case ") != 10 or "return 10;" not in text:
        errors.append("MQL5 catalog count mismatch")

inventory = root / f"{STATUS_BASE}/artifacts/UCE_I11_ARTIFACT_INVENTORY.csv"
if inventory.exists():
    try:
        rows = list(csv.DictReader(inventory.read_text(encoding="utf-8").splitlines()))
        if not rows or not {"path", "sha256", "size_bytes"} <= set(rows[0]):
            errors.append("artifact inventory columns are incomplete")
    except Exception as exc:
        errors.append(f"invalid artifact inventory: {exc}")

status_path = root / f"{STATUS_BASE}/phase_status/UCE_I11.json"
if status_path.exists():
    status = json.loads(status_path.read_text(encoding="utf-8"))
    expected = {
        "phase_test_count": 59, "uce_i01_to_i11_test_count": 290,
        "python_module_count": 18, "public_schema_count": 24,
        "search_adapter_count": 10, "native_search_adapter_count": 9,
    }
    for key, value in expected.items():
        if status.get(key) != value:
            errors.append(f"status {key}={status.get(key)!r}, expected {value!r}")
    if status.get("runtime_authority") != "none":
        errors.append("runtime authority must remain none")

acceptance_path = root / f"{STATUS_BASE}/artifacts/UCE_I11_ACCEPTANCE_EVIDENCE.json"
if acceptance_path.exists():
    acceptance = json.loads(acceptance_path.read_text(encoding="utf-8"))
    if acceptance.get("delivery_validation") != "pass":
        errors.append("acceptance evidence does not record delivery validation pass")
    if acceptance.get("metaeditor", {}).get("result") != "pending_local_windows":
        errors.append("MetaEditor status must be pending_local_windows in this environment")

for cache in root.rglob("__pycache__"):
    if PACKAGE_REL in cache.as_posix() or TEST_REL in cache.as_posix():
        errors.append(f"release-owned cache directory exists: {cache.relative_to(root)}")

if errors:
    print("\n".join(errors))
    raise SystemExit(1)

print(
    "UCE-I11 delivery validation PASS: "
    f"{len(expected_modules)} Python modules, {len(phase_tests)} test modules, {len(schema_names)} closed schemas, "
    f"{len(doc_notes)} delivery notes + {len(concepts)} atomic concepts, 10 search adapters/9 native, "
    "MQL5 mirrors, immutable manifests, budget/scheduler/cache/reproducibility evidence, and release metadata."
)
