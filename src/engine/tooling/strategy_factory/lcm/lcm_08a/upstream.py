from __future__ import annotations
from pathlib import Path
from .constants import *
from .errors import UpstreamContractError
from .io import load_json, load_jsonl
from .canonical import file_digest


def _need(path: Path) -> Path:
    if not path.is_file():
        raise UpstreamContractError(f"required upstream artifact missing: {path}")
    return path


def load(repo_root: Path) -> dict:
    root = repo_root.resolve()
    survey = root / "registry/history/lcm/surveys" / SURVEY_ID
    classification = root / "registry/history/lcm/classifications" / CLASSIFICATION_ID
    identity = root / "registry/history/lcm/identities" / IDENTITY_ID
    characterization = root / "registry/history/lcm/characterizations" / CHARACTERIZATION_ID
    topology = root / "registry/history/lcm/target_paths" / TOPOLOGY_ID
    framework = root / "registry/history/lcm/frameworks" / FRAMEWORK_ID
    shared = root / "registry/history/lcm/shared_engines" / SHARED_ENGINE_ID
    roadmap = root / "registry/history/lcm/roadmaps" / ROADMAP_ID
    handoff_path = _need(shared / "handoff/lcm07_to_lcm08_handoff.json")
    handoff = load_json(handoff_path)
    if handoff.get("handoff_type") != "LCM07_TO_LCM08":
        raise UpstreamContractError("LCM-07 handoff type mismatch")
    if not handoff.get("context_migration_reference_authorized"):
        raise UpstreamContractError("LCM-07 does not authorize reference context migration")
    if handoff.get("source_move_allowed") or handoff.get("source_delete_allowed"):
        raise UpstreamContractError("LCM-07 handoff illegally expands source authority")
    paths = {
        "identity_candidates": _need(identity / "identities/canonical_identity_candidates.jsonl"),
        "identity_summary": _need(identity / "reports/identity_summary.json"),
        "identity_ambiguities": _need(identity / "unresolved/identity_ambiguity_queue.jsonl"),
        "alias_collisions": _need(identity / "collisions/alias_collision_report.json"),
        "classification_records": _need(classification / "artifacts/artifact_classification_records.jsonl"),
        "owner_registry": _need(classification / "owners/owner_role_registry.json"),
        "characterization_packets": _need(characterization / "packets/characterization_packet_index.jsonl"),
        "static_profiles": _need(characterization / "profiles/source_static_profiles.jsonl"),
        "characterization_summary": _need(characterization / "reports/characterization_summary.json"),
        "dependency_edges": _need(survey / "dependencies/all_dependency_edges.csv"),
        "capability_findings": _need(survey / "capabilities/capability_findings.csv"),
        "identity_target_map": _need(topology / "mappings/identity_target_map.jsonl"),
        "artifact_target_map": _need(topology / "mappings/artifact_target_map.jsonl"),
        "framework_handoff": _need(framework / "handoff/lcm06_to_lcm07_handoff.json"),
        "shared_candidates": _need(shared / "candidates/selected_candidate_clusters.jsonl"),
        "shared_decisions": _need(shared / "decisions/extraction_decisions.jsonl"),
        "roadmap_manifest": _need(roadmap / "roadmap_registry.json"),
    }
    return {
        "root": root,
        "handoff": handoff,
        "handoff_path": handoff_path,
        "paths": paths,
        "input_digests": {name: file_digest(path) for name, path in sorted(paths.items())},
        "roots": {"survey": survey, "classification": classification, "identity": identity, "characterization": characterization, "topology": topology, "framework": framework, "shared": shared, "roadmap": roadmap},
    }
