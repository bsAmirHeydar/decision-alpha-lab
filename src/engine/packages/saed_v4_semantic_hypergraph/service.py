from __future__ import annotations

from typing import Any

from .builder import SemanticTemporalHypergraphBuilder
from .diff import diff_graphs
from .integrity import build_integrity_receipt, verify_integrity
from .models import GraphBuildPolicy, GraphQuery, SemanticRegistry, SemanticTemporalHypergraph
from .partitioning import deterministic_partition
from .projection import incidence_projection
from .query import execute_query
from .replay import replay_graph
from .telemetry import build_telemetry


class SemanticTemporalHypergraphService:
    def __init__(self) -> None:
        self._builder = SemanticTemporalHypergraphBuilder()

    def build(
        self,
        package: Any,
        registry: SemanticRegistry,
        policy: GraphBuildPolicy,
        graph_version: str = "1.0.0",
    ) -> SemanticTemporalHypergraph:
        return self._builder.build(package, registry, policy, graph_version)

    @staticmethod
    def integrity(graph: SemanticTemporalHypergraph):
        return build_integrity_receipt(graph)

    @staticmethod
    def verify(graph: SemanticTemporalHypergraph, receipt) -> bool:
        return verify_integrity(graph, receipt)

    @staticmethod
    def replay(expected, package, registry, policy):
        return replay_graph(expected=expected, package=package, registry=registry, policy=policy)

    @staticmethod
    def diff(left, right):
        return diff_graphs(left, right)

    @staticmethod
    def project(graph):
        return incidence_projection(graph)

    @staticmethod
    def query(graph, query: GraphQuery):
        return execute_query(graph, query)

    @staticmethod
    def partition(graph, partition_count: int):
        return deterministic_partition(graph, partition_count)

    @staticmethod
    def telemetry(graph):
        return build_telemetry(graph)
