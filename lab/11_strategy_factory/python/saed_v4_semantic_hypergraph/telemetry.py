from __future__ import annotations

from .canonical import content_hash
from .models import HypergraphTelemetry, SemanticTemporalHypergraph


def build_telemetry(graph: SemanticTemporalHypergraph) -> HypergraphTelemetry:
    payload = {
        "operation": "build_hypergraph",
        "graph_id": graph.graph_id,
        "source_package_id": graph.source_package_id,
        "node_count": len(graph.nodes),
        "edge_count": len(graph.edges),
        "masked_edge_count": sum(not edge.active for edge in graph.edges),
        "degraded_node_count": sum(node.masked or node.quality < 1.0 for node in graph.nodes),
        "deterministic": True,
        "authority_violation_count": 0,
    }
    return HypergraphTelemetry(**payload, telemetry_hash=content_hash(payload))
