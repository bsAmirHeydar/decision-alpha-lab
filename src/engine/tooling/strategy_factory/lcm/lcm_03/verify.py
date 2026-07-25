from __future__ import annotations

from pathlib import Path

from .canonical import digest_object, sha256_file
from .errors import IntegrityError
from .event_ledger import verify as verify_events
from .io import read_json, read_jsonl
from .locators import Resolver
from .upstream import latest_classification, verify_classification


def verify_output_manifest(root: Path):
    manifest = read_json(root / "output_manifest.json")
    if manifest.get("output_manifest_digest") != digest_object(
        manifest, "output_manifest_digest"
    ):
        raise IntegrityError("LCM-03 output manifest digest mismatch")

    declared = set()
    for artifact in manifest.get("artifacts", []):
        path = root / artifact["path"]
        declared.add(artifact["path"])
        if (
            not path.is_file()
            or path.stat().st_size != artifact["size_bytes"]
            or sha256_file(path) != artifact["sha256"]
        ):
            raise IntegrityError(f"LCM-03 artifact mismatch: {artifact['path']}")

    actual = {
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file() and path.name != "output_manifest.json"
    }
    if actual != declared:
        raise IntegrityError("LCM-03 artifact set mismatch")
    return manifest


def verify_package(root: Path):
    manifest = verify_output_manifest(root)
    marker = read_json(root / "identity_marker.json")
    run_id = marker["identity_run_id"]
    if marker.get("marker_digest") != digest_object(marker, "marker_digest"):
        raise IntegrityError("identity marker digest mismatch")

    identities = list(read_jsonl(root / "identities/canonical_identity_candidates.jsonl"))
    ambiguities = list(read_jsonl(root / "unresolved/identity_ambiguity_queue.jsonl"))
    aliases = list(read_jsonl(root / "aliases/legacy_alias_records.jsonl"))
    locators = list(read_jsonl(root / "locators/artifact_locator_records.jsonl"))
    consumers = list(read_jsonl(root / "consumers/consumer_census.jsonl"))
    collisions = read_json(root / "collisions/alias_collision_report.json")["collisions"]
    summary = read_json(root / "reports/identity_summary.json")

    if summary.get("summary_digest") != digest_object(summary, "summary_digest"):
        raise IntegrityError("identity summary digest mismatch")
    if len(identities) != summary["identity_candidate_count"]:
        raise IntegrityError("identity cardinality mismatch")
    if len(ambiguities) != summary["identity_ambiguity_count"]:
        raise IntegrityError("ambiguity cardinality mismatch")
    if len({item["identity_id"] for item in identities}) != len(identities):
        raise IntegrityError("duplicate identity ID")
    if len(locators) != len(identities):
        raise IntegrityError("locator cardinality mismatch")
    if any(item.get("canonical_path_materialized") for item in locators):
        raise IntegrityError("canonical path materialized in LCM-03")
    if len(identities) + len(ambiguities) != summary["active_candidate_count"]:
        raise IntegrityError("active candidate coverage mismatch")

    alias_index = read_json(root / "aliases/alias_resolution_index.json")["index"]
    collision_keys = {
        "|".join(
            [
                item["alias_type"],
                item["alias_scope"],
                item["normalized_alias_value"],
            ]
        )
        for item in collisions
    }
    resolver = Resolver(locators, alias_index, collision_keys)
    for identity in identities[:50]:
        resolver.resolve_identity(identity["identity_id"], "1.0.0")

    verify_events(read_json(root / "events/identity_event_ledger.json"))
    handoff = read_json(root / "handoff/lcm03_to_lcm04_handoff.json")
    if handoff.get("handoff_digest") != digest_object(handoff, "handoff_digest"):
        raise IntegrityError("LCM-03 handoff digest mismatch")

    receipt = read_json(root / "identity_receipt.json")
    if receipt.get("receipt_digest") != digest_object(receipt, "receipt_digest"):
        raise IntegrityError("LCM-03 receipt digest mismatch")
    if receipt["identity_run_id"] != run_id:
        raise IntegrityError("LCM-03 receipt run binding mismatch")
    if receipt["identity_summary_digest"] != summary["summary_digest"]:
        raise IntegrityError("LCM-03 receipt summary binding mismatch")
    if receipt["handoff_digest"] != handoff["handoff_digest"]:
        raise IntegrityError("LCM-03 receipt handoff binding mismatch")

    denied = [
        "source_move_performed",
        "source_delete_performed",
        "semantic_refactor_performed",
        "merge_performed",
        "cutover_performed",
        "human_semantic_approval_claimed",
        "runtime_authority_created",
        "live_order_authority_created",
        "capital_authority_created",
    ]
    if any(receipt.get(key) for key in denied):
        raise IntegrityError("LCM-03 authority escalation")

    return {
        "passed": True,
        "identity_run_id": run_id,
        "active_candidate_count": summary["active_candidate_count"],
        "identity_candidate_count": len(identities),
        "identity_ambiguity_count": len(ambiguities),
        "alias_record_count": len(aliases),
        "alias_collision_count": len(collisions),
        "locator_record_count": len(locators),
        "consumer_record_count": len(consumers),
        "package_artifact_count": manifest["artifact_count"],
    }


def verify_installation(repo_root: Path, identity_root: Path, patch_index: Path):
    verify_classification(latest_classification(repo_root))
    result = verify_package(identity_root)
    missing = []
    for line in patch_index.read_text(encoding="utf-8").splitlines():
        relative = line.strip().replace("\\", "/")
        if relative and not (repo_root / relative).is_file():
            missing.append(relative)
    return {
        **result,
        "installation_passed": not missing,
        "missing_patch_files": missing,
    }
