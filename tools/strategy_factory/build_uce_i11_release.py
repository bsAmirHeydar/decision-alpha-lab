#!/usr/bin/env python3
"""Build deterministic metadata and patch ZIP for UCE-I11-owned files."""
from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import argparse
import csv
import json
import zipfile

SCHEMAS = (
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
STATUS_BASE = "lab/11_strategy_factory/implementation_program/universal_context_exploitation_engine/v3_implementation"
RELEASE_META = {"UCEE_I11_FILE_INDEX.txt", "UCEE_I11_FILE_HASHES.sha256", "UCEE_I11_PATCH_MANIFEST.json"}


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def owned_paths(root: Path) -> list[Path]:
    paths: set[Path] = set()
    owned_dirs = (
        "lab/11_strategy_factory/python/strategy_factory_experiments_v3",
        "lab/11_strategy_factory/tests/phase_uce_i11_experiments",
        "lab/11_strategy_factory/examples/uce_i11",
        "docs/strategy_factory_universal_context_exploitation_engine/implementation_program/phase_deliveries/uce_i11",
        "mql5/Include/AlphaLab/StrategyFactory/ExperimentOrchestration",
    )
    for relative in owned_dirs:
        base = root / relative
        if base.exists():
            for path in base.rglob("*"):
                if path.is_file() and path.suffix != ".pyc" and "__pycache__" not in path.parts and path.name != ".DS_Store":
                    paths.add(path)

    specific = [
        "README_STRATEGY_FACTORY_UCEE_I11_IMPLEMENTATION.md",
        "INSTALL_STRATEGY_FACTORY_UCEE_I11_IMPLEMENTATION.md",
        "EXPAND_REMOVE_UCEE_I11_PATCH.ps1",
        "COMMIT_MESSAGE.md",
        "UCEE_I11_QA_REPORT.json",
        "UCEE_I11_FILE_INDEX.txt",
        "UCEE_I11_FILE_HASHES.sha256",
        "UCEE_I11_PATCH_MANIFEST.json",
        "docs/strategy_factory_universal_context_exploitation_engine/implementation_program/phases/UCE_I11_EXPERIMENT_DAG_SEARCH_AND_BUDGETING.md",
        "mql5/Experts/StrategyFactory/UCE_I11_ExperimentOrchestrationDiagnostic.mq5",
        "mql5/Experts/StrategyFactoryTests/UCE_I11_ExperimentContractsSelfTest.mq5",
        "mql5/Experts/StrategyFactoryTests/UCE_I11_BudgetAndReproSelfTest.mq5",
        "lab/11_strategy_factory/test_vectors/v3/uce_i11_experiment_conformance_vectors.json",
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
    specific.extend(f"lab/11_strategy_factory/schemas/v3/{name}.schema.json" for name in SCHEMAS)
    for path in (root / "docs/obsidian_deep/01_concepts").glob("UCE-I11*.md"):
        paths.add(path)
    for relative in specific:
        path = root / relative
        if path.is_file():
            paths.add(path)
    return sorted(paths, key=lambda path: path.relative_to(root).as_posix())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--zip", dest="zip_path")
    parser.add_argument("--phase-tests", type=int, default=59)
    parser.add_argument("--cumulative-tests", type=int, default=290)
    parser.add_argument("--engineering-checks", type=int, default=4)
    args = parser.parse_args()
    root = Path(args.root).resolve()
    generated = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    inventory = root / f"{STATUS_BASE}/artifacts/UCE_I11_ARTIFACT_INVENTORY.csv"
    inventory.parent.mkdir(parents=True, exist_ok=True)
    inventory_exclusions = RELEASE_META | {"UCE_I11_ARTIFACT_INVENTORY.csv"}
    rows = []
    for path in owned_paths(root):
        if path.name in inventory_exclusions:
            continue
        rows.append({
            "path": path.relative_to(root).as_posix(),
            "sha256": digest(path),
            "size_bytes": path.stat().st_size,
        })
    with inventory.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=("path", "sha256", "size_bytes"))
        writer.writeheader()
        writer.writerows(rows)

    # Index includes every patch-owned file, including release metadata names, so Git staging is exact.
    pre_meta_paths = [path for path in owned_paths(root) if path.name not in RELEASE_META]
    indexed_relatives = sorted({path.relative_to(root).as_posix() for path in pre_meta_paths} | RELEASE_META)
    (root / "UCEE_I11_FILE_INDEX.txt").write_text("\n".join(indexed_relatives) + "\n", encoding="utf-8")

    hash_paths = [path for path in owned_paths(root) if path.name not in {"UCEE_I11_FILE_HASHES.sha256", "UCEE_I11_PATCH_MANIFEST.json"}]
    hashes = [(path.relative_to(root).as_posix(), digest(path)) for path in hash_paths]
    (root / "UCEE_I11_FILE_HASHES.sha256").write_text(
        "\n".join(f"{value}  {relative}" for relative, value in hashes) + "\n",
        encoding="utf-8",
    )

    docs = list((root / "docs/strategy_factory_universal_context_exploitation_engine/implementation_program/phase_deliveries/uce_i11").rglob("*.md"))
    concepts = list((root / "docs/obsidian_deep/01_concepts").glob("UCE-I11*.md"))
    manifest = {
        "patch_id": "decision-alpha-lab-ucee-i11-experiment-dag-search-scheduling-budget-governance",
        "patch_version": "1.0.0",
        "phase_id": "UCE-I11",
        "created_at_utc": generated,
        "title": "Experiment DAG, Search, Scheduling, Budget, Cache, Ledger, Isolation, and Reproducibility Governance",
        "authority_boundary": "offline experiment orchestration only; no broker, order, position, or live-network authority",
        "python_module_count": 18,
        "search_adapter_count": 10,
        "native_search_adapter_count": 9,
        "public_schema_count": len(SCHEMAS),
        "delivery_document_count": len(docs),
        "atomic_concept_count": len(concepts),
        "phase_test_count": args.phase_tests,
        "cumulative_ucee_test_count": args.cumulative_tests,
        "engineering_policy_check_count": args.engineering_checks,
        "metaeditor_compile_status": "pending_local_windows",
        "file_count": len(indexed_relatives),
        "file_index": "UCEE_I11_FILE_INDEX.txt",
        "file_hashes": "UCEE_I11_FILE_HASHES.sha256",
        "next_phase": "UCE-I12 Statistical Anti-Overfit and Multiplicity Control",
    }
    (root / "UCEE_I11_PATCH_MANIFEST.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    # Regenerate index once manifest exists; all metadata are now part of the owned set.
    release_paths = owned_paths(root)
    indexed_relatives = [path.relative_to(root).as_posix() for path in release_paths]
    (root / "UCEE_I11_FILE_INDEX.txt").write_text("\n".join(indexed_relatives) + "\n", encoding="utf-8")
    manifest["file_count"] = len(indexed_relatives)
    (root / "UCEE_I11_PATCH_MANIFEST.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    # Final hashes deliberately exclude the hash file itself, but include index and manifest.
    release_paths = owned_paths(root)
    final_hash_paths = [path for path in release_paths if path.name != "UCEE_I11_FILE_HASHES.sha256"]
    (root / "UCEE_I11_FILE_HASHES.sha256").write_text(
        "\n".join(
            f"{digest(path)}  {path.relative_to(root).as_posix()}" for path in final_hash_paths
        ) + "\n",
        encoding="utf-8",
    )

    if args.zip_path:
        target = Path(args.zip_path).resolve()
        target.parent.mkdir(parents=True, exist_ok=True)
        release_paths = owned_paths(root)
        with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for path in release_paths:
                relative = path.relative_to(root).as_posix()
                info = zipfile.ZipInfo(relative, (2026, 7, 13, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = (0o644 & 0xFFFF) << 16
                archive.writestr(info, path.read_bytes())
        print(f"{target} files={len(release_paths)} sha256={digest(target)}")

    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
