from __future__ import annotations

from .models import GraphDiff, SemanticTemporalHypergraph


def diff_graphs(left: SemanticTemporalHypergraph, right: SemanticTemporalHypergraph) -> GraphDiff:
    left_nodes = {node.node_id: node.node_hash for node in left.nodes}
    right_nodes = {node.node_id: node.node_hash for node in right.nodes}
    left_edges = {edge.edge_id: edge.edge_hash for edge in left.edges}
    right_edges = {edge.edge_id: edge.edge_hash for edge in right.edges}
    return GraphDiff(
        left_graph_hash=left.graph_hash,
        right_graph_hash=right.graph_hash,
        added_node_ids=tuple(sorted(right_nodes.keys() - left_nodes.keys())),
        removed_node_ids=tuple(sorted(left_nodes.keys() - right_nodes.keys())),
        changed_node_ids=tuple(
            sorted(node_id for node_id in left_nodes.keys() & right_nodes.keys() if left_nodes[node_id] != right_nodes[node_id])
        ),
        added_edge_ids=tuple(sorted(right_edges.keys() - left_edges.keys())),
        removed_edge_ids=tuple(sorted(left_edges.keys() - right_edges.keys())),
        changed_edge_ids=tuple(
            sorted(edge_id for edge_id in left_edges.keys() & right_edges.keys() if left_edges[edge_id] != right_edges[edge_id])
        ),
        status_changed=left.status != right.status,
        support_changed=left.support != right.support,
    )
