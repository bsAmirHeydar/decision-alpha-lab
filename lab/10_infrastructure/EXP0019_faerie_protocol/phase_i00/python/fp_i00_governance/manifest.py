"""Baseline manifest assembly."""
from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any
import json

from .canonical import canonical_sha256, file_sha256, aggregate_files_hash
from .git_capture import capture_source_control
from .scanner import collect_files, load_json, scan_dependencies, scan_tests, scan_ownership


def build_manifest(repo: Path, policy: dict) -> dict[str, Any]:
    source_hash_contract = repo / policy["source_hash_contract"]
    owner_decisions_path = repo / policy["owner_decisions_path"]
    open_decisions_path = repo / policy["open_decisions_path"]
    relation_registry_path = repo / policy["relation_registry_path"]
    program_registry_path = repo / policy["program_registry_path"]
    documentation_files = collect_files(repo, policy["documentation_root"], [".md", ".json", ".csv", ".ini"])
    dependencies = scan_dependencies(repo, policy)
    tests = scan_tests(repo, policy)
    ownership = scan_ownership(policy)
    source_control = capture_source_control(repo, tuple(item["path_prefix"] for item in policy["phase_ownership"]))
    material = {
        "schema_version": "1.0.0",
        "phase_id": policy["phase_id"],
        "phase_version": policy["phase_version"],
        "experiment_id": policy["experiment_id"],
        "context_id": policy["context_id"],
        "authority": {
            "execution_authority": False,
            "broker_authority": False,
            "network_authority": False,
            "shared_core_mutation": False,
        },
        "source_control": asdict(source_control),
        "source_freeze": {
            "hash_contract_path": policy["source_hash_contract"],
            "hash_contract_sha256": file_sha256(source_hash_contract),
            "expected_source_count": policy["expected_source_count"],
        },
        "decision_freeze": {
            "owner_decisions_path": policy["owner_decisions_path"],
            "owner_decisions_sha256": file_sha256(owner_decisions_path),
            "owner_decisions": load_json(owner_decisions_path),
            "open_decisions_path": policy["open_decisions_path"],
            "open_decisions_sha256": file_sha256(open_decisions_path),
            "open_decisions": load_json(open_decisions_path),
        },
        "relation_registry": {
            "path": policy["relation_registry_path"],
            "sha256": file_sha256(relation_registry_path),
            "relation_count": len(load_json(relation_registry_path)["relations"]),
        },
        "implementation_program": {
            "path": policy["program_registry_path"],
            "sha256": file_sha256(program_registry_path),
            "program_id": load_json(program_registry_path)["program_id"],
            "program_version": load_json(program_registry_path)["program_version"],
        },
        "documentation_freeze": {
            "root": policy["documentation_root"],
            "file_count": len(documentation_files),
            "aggregate_sha256": aggregate_files_hash(repo, documentation_files),
        },
        "shared_dependencies": [asdict(record) for record in dependencies],
        "previous_context_tests": [asdict(record) for record in tests],
        "phase_ownership": [asdict(record) for record in ownership],
        "open_decision_ids": load_json(owner_decisions_path)["open_decision_ids"],
        "next_phase": "FP-I01",
    }
    material["manifest_hash"] = canonical_sha256(material)
    return material


def write_manifest(path: Path, manifest: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
