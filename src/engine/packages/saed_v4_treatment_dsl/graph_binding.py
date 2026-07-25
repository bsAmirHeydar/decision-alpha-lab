from __future__ import annotations

from typing import Any, Mapping

from .canonical import content_hash, stable_id
from .enums import BindingStatus, EvidenceRole
from .errors import BindingError, IntegrityError, TemporalBoundaryError
from .models import CanonicalTreatmentProgram, DescriptorBinding


def validate_handoff(graph: Mapping[str, Any], handoff: Mapping[str, Any]) -> None:
    required = {
        "phase": "SAED_V4_05",
        "next_phase": "SAED_V4_06",
        "graph_id": graph["graph_id"],
        "graph_hash": graph["graph_hash"],
        "evidence_role": graph["evidence_role"],
        "known_as_of": graph["known_as_of"],
    }
    for key, expected in required.items():
        if handoff.get(key) != expected:
            raise IntegrityError(f"V4-05 handoff mismatch at {key}")
    authority = handoff.get("authority", {})
    if not authority.get("read_hypergraph") or not authority.get("bind_external_treatment_dsl"):
        raise IntegrityError("handoff does not grant bounded V4-06 read/bind authority")
    forbidden = ("mutate_ucee_truth", "mutate_graph", "generate_treatment", "select_treatment", "train_model", "allocate_risk", "activate_runtime", "send_order")
    if any(authority.get(name) for name in forbidden):
        raise IntegrityError("handoff contains forbidden authority")


def bind_descriptor(
    graph: Mapping[str, Any],
    program: CanonicalTreatmentProgram,
) -> DescriptorBinding:
    if program.descriptor_id is None:
        raise BindingError("program has no descriptor_id")
    if graph["evidence_role"] != program.evidence_role.value:
        raise TemporalBoundaryError("cross-role descriptor binding is forbidden")
    if graph["known_as_of"] != program.known_as_of:
        raise TemporalBoundaryError("descriptor binding requires exact known_as_of")
    descriptor_nodes = [
        node for node in graph["nodes"]
        if node["kind"] == "treatment_descriptor"
        and node["attributes"].get("descriptor_id") == program.descriptor_id
    ]
    if len(descriptor_nodes) != 1:
        raise BindingError("exactly one immutable descriptor node is required")
    node = descriptor_nodes[0]
    if node["masked"] or node["missing"] or not node["attributes"].get("read_only"):
        raise BindingError("descriptor node must be visible and read-only")
    graph_labels = {}
    for item in graph["nodes"]:
        if item["kind"] != "feature":
            continue
        attrs = item["attributes"]
        if attrs.get("view_name") == "treatment_descriptor_view" and not item["masked"] and not item["missing"]:
            graph_labels[attrs["feature_id"]] = attrs.get("normalized_value")
    program_labels = dict(program.semantic_labels)
    matched = []
    for key in ("payoff_profile", "entry_mechanism", "path_dependent"):
        if key in program_labels:
            if graph_labels.get(key) != program_labels[key]:
                raise BindingError(f"descriptor semantic label mismatch: {key}")
            matched.append(key)
    if graph_labels.get("descriptor_id") != program.descriptor_id:
        raise BindingError("descriptor_id feature does not match program")
    payload = {
        "descriptor_id": program.descriptor_id,
        "graph_node_id": node["node_id"],
        "graph_node_hash": node["node_hash"],
        "program_id": program.program_id,
        "program_hash": program.program_hash,
        "status": BindingStatus.BOUND.value,
        "evidence_role": program.evidence_role.value,
        "known_as_of": program.known_as_of,
        "matched_labels": sorted(matched),
        "reason_codes": [],
    }
    binding_id = stable_id("dslbinding", payload)
    draft = DescriptorBinding(
        binding_id=binding_id,
        descriptor_id=program.descriptor_id,
        graph_node_id=node["node_id"],
        graph_node_hash=node["node_hash"],
        program_id=program.program_id,
        program_hash=program.program_hash,
        status=BindingStatus.BOUND,
        evidence_role=program.evidence_role,
        known_as_of=program.known_as_of,
        matched_labels=tuple(sorted(matched)),
        reason_codes=(),
        binding_hash="",
    )
    return DescriptorBinding(**{**draft.__dict__, "binding_hash": content_hash(draft.semantic_payload())})
