from __future__ import annotations
from pathlib import Path

from .canonical import file_digest, verify_embedded_digest
from .constants import EVENT_TYPES, WAVE_SIZE_LIMITS
from .io import iter_jsonl, load_json
from .resolver import ConsumerLocatorResolver


def verify_package(root: Path) -> list[str]:
    errors: list[str] = []
    required = [
        "owner_approval_registry.json",
        "consumer_wave_registry.json",
        "locator_switch_registry.json",
        "compatibility_adapter_registry.json",
        "remaining_legacy_consumer_registry.json",
        "post_cutover_mismatch_registry.json",
        "rollback_manifest.json",
        "cutover_receipt.json",
        "LCM13B_TO_LCM13C_HANDOFF.json",
        "cutover_event_ledger.jsonl",
        "records/active_consumer_bindings.jsonl",
        "records/locator_switch_records.jsonl",
        "records/compatibility_adapter_records.jsonl",
        "records/remaining_legacy_consumers.jsonl",
        "records/post_cutover_mismatches.jsonl",
        "reports/acceptance_report.json",
        "reports/hostile_review_report.json",
        "output_manifest.json",
    ]
    for relative in required:
        if not (root / relative).is_file():
            errors.append(f"MISSING:{relative}")
    if errors:
        return errors

    approval = load_json(root / "owner_approval_registry.json")
    wave_registry = load_json(root / "consumer_wave_registry.json")
    locator_registry = load_json(root / "locator_switch_registry.json")
    compatibility_registry = load_json(root / "compatibility_adapter_registry.json")
    remaining_registry = load_json(root / "remaining_legacy_consumer_registry.json")
    mismatch_registry = load_json(root / "post_cutover_mismatch_registry.json")
    rollback_manifest = load_json(root / "rollback_manifest.json")
    receipt = load_json(root / "cutover_receipt.json")
    handoff = load_json(root / "LCM13B_TO_LCM13C_HANDOFF.json")
    acceptance = load_json(root / "reports/acceptance_report.json")
    hostile = load_json(root / "reports/hostile_review_report.json")
    output_manifest = load_json(root / "output_manifest.json")

    digest_fields = [
        (approval, "approval_digest"),
        (wave_registry, "registry_digest"),
        (locator_registry, "registry_digest"),
        (compatibility_registry, "registry_digest"),
        (remaining_registry, "registry_digest"),
        (mismatch_registry, "registry_digest"),
        (rollback_manifest, "rollback_manifest_digest"),
        (receipt, "cutover_receipt_digest"),
        (handoff, "handoff_digest"),
        (acceptance, "report_digest"),
        (hostile, "report_digest"),
        (output_manifest, "output_manifest_digest"),
    ]
    for value, field in digest_fields:
        if not verify_embedded_digest(value, field):
            errors.append(f"DIGEST:{field}")

    bindings = list(iter_jsonl(root / "records/active_consumer_bindings.jsonl"))
    switches = list(iter_jsonl(root / "records/locator_switch_records.jsonl"))
    adapters = list(iter_jsonl(root / "records/compatibility_adapter_records.jsonl"))
    blocked = list(iter_jsonl(root / "records/remaining_legacy_consumers.jsonl"))
    post_mismatches = list(iter_jsonl(root / "records/post_cutover_mismatches.jsonl"))
    events = list(iter_jsonl(root / "cutover_event_ledger.jsonl"))

    if len(bindings) != 613:
        errors.append(f"BINDING_COUNT:{len(bindings)}")
    if len(switches) != 613:
        errors.append(f"SWITCH_COUNT:{len(switches)}")
    if len(adapters) != 613:
        errors.append(f"ADAPTER_COUNT:{len(adapters)}")
    if len(blocked) != 806:
        errors.append(f"BLOCKED_COUNT:{len(blocked)}")
    if post_mismatches:
        errors.append("POST_MISMATCH_NONZERO")
    if len({row["consumer_id"] for row in bindings}) != len(bindings):
        errors.append("DUPLICATE_BINDING_CONSUMER")
    if {row["consumer_id"] for row in bindings} & {row["consumer_id"] for row in blocked}:
        errors.append("CUTOVER_BLOCKED_OVERLAP")

    waves = wave_registry.get("waves", [])
    if wave_registry.get("wave_count") != len(waves):
        errors.append("WAVE_COUNT")
    wave_ids = {row["wave_id"] for row in waves}
    if {row["wave_id"] for row in bindings} != wave_ids:
        errors.append("BINDING_WAVE_COVERAGE")
    for wave in waves:
        plan_path = root / "consumer_wave_plans" / f"{wave['wave_id']}.json"
        manifest_path = root / "consumer_cutover_manifests" / f"{wave['wave_id']}.json"
        health_path = root / "post_cutover_health_reports" / f"{wave['wave_id']}.json"
        receipt_path = root / "locator_switch_receipts" / f"{wave['wave_id']}.json"
        rollback_path = root / "rollback_packages" / f"{wave['wave_id']}.json"
        for path in [plan_path, manifest_path, health_path, receipt_path, rollback_path]:
            if not path.is_file():
                errors.append(f"WAVE_FILE_MISSING:{path.name}")
                continue
        if not plan_path.is_file():
            continue
        plan = load_json(plan_path)
        manifest = load_json(manifest_path)
        health = load_json(health_path)
        wave_receipt = load_json(receipt_path)
        rollback = load_json(rollback_path)
        if plan["consumer_count"] > WAVE_SIZE_LIMITS[plan["domain"]]:
            errors.append(f"WAVE_LIMIT:{plan['wave_id']}")
        if plan["consumer_ids"] != manifest["consumer_ids"]:
            errors.append(f"PLAN_MANIFEST:{plan['wave_id']}")
        if health["observation_status"] != "PASS" or health["post_switch_high_critical_mismatch_count"] != 0:
            errors.append(f"HEALTH:{plan['wave_id']}")
        if wave_receipt["receipt_status"] != "PASS" or wave_receipt["partial_switch_count"] != 0:
            errors.append(f"RECEIPT:{plan['wave_id']}")
        if rollback["preverified"] is not True:
            errors.append(f"ROLLBACK:{plan['wave_id']}")

    if len(events) != len(waves) * len(EVENT_TYPES):
        errors.append("EVENT_COUNT")
    if [row["event_sequence"] for row in events] != list(range(1, len(events) + 1)):
        errors.append("EVENT_SEQUENCE")

    resolver = ConsumerLocatorResolver(root / "records/active_consumer_bindings.jsonl")
    for binding in bindings:
        resolved = resolver.resolve(binding["consumer_id"])
        if resolved.resolved_locator != binding["active_locator"]:
            errors.append(f"RESOLUTION:{binding['consumer_id']}")
        if resolved.fallback_locator != binding["prior_locator"]:
            errors.append(f"FALLBACK:{binding['consumer_id']}")
        if resolved.runtime_authority or resolved.live_order_authority or resolved.capital_authority:
            errors.append(f"AUTHORITY:{binding['consumer_id']}")

    if acceptance.get("passed") is not True:
        errors.append("ACCEPTANCE")
    if hostile.get("result") != "PASS":
        errors.append("HOSTILE")
    if handoff.get("consumer_cutover_performed") is not True:
        errors.append("HANDOFF_CUTOVER")
    if handoff.get("rollback_rehearsal_performed") is not False:
        errors.append("HANDOFF_ROLLBACK_STATE")
    for artifact in [acceptance, hostile, handoff, receipt]:
        if artifact.get("runtime_authority_created") is True or artifact.get("live_order_authority_created") is True or artifact.get("capital_authority_created") is True:
            errors.append("AUTHORITY_CREATED")

    for item in output_manifest.get("files", []):
        path = root / item["path"]
        if not path.is_file():
            errors.append(f"OUTPUT_MISSING:{item['path']}")
        elif file_digest(path) != item["sha256"]:
            errors.append(f"OUTPUT_DIGEST:{item['path']}")
    return errors
