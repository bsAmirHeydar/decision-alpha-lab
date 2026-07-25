from __future__ import annotations

from .canonical import content_id, digest_object


def build_provenance(baseline_id: str, digests: dict[str, str]) -> dict:
    nodes = []
    for name, digest in sorted(digests.items()):
        nodes.append({
            "node_id": content_id("LCM00NODE", {"name": name, "digest": digest}),
            "artifact_role": name,
            "artifact_digest": digest,
        })
    edges = []
    by_role = {node["artifact_role"]: node["node_id"] for node in nodes}
    ordered = [
        "program_constitution",
        "scope_policy",
        "repository_state",
        "ownership_registry",
        "baseline_manifest",
        "restore_rehearsal",
        "baseline_receipt",
        "lcm01_handoff",
    ]
    for left, right in zip(ordered, ordered[1:]):
        if left in by_role and right in by_role:
            edges.append({"from": by_role[left], "to": by_role[right], "relation": "DERIVES_AND_BINDS"})
    value = {
        "schema_version": "1.0.0",
        "baseline_id": baseline_id,
        "nodes": nodes,
        "edges": edges,
        "source_behavior_mutated": False,
        "source_file_moved": False,
        "source_file_deleted": False,
        "execution_authority_created": False,
        "capital_authority_created": False,
        "provenance_digest": "",
    }
    value["provenance_digest"] = digest_object(value, "provenance_digest")
    return value
