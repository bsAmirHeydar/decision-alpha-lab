from __future__ import annotations

from collections import deque

from .canonical import content_hash
from .errors import QueryError
from .models import GraphQuery, GraphQueryResult, SemanticTemporalHypergraph


def execute_query(graph: SemanticTemporalHypergraph, query: GraphQuery) -> GraphQueryResult:
    if query.maximum_hops < 0 or query.maximum_hops > 8:
        raise QueryError("maximum_hops must be in [0,8]")
    if query.maximum_results < 1 or query.maximum_results > 10000:
        raise QueryError("maximum_results must be in [1,10000]")
    nodes = {node.node_id: node for node in graph.nodes}
    missing_seeds = sorted(set(query.seed_node_ids) - nodes.keys())
    if missing_seeds:
        raise QueryError(f"unknown seed nodes: {missing_seeds}")
    allowed_relations = set(query.relation_kinds)
    allowed_node_kinds = set(query.node_kinds)
    incident: dict[str, list] = {node_id: [] for node_id in nodes}
    for edge in graph.edges:
        if allowed_relations and edge.relation_kind not in allowed_relations:
            continue
        if not query.include_masked and not edge.active:
            continue
        for node_id in edge.member_node_ids:
            incident[node_id].append(edge)
    visited_nodes = set(query.seed_node_ids)
    visited_edges: set[str] = set()
    queue = deque((node_id, 0) for node_id in sorted(query.seed_node_ids))
    truncated = False
    while queue:
        node_id, hop = queue.popleft()
        if hop >= query.maximum_hops:
            continue
        for edge in sorted(incident[node_id], key=lambda item: item.edge_id):
            visited_edges.add(edge.edge_id)
            for member_id in edge.member_node_ids:
                if allowed_node_kinds and nodes[member_id].kind not in allowed_node_kinds:
                    continue
                if member_id not in visited_nodes:
                    visited_nodes.add(member_id)
                    queue.append((member_id, hop + 1))
                    if len(visited_nodes) >= query.maximum_results:
                        truncated = True
                        queue.clear()
                        break
            if truncated:
                break
    selected_nodes = tuple(sorted(visited_nodes)[: query.maximum_results])
    selected_edges = tuple(
        sorted(
            edge_id
            for edge_id in visited_edges
            if any(node_id in selected_nodes for node_id in next(edge.member_node_ids for edge in graph.edges if edge.edge_id == edge_id))
        )
    )
    payload = {
        "query_id": query.query_id,
        "graph_id": graph.graph_id,
        "node_ids": selected_nodes,
        "edge_ids": selected_edges,
        "truncated": truncated,
    }
    return GraphQueryResult(
        query_id=query.query_id,
        graph_id=graph.graph_id,
        node_ids=selected_nodes,
        edge_ids=selected_edges,
        truncated=truncated,
        result_hash=content_hash(payload),
    )
