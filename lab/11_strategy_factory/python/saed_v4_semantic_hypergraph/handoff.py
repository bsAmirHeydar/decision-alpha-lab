from __future__ import annotations

from .canonical import content_hash, stable_id
from .models import GraphIntegrityReceipt, SemanticTemporalHypergraph


def build_v4_06_handoff(
    graph: SemanticTemporalHypergraph,
    integrity_receipt: GraphIntegrityReceipt,
) -> dict:
    payload = {
        "phase": "SAED_V4_05",
        "next_phase": "SAED_V4_06",
        "graph_id": graph.graph_id,
        "graph_hash": graph.graph_hash,
        "source_package_id": graph.source_package_id,
        "source_package_hash": graph.source_package_hash,
        "registry_id": graph.registry_id,
        "registry_hash": graph.registry_hash,
        "policy_id": graph.policy_id,
        "policy_hash": graph.policy_hash,
        "twin_id": graph.twin_id,
        "known_as_of": graph.known_as_of,
        "event_as_of": graph.event_as_of,
        "evidence_role": graph.evidence_role.value,
        "status": graph.status.value,
        "node_ids": sorted(node.node_id for node in graph.nodes),
        "node_hashes": sorted(node.node_hash for node in graph.nodes),
        "edge_ids": sorted(edge.edge_id for edge in graph.edges),
        "edge_hashes": sorted(edge.edge_hash for edge in graph.edges),
        "integrity_receipt_id": integrity_receipt.receipt_id,
        "authority": {
            "read_hypergraph": True,
            "bind_external_treatment_dsl": True,
            "mutate_ucee_truth": False,
            "mutate_graph": False,
            "generate_treatment": False,
            "select_treatment": False,
            "train_model": False,
            "allocate_risk": False,
            "activate_runtime": False,
            "send_order": False,
        },
        "limitations": [
            "Hyperedges are deterministic and allowlisted; no learned relation is canonical.",
            "Treatment descriptors are read-only and no Treatment is generated or selected.",
            "The graph contains no trained encoder and makes no alpha claim.",
        ],
    }
    payload["handoff_id"] = stable_id("v405to06", payload)
    payload["handoff_hash"] = content_hash(payload)
    return payload
