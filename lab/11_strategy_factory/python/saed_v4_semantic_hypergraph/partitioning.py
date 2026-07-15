from __future__ import annotations

from .canonical import content_hash
from .models import PartitionManifest, SemanticTemporalHypergraph


def deterministic_partition(graph: SemanticTemporalHypergraph, partition_count: int) -> PartitionManifest:
    if partition_count < 1:
        raise ValueError("partition_count must be positive")
    node_partitions = tuple(
        sorted(
            (node.node_id, int(node.node_hash[:16], 16) % partition_count)
            for node in graph.nodes
        )
    )
    edge_partitions = tuple(
        sorted(
            (edge.edge_id, int(edge.edge_hash[:16], 16) % partition_count)
            for edge in graph.edges
        )
    )
    payload = {
        "graph_id": graph.graph_id,
        "graph_hash": graph.graph_hash,
        "partition_count": partition_count,
        "node_partitions": node_partitions,
        "edge_partitions": edge_partitions,
    }
    return PartitionManifest(
        graph_id=graph.graph_id,
        graph_hash=graph.graph_hash,
        partition_count=partition_count,
        node_partitions=node_partitions,
        edge_partitions=edge_partitions,
        manifest_hash=content_hash(payload),
    )
