from __future__ import annotations

from .canonical import content_hash, stable_id
from .enums import ProjectionKind
from .models import GraphProjection, SemanticTemporalHypergraph


def incidence_projection(graph: SemanticTemporalHypergraph) -> GraphProjection:
    nodes = tuple(sorted(node.node_id for node in graph.nodes))
    edges = tuple(sorted(edge.edge_id for edge in graph.edges))
    node_position = {node_id: index for index, node_id in enumerate(nodes)}
    rows = []
    edge_by_id = {edge.edge_id: edge for edge in graph.edges}
    for edge_id in edges:
        row = [0] * len(nodes)
        edge = edge_by_id[edge_id]
        for node_id in edge.member_node_ids:
            row[node_position[node_id]] = 1 if edge.active else -1
        rows.append(tuple(row))
    payload = {
        "graph_hash": graph.graph_hash,
        "kind": ProjectionKind.INCIDENCE.value,
        "node_ids": nodes,
        "edge_ids": edges,
        "rows": rows,
    }
    projection_hash = content_hash(payload)
    return GraphProjection(
        projection_id=stable_id("graphprojection", payload),
        graph_id=graph.graph_id,
        graph_hash=graph.graph_hash,
        kind=ProjectionKind.INCIDENCE,
        node_ids=nodes,
        edge_ids=edges,
        rows=tuple(rows),
        projection_hash=projection_hash,
        limitations=(
            "Incidence projection is a deterministic non-learned baseline.",
            "A -1 incidence denotes membership in a masked edge; it is not a negative causal relation.",
        ),
    )
