from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _jsonl(path: Path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _latest_framework(repo_root: Path) -> Path | None:
    roots = sorted((repo_root / "registry/history/lcm/frameworks").glob("FRAMEWORK_*"))
    roots = [root for root in roots if root.is_dir() and not root.is_symlink()]
    return roots[-1] if roots else None


def validate(repo_root):
    repo_root = Path(repo_root)
    schema_root = repo_root / "registry/history/lcm/lcm_06/schemas/v1"
    schemas: dict[str, dict] = {}
    for path in sorted(schema_root.glob("*.schema.json")):
        schema = _load(path)
        Draft202012Validator.check_schema(schema)
        schemas[path.name.removesuffix(".schema.json")] = schema

    framework_root = _latest_framework(repo_root)
    instances: list[tuple[str, dict, str]] = []
    if framework_root is not None:
        instances.extend(
            [
                ("framework_marker", _load(framework_root / "framework_marker.json"), "framework_marker.json"),
                ("authority_permit", _load(framework_root / "authority/authority_permit.json"), "authority permit"),
                ("lcm05_binding", _load(framework_root / "input/lcm05_binding.json"), "LCM-05 binding"),
                ("framework_summary", _load(framework_root / "reports/framework_summary.json"), "framework summary"),
                ("acceptance_report", _load(framework_root / "reports/acceptance_report.json"), "acceptance report"),
                ("hostile_review", _load(framework_root / "reports/hostile_review.json"), "hostile review"),
                ("event_ledger", _load(framework_root / "events/framework_event_ledger.json"), "event ledger"),
                ("provenance_graph", _load(framework_root / "provenance/framework_provenance_graph.json"), "provenance graph"),
                ("handoff", _load(framework_root / "handoff/lcm06_to_lcm07_handoff.json"), "handoff"),
                ("output_manifest", _load(framework_root / "output_manifest.json"), "output manifest"),
                ("receipt", _load(framework_root / "framework_receipt.json"), "receipt"),
                ("move_plan", _load(framework_root / "movement/reference_move_plan.json"), "move plan"),
            ]
        )
        for path in sorted((framework_root / "registries").glob("*.json")):
            instances.append(("registry", _load(path), path.name))
        for path in sorted((framework_root / "contracts").glob("*.json")):
            instances.append(("contract", _load(path), path.name))
        for record in _jsonl(framework_root / "validation/migration_packet_validation_results.jsonl"):
            instances.append(("packet_validation_result", record, "packet validation result"))
        for record in _jsonl(framework_root / "resolution/alias_resolution_results.jsonl"):
            instances.append(("alias_resolution_result", record, "alias resolution result"))
        for record in _jsonl(framework_root / "parity/trace_comparison_results.jsonl"):
            instances.append(("trace_comparison_result", record, "trace comparison result"))
        for record in _jsonl(framework_root / "adapters/reference_adapter_contracts.jsonl"):
            instances.append(("adapter_contract", record, "adapter contract"))
        for record in _jsonl(framework_root / "redirects/reference_redirect_previews.jsonl"):
            instances.append(("redirect_preview", record, "redirect preview"))
        for record in _jsonl(framework_root / "quarantine/quarantine_validation_results.jsonl"):
            instances.append(("quarantine_validation_result", record, "quarantine result"))
        for record in _jsonl(framework_root / "deletion/deletion_validation_results.jsonl"):
            instances.append(("deletion_validation_result", record, "deletion result"))

    fixture_root = repo_root / "tests/legacy/strategy_factory/migration/fixtures/lcm_06"
    if fixture_root.is_dir():
        for record in _jsonl(fixture_root / "packets/reference_migration_packets.jsonl"):
            instances.append(("migration_packet", record, "migration packet fixture"))
        instances.append(("fixture_alias_registry", _load(fixture_root / "aliases/reference_alias_records.json"), "alias fixture registry"))
        for path in sorted((fixture_root / "traces").glob("*.json")):
            instances.append(("trace_bundle", _load(path), path.name))
        instances.append(("fixture_quarantine_bundle", _load(fixture_root / "quarantine/reference_quarantine_records.json"), "quarantine fixture bundle"))
        instances.append(("fixture_deletion_bundle", _load(fixture_root / "deletion/reference_deletion_records.json"), "deletion fixture bundle"))

    errors: list[dict] = []
    for schema_name, instance, label in instances:
        schema = schemas.get(schema_name)
        if schema is None:
            errors.append({"label": label, "error": f"schema missing: {schema_name}"})
            continue
        validator = Draft202012Validator(schema)
        for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.absolute_path)):
            errors.append({"label": label, "schema": schema_name, "path": list(error.absolute_path), "error": error.message})

    return {
        "passed": bool(schemas) and not errors,
        "schema_count": len(schemas),
        "instance_count": len(instances),
        "errors": errors,
    }
