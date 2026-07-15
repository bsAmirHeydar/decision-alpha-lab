from __future__ import annotations

from .canonical import merkle_root
from .errors import IntegrityError
from .models import GraphIntegrityReceipt, SemanticTemporalHypergraph


def build_integrity_receipt(graph: SemanticTemporalHypergraph) -> GraphIntegrityReceipt:
    node_hashes = tuple(sorted(node.node_hash for node in graph.nodes))
    edge_hashes = tuple(sorted(edge.edge_hash for edge in graph.edges))
    component_root = merkle_root(
        [
            graph.graph_hash,
            graph.source_package_hash,
            graph.registry_hash,
            graph.policy_hash,
            graph.lineage_root,
            *node_hashes,
            *edge_hashes,
        ]
    )
    return GraphIntegrityReceipt(
        graph_id=graph.graph_id,
        graph_hash=graph.graph_hash,
        source_package_hash=graph.source_package_hash,
        registry_hash=graph.registry_hash,
        policy_hash=graph.policy_hash,
        node_hashes=node_hashes,
        edge_hashes=edge_hashes,
        component_root=component_root,
        status="pass",
    )


def verify_integrity(graph: SemanticTemporalHypergraph, receipt: GraphIntegrityReceipt) -> bool:
    observed = build_integrity_receipt(graph)
    if observed != receipt:
        raise IntegrityError("semantic-temporal hypergraph integrity mismatch")
    return True
