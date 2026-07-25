from __future__ import annotations

from pathlib import Path

from .canonical import file_digest, verify_embedded_digest
from .constants import CLAIM_CEILING, CLOSURE_STATES, EVENT_TYPES, PHASE_ID, STATE_PLANES
from .io import iter_jsonl, load_json

REQUIRED_FILES = (
    "state_recovery_registry.json",
    "cutover_closure_registry.json",
    "deprecation_candidate_registry.json",
    "remaining_legacy_blocker_registry.json",
    "cutover_closure_receipt.json",
    "rollback_manifest.json",
    "LCM13C_TO_LCM14A_HANDOFF.json",
    "residual_cutover_risk.md",
    "closure_event_ledger.jsonl",
    "records/state_recovery_records.jsonl",
    "records/cutover_closure_records.jsonl",
    "records/deprecation_candidate_records.jsonl",
    "reports/acceptance_report.json",
    "reports/hostile_review_report.json",
    "output_manifest.json",
)


def _authority_breach(value: dict) -> bool:
    return any(
        value.get(key) is True
        for key in (
            "quarantine_authority_created",
            "deletion_authority_created",
            "runtime_authority_created",
            "live_order_authority_created",
            "capital_authority_created",
        )
    )


def verify_package(root: Path) -> list[str]:
    errors: list[str] = []
    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            errors.append(f"MISSING:{relative}")
    if errors:
        return errors

    named = {
        "state": (load_json(root / "state_recovery_registry.json"), "registry_digest"),
        "closure": (load_json(root / "cutover_closure_registry.json"), "registry_digest"),
        "deprecation": (load_json(root / "deprecation_candidate_registry.json"), "registry_digest"),
        "blocker": (load_json(root / "remaining_legacy_blocker_registry.json"), "registry_digest"),
        "receipt": (load_json(root / "cutover_closure_receipt.json"), "closure_receipt_digest"),
        "rollback": (load_json(root / "rollback_manifest.json"), "rollback_manifest_digest"),
        "handoff": (load_json(root / "LCM13C_TO_LCM14A_HANDOFF.json"), "handoff_digest"),
        "acceptance": (load_json(root / "reports/acceptance_report.json"), "report_digest"),
        "hostile": (load_json(root / "reports/hostile_review_report.json"), "report_digest"),
        "output": (load_json(root / "output_manifest.json"), "output_manifest_digest"),
    }
    for name, (value, field) in named.items():
        if value.get("phase_id") != PHASE_ID:
            errors.append(f"PHASE:{name}")
        if value.get("claim_ceiling") != CLAIM_CEILING:
            errors.append(f"CLAIM:{name}")
        if value.get("validation_status") != "PASS":
            errors.append(f"STATUS:{name}")
        if not verify_embedded_digest(value, field):
            errors.append(f"DIGEST:{name}:{field}")
        if _authority_breach(value):
            errors.append(f"AUTHORITY:{name}")

    state_registry = named["state"][0]
    closure_registry = named["closure"][0]
    deprecation_registry = named["deprecation"][0]
    blocker_registry = named["blocker"][0]
    receipt = named["receipt"][0]
    handoff = named["handoff"][0]
    acceptance = named["acceptance"][0]
    hostile = named["hostile"][0]
    output_manifest = named["output"][0]

    states = list(iter_jsonl(root / "records/state_recovery_records.jsonl"))
    closures = list(iter_jsonl(root / "records/cutover_closure_records.jsonl"))
    candidates = list(iter_jsonl(root / "records/deprecation_candidate_records.jsonl"))
    events = list(iter_jsonl(root / "closure_event_ledger.jsonl"))

    if len(closures) != 27:
        errors.append("WAVE_COUNT")
    if len(states) != 27 * len(STATE_PLANES):
        errors.append("STATE_COUNT")
    if len(candidates) != 613:
        errors.append("DEPRECATION_COUNT")
    if len(events) != 27 * len(EVENT_TYPES):
        errors.append("EVENT_COUNT")
    if blocker_registry.get("remaining_legacy_consumer_count") != 806:
        errors.append("BLOCKER_COUNT")

    expected_counts = {
        state: sum(row.get("closure_state") == state for row in closures)
        for state in CLOSURE_STATES
    }
    if closure_registry.get("closure_counts") != expected_counts:
        errors.append("CLOSURE_COUNTS")
    if expected_counts["REOPEN_REQUIRED"] != 0:
        errors.append("REOPEN_REQUIRED")
    if closure_registry.get("consumer_count") != 613:
        errors.append("CLOSURE_CONSUMER_COUNT")

    wave_ids = {row["wave_id"] for row in closures}
    if len(wave_ids) != 27:
        errors.append("WAVE_ID_UNIQUENESS")
    for row in closures:
        if not row.get("rollback_verified") or not row.get("forward_recovery_verified"):
            errors.append(f"REVERSIBILITY:{row.get('wave_id')}")
        if not row.get("persistent_state_ownership_verified"):
            errors.append(f"STATE_OWNERSHIP:{row.get('wave_id')}")
        wave_id = row["wave_id"]
        if not (root / "rollback_rehearsal_reports" / f"{wave_id}.json").is_file():
            errors.append(f"ROLLBACK_REPORT:{wave_id}")
        if not (root / "forward_recovery_reports" / f"{wave_id}.json").is_file():
            errors.append(f"FORWARD_REPORT:{wave_id}")

    state_pairs = {(row["wave_id"], row["state_plane"]) for row in states}
    expected_pairs = {(wave_id, plane) for wave_id in wave_ids for plane in STATE_PLANES}
    if state_pairs != expected_pairs:
        errors.append("STATE_PLANE_COVERAGE")
    if any(row.get("live_state_mutation_performed") is not False for row in states):
        errors.append("LIVE_STATE_MUTATION")
    if state_registry.get("state_record_count") != len(states):
        errors.append("STATE_REGISTRY_COUNT")

    candidate_ids = {row["consumer_id"] for row in candidates}
    if len(candidate_ids) != 613:
        errors.append("CANDIDATE_UNIQUENESS")
    for row in candidates:
        if not verify_embedded_digest(row, "candidate_digest"):
            errors.append(f"CANDIDATE_DIGEST:{row.get('consumer_id')}")
        if row.get("quarantine_authorized") or row.get("deletion_authorized"):
            errors.append(f"CANDIDATE_AUTHORITY:{row.get('consumer_id')}")
    if deprecation_registry.get("candidate_count") != len(candidates):
        errors.append("DEPRECATION_REGISTRY_COUNT")
    if deprecation_registry.get("deletion_authorized_count") != 0:
        errors.append("DELETION_AUTHORITY")

    if [row["event_sequence"] for row in events] != list(range(1, len(events) + 1)):
        errors.append("EVENT_SEQUENCE")
    if {row["event_type"] for row in events} != set(EVENT_TYPES):
        errors.append("EVENT_TYPE_COVERAGE")
    if any(not verify_embedded_digest(row, "event_digest") for row in events):
        errors.append("EVENT_DIGEST")

    if acceptance.get("passed") is not True:
        errors.append("ACCEPTANCE")
    if hostile.get("result") != "PASS":
        errors.append("HOSTILE_REVIEW")
    if receipt.get("event_count") != len(events):
        errors.append("RECEIPT_EVENT_COUNT")
    if receipt.get("live_state_mutation_performed") is not False:
        errors.append("RECEIPT_LIVE_MUTATION")
    if handoff.get("deprecation_candidate_count") != len(candidates):
        errors.append("HANDOFF_DEPRECATION_COUNT")
    if handoff.get("remaining_legacy_consumer_count") != 806:
        errors.append("HANDOFF_BLOCKER_COUNT")
    if handoff.get("reference_rehearsal_only") is not True:
        errors.append("HANDOFF_SCOPE")

    manifest_paths = set()
    for item in output_manifest.get("files", []):
        relative = item["path"]
        if relative in manifest_paths:
            errors.append(f"OUTPUT_DUPLICATE:{relative}")
        manifest_paths.add(relative)
        path = root / relative
        if not path.is_file():
            errors.append(f"OUTPUT_MISSING:{relative}")
        elif file_digest(path) != item["sha256"]:
            errors.append(f"OUTPUT_HASH:{relative}")
    actual_paths = {
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file() and path.name != "output_manifest.json"
    }
    if manifest_paths != actual_paths:
        errors.append("OUTPUT_MANIFEST_COVERAGE")
    if output_manifest.get("file_count") != len(manifest_paths):
        errors.append("OUTPUT_MANIFEST_COUNT")

    return errors
