from __future__ import annotations

from .adapter_contracts import verify as verify_adapter
from .authority import verify_permit
from .canonical import digest_object, sha256_bytes
from .errors import IntegrityError
from .io import read_json, read_jsonl


def _verify_digest(obj: dict, field: str, label: str) -> None:
    if digest_object(obj, field) != obj.get(field):
        raise IntegrityError(f"{label} digest invalid")


def _verify_jsonl_digests(records: list[dict], field: str, label: str) -> None:
    for index, record in enumerate(records, 1):
        _verify_digest(record, field, f"{label} {index}")


def verify_package(root):
    if root.is_symlink() or not root.is_dir():
        raise IntegrityError("framework root missing or symlinked")

    marker = read_json(root / "framework_marker.json")
    handoff = read_json(root / "handoff/lcm06_to_lcm07_handoff.json")
    receipt = read_json(root / "framework_receipt.json")
    manifest = read_json(root / "output_manifest.json")
    permit = read_json(root / "authority/authority_permit.json")

    seen: set[str] = set()
    for record in manifest.get("artifacts", []):
        relative_path = record["path"]
        if relative_path in seen:
            raise IntegrityError(f"duplicate manifest path: {relative_path}")
        seen.add(relative_path)
        path = root / relative_path
        if path.is_symlink():
            raise IntegrityError(f"manifest symlink forbidden: {relative_path}")
        if not path.is_file():
            raise IntegrityError(f"manifest missing: {relative_path}")
        if path.stat().st_size != record["size_bytes"] or sha256_bytes(path.read_bytes()) != record["sha256"]:
            raise IntegrityError(f"manifest mismatch: {relative_path}")
    if manifest.get("artifact_count") != len(seen):
        raise IntegrityError("manifest artifact count invalid")

    _verify_digest(manifest, "output_manifest_digest", "manifest")
    _verify_digest(marker, "marker_digest", "marker")
    _verify_digest(handoff, "handoff_digest", "handoff")
    _verify_digest(receipt, "receipt_digest", "receipt")

    if marker.get("phase_id") != "LCM-06" or marker.get("framework_run_id") != root.name:
        raise IntegrityError("framework marker phase or run binding invalid")
    if marker.get("claim_ceiling") != "MIGRATION_FRAMEWORK_REFERENCE_ONLY":
        raise IntegrityError("framework claim ceiling invalid")
    if handoff.get("handoff_type") != "LCM06_TO_LCM07":
        raise IntegrityError("handoff type invalid")
    verify_permit(permit, marker["source_handoff_digest"], marker["topology_run_id"])

    binding = read_json(root / "input/lcm05_binding.json")
    _verify_digest(binding, "binding_digest", "LCM-05 binding")
    if binding.get("source_handoff_digest") != marker.get("source_handoff_digest"):
        raise IntegrityError("LCM-05 binding source mismatch")
    if binding.get("topology_run_id") != marker.get("topology_run_id"):
        raise IntegrityError("LCM-05 binding topology mismatch")
    if binding.get("target_materialization_allowed") is not False:
        raise IntegrityError("LCM-05 binding authority escalation")

    for path in sorted((root / "registries").glob("*.json")):
        registry = read_json(path)
        _verify_digest(registry, "registry_digest", path.name)
        if registry.get("closed") is not True:
            raise IntegrityError(f"open registry forbidden: {path.name}")
    for path in sorted((root / "contracts").glob("*.json")):
        contract = read_json(path)
        _verify_digest(contract, "contract_digest", path.name)
        if contract.get("source_mutation_allowed") is not False or contract.get("authority_expansion_allowed") is not False:
            raise IntegrityError(f"contract authority escalation: {path.name}")

    summary = read_json(root / "reports/framework_summary.json")
    acceptance = read_json(root / "reports/acceptance_report.json")
    hostile = read_json(root / "reports/hostile_review.json")
    events = read_json(root / "events/framework_event_ledger.json")
    provenance = read_json(root / "provenance/framework_provenance_graph.json")
    move_plan = read_json(root / "movement/reference_move_plan.json")
    _verify_digest(summary, "summary_digest", "summary")
    _verify_digest(acceptance, "acceptance_digest", "acceptance")
    _verify_digest(hostile, "hostile_review_digest", "hostile review")
    _verify_digest(events, "ledger_digest", "event ledger")
    _verify_digest(provenance, "provenance_digest", "provenance")
    _verify_digest(move_plan, "move_plan_digest", "move plan")

    previous = None
    for index, event in enumerate(events.get("events", []), 1):
        if event.get("sequence") != index or event.get("previous_event_digest") != previous:
            raise IntegrityError("event chain ordering invalid")
        _verify_digest(event, "event_digest", f"event {index}")
        for authority_field in (
            "source_move_authority",
            "source_delete_authority",
            "target_materialization_authority",
            "semantic_refactor_authority",
            "runtime_authority",
            "live_order_authority",
            "capital_authority",
        ):
            if event.get(authority_field) is not False:
                raise IntegrityError(f"event authority escalation: {authority_field}")
        previous = event["event_digest"]
    if events.get("event_count") != len(events.get("events", [])) or previous != events.get("final_event_digest"):
        raise IntegrityError("event chain final binding invalid")

    packet_results = read_jsonl(root / "validation/migration_packet_validation_results.jsonl")
    alias_results = read_jsonl(root / "resolution/alias_resolution_results.jsonl")
    comparisons = read_jsonl(root / "parity/trace_comparison_results.jsonl")
    adapters = read_jsonl(root / "adapters/reference_adapter_contracts.jsonl")
    redirects = read_jsonl(root / "redirects/reference_redirect_previews.jsonl")
    quarantine = read_jsonl(root / "quarantine/quarantine_validation_results.jsonl")
    deletion = read_jsonl(root / "deletion/deletion_validation_results.jsonl")

    _verify_jsonl_digests(packet_results, "validation_digest", "packet result")
    _verify_jsonl_digests(alias_results, "resolver_digest", "alias result")
    _verify_jsonl_digests(comparisons, "comparison_digest", "trace comparison")
    _verify_jsonl_digests(redirects, "redirect_digest", "redirect preview")
    _verify_jsonl_digests(quarantine, "validation_digest", "quarantine result")
    _verify_jsonl_digests(deletion, "validation_digest", "deletion result")
    for adapter in adapters:
        verify_adapter(adapter)

    if any(item.get("hard_mismatch_waived") is not False for item in comparisons):
        raise IntegrityError("hard mismatch waiver detected")
    if any(item.get("write_performed") is not False for item in redirects):
        raise IntegrityError("redirect write detected")
    if any(item.get("delete_performed") is not False for item in deletion):
        raise IntegrityError("delete execution detected")
    if any(item.get("source_move_performed") is not False or item.get("source_delete_performed") is not False for item in quarantine):
        raise IntegrityError("quarantine mutation detected")
    if move_plan.get("execute_allowed") is not False or move_plan.get("target_materialization_allowed") is not False:
        raise IntegrityError("move plan execution authority detected")

    immutable_false_fields = (
        "target_materialization_performed",
        "source_move_performed",
        "source_delete_performed",
        "semantic_refactor_performed",
        "merge_performed",
        "cutover_performed",
        "runtime_authority_created",
        "live_order_authority_created",
        "capital_authority_created",
    )
    for field in immutable_false_fields:
        if summary.get(field) is not False or receipt.get(field) is not False:
            raise IntegrityError(f"authority or mutation escalation: {field}")

    if acceptance.get("acceptance_gate_passed") is not True or acceptance.get("target_materialization_allowed") is not False:
        raise IntegrityError("acceptance boundary invalid")
    if hostile.get("hostile_review_passed") is not True or any(check.get("passed") is not True for check in hostile.get("checks", [])):
        raise IntegrityError("hostile review invalid")
    if receipt.get("handoff_digest") != handoff.get("handoff_digest"):
        raise IntegrityError("receipt handoff binding invalid")
    if receipt.get("framework_summary_digest") != summary.get("summary_digest"):
        raise IntegrityError("receipt summary binding invalid")
    if receipt.get("acceptance_report_digest") != acceptance.get("acceptance_digest"):
        raise IntegrityError("receipt acceptance binding invalid")
    if marker.get("framework_run_id") != summary.get("framework_run_id") or marker.get("framework_run_id") != handoff.get("framework_run_id"):
        raise IntegrityError("framework run binding invalid")
    if provenance.get("reaches_lcm05_topology") is not True or provenance.get("source_moved") is not False or provenance.get("source_deleted") is not False:
        raise IntegrityError("provenance boundary invalid")
    if handoff.get("shared_engine_extraction_authorized") is not False or handoff.get("target_materialization_allowed") is not False:
        raise IntegrityError("handoff authority escalation")

    return {
        "passed": True,
        "framework_run_id": marker["framework_run_id"],
        "manifest_artifact_count": manifest["artifact_count"],
        "packet_result_count": len(packet_results),
        "alias_result_count": len(alias_results),
        "trace_comparison_count": len(comparisons),
        "adapter_contract_count": len(adapters),
        "redirect_preview_count": len(redirects),
        "quarantine_validation_count": len(quarantine),
        "deletion_validation_count": len(deletion),
        "event_count": events["event_count"],
        "registry_count": len(list((root / "registries").glob("*.json"))),
        "contract_count": len(list((root / "contracts").glob("*.json"))),
    }
