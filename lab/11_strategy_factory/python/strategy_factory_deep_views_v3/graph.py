"""Known-time graph construction and deterministic message-passing baseline."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

from .canonical import canonical_sha256, stable_id
from .contracts import GraphArtifact, GraphSpec
from .errors import DeepViewError
from .math_utils import mean, ridge_fit, ridge_predict, sigmoid, std


def build_graph_artifact(
    spec: GraphSpec,
    context_observation_id: str,
    known_time_ms: int,
    node_ids: Sequence[str],
    node_times_ms: Sequence[int],
    node_features: Sequence[Sequence[float]],
    edges: Sequence[tuple[int, int]],
) -> GraphArtifact:
    if not context_observation_id:
        raise DeepViewError("context_id_required", "context_observation_id is required")
    ids = tuple(str(value) for value in node_ids)
    times = tuple(int(value) for value in node_times_ms)
    features = tuple(tuple(float(value) for value in row) for row in node_features)
    if not ids or len(ids) != len(times) or len(ids) != len(features):
        raise DeepViewError("graph_node_alignment", "graph node arrays differ")
    if len(set(ids)) != len(ids):
        raise DeepViewError("duplicate_graph_node", "node IDs must be unique")
    if any(time > int(known_time_ms) for time in times):
        raise DeepViewError("future_graph_node", "graph contains a future node")
    width = len(spec.node_feature_order)
    if any(len(row) != width for row in features):
        raise DeepViewError("graph_feature_width", "node feature width differs")
    if any(not math.isfinite(value) for row in features for value in row):
        raise DeepViewError("non_finite_graph_feature", "graph node features must be finite")

    normalized_edges: set[tuple[int, int]] = set()
    for raw_source, raw_target in edges:
        source, target = int(raw_source), int(raw_target)
        if source < 0 or target < 0 or source >= len(ids) or target >= len(ids):
            raise DeepViewError("graph_edge_out_of_range", "graph edge endpoint is out of range")
        if source == target:
            raise DeepViewError("graph_self_loop_forbidden", "explicit self-loops are forbidden in the canonical topology")
        normalized_edges.add((source, target) if spec.directed else tuple(sorted((source, target))))
    canonical_edges = tuple(sorted(normalized_edges))
    topology_material = {
        "node_ids": ids,
        "edges": canonical_edges,
        "directed": spec.directed,
        "topology_version": spec.topology_version,
    }
    topology_hash = canonical_sha256(topology_material)
    identity = {
        "spec_hash": spec.spec_hash,
        "context_observation_id": context_observation_id,
        "known_time_ms": int(known_time_ms),
        "node_ids": ids,
        "node_times_ms": times,
        "node_features": features,
        "topology_hash": topology_hash,
    }
    return GraphArtifact(
        artifact_id=stable_id("ucegraph", identity),
        spec_hash=spec.spec_hash,
        context_observation_id=context_observation_id,
        known_time_ms=int(known_time_ms),
        node_ids=ids,
        node_times_ms=times,
        node_features=features,
        edges=canonical_edges,
        topology_hash=topology_hash,
        evidence_hash=canonical_sha256(identity),
    )


class MessagePassingEncoder:
    """Fixed mean aggregation with residual updates and graph-level pooling."""

    def __init__(self, rounds: int = 2) -> None:
        self.rounds = int(rounds)
        if self.rounds < 0:
            raise DeepViewError("negative_message_rounds", "message-passing rounds cannot be negative")

    def encode(
        self,
        node_features: Sequence[Sequence[float]],
        edges: Sequence[tuple[int, int]],
        directed: bool = False,
    ) -> tuple[float, ...]:
        state = [list(map(float, row)) for row in node_features]
        if not state:
            return ()
        feature_count = len(state[0])
        if feature_count < 1 or any(len(row) != feature_count for row in state):
            raise DeepViewError("graph_feature_width", "node feature widths differ")
        adjacency = [set() for _ in state]
        incoming = [set() for _ in state]
        for source, target in edges:
            if source < 0 or target < 0 or source >= len(state) or target >= len(state):
                raise DeepViewError("graph_edge_out_of_range", "graph edge endpoint is out of range")
            adjacency[source].add(target)
            incoming[target].add(source)
            if not directed:
                adjacency[target].add(source)
                incoming[source].add(target)

        for _ in range(self.rounds):
            next_state: list[list[float]] = []
            for index, row in enumerate(state):
                neighbor_ids = sorted(incoming[index] if directed else adjacency[index])
                neighbors = [state[neighbor] for neighbor in neighbor_ids]
                aggregate = [
                    mean(neighbor[column] for neighbor in neighbors) if neighbors else row[column]
                    for column in range(feature_count)
                ]
                next_state.append([(row[column] + aggregate[column]) / 2.0 for column in range(feature_count)])
            state = next_state

        output: list[float] = []
        for column in range(feature_count):
            values = [row[column] for row in state]
            output.extend((mean(values), std(values), max(values), min(values)))
        out_degrees = [len(neighbors) for neighbors in adjacency]
        in_degrees = [len(neighbors) for neighbors in incoming]
        output.extend(
            (
                mean(out_degrees),
                max(out_degrees, default=0),
                mean(in_degrees),
                max(in_degrees, default=0),
                len(edges) / max(1, len(state)),
                sum(degree == 0 for degree in out_degrees) / len(state),
            )
        )
        return tuple(float(value) for value in output)


@dataclass(frozen=True, slots=True)
class GraphMessagePassingModel:
    node_count: int
    feature_count: int
    directed: bool
    rounds: int
    edges: tuple[tuple[int, int], ...]
    coefficients: tuple[tuple[float, ...], ...]
    output_count: int
    probability_output: bool
    state_hash: str

    @classmethod
    def fit(
        cls,
        flattened_values: Sequence[Sequence[float]],
        targets: Sequence[Sequence[float]],
        node_count: int,
        feature_count: int,
        edges: Sequence[tuple[int, int]],
        directed: bool = False,
        rounds: int = 2,
        alpha: float = 1e-3,
        probability_output: bool = False,
        weights: Sequence[float] | None = None,
    ) -> "GraphMessagePassingModel":
        if len(flattened_values) != len(targets) or not flattened_values:
            raise DeepViewError("invalid_graph_training_set", "graph rows and targets must be non-empty and aligned")
        canonical_edges = tuple(sorted(set((int(a), int(b)) if directed else tuple(sorted((int(a), int(b)))) for a, b in edges)))
        encoder = MessagePassingEncoder(rounds)
        graph_features: list[tuple[float, ...]] = []
        for values in flattened_values:
            if len(values) != node_count * feature_count:
                raise DeepViewError("graph_flat_width", "flattened graph width differs")
            nodes = [
                values[index * feature_count : (index + 1) * feature_count]
                for index in range(node_count)
            ]
            graph_features.append(encoder.encode(nodes, canonical_edges, directed))
        output_count = len(targets[0])
        if output_count < 1 or any(len(target) != output_count for target in targets):
            raise DeepViewError("graph_target_width_mismatch", "graph target widths differ")
        coefficients = tuple(
            ridge_fit(graph_features, [target[index] for target in targets], alpha, weights)
            for index in range(output_count)
        )
        material = {
            "node_count": node_count,
            "feature_count": feature_count,
            "directed": directed,
            "rounds": rounds,
            "edges": canonical_edges,
            "coefficients": coefficients,
            "probability_output": probability_output,
        }
        return cls(
            int(node_count),
            int(feature_count),
            bool(directed),
            int(rounds),
            canonical_edges,
            coefficients,
            output_count,
            bool(probability_output),
            canonical_sha256(material),
        )

    def predict(self, values: Sequence[float]) -> tuple[float, ...]:
        if len(values) != self.node_count * self.feature_count:
            raise DeepViewError("graph_flat_width", "flattened graph width differs")
        nodes = [
            values[index * self.feature_count : (index + 1) * self.feature_count]
            for index in range(self.node_count)
        ]
        features = MessagePassingEncoder(self.rounds).encode(nodes, self.edges, self.directed)
        raw = tuple(ridge_predict(coefficients, features) for coefficients in self.coefficients)
        return tuple(sigmoid(value) for value in raw) if self.probability_output else raw


def remove_edges(
    edges: Sequence[tuple[int, int]],
    removed: Sequence[tuple[int, int]],
    directed: bool = False,
) -> tuple[tuple[int, int], ...]:
    normalize = lambda edge: tuple(map(int, edge)) if directed else tuple(sorted(map(int, edge)))
    removed_set = {normalize(edge) for edge in removed}
    return tuple(sorted({normalize(edge) for edge in edges if normalize(edge) not in removed_set}))
