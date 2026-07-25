from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from strategy_factory_contexts_v3 import FeatureDataType
from strategy_factory_rthp_context_v1 import RTHPContextPackage, cluster_dimensions
from strategy_factory_contexts_v3 import ClusterCompiler, RepresentationViewRegistry, RepresentationKind


@dataclass(frozen=True, slots=True)
class EncodedObservation:
    event_id: str
    feature_order: tuple[str, ...]
    features: tuple[float, ...]
    observation_id: str
    observation_hash: str
    opportunity_cluster_id: str
    event_time_ms: int
    known_time_ms: int
    view_hashes: dict[str, str]


class RTHPFeatureEncoder:
    def __init__(self):
        self.package = RTHPContextPackage()
        self.feature_order = self._feature_order()
        self._cluster_compiler = ClusterCompiler()
        self._view_registry = RepresentationViewRegistry()

    def _feature_order(self) -> tuple[str, ...]:
        order: list[str] = []
        for descriptor in self.package.feature_descriptors():
            if descriptor.data_type is FeatureDataType.CATEGORY:
                order.extend(f"{descriptor.feature_id}=={category}" for category in descriptor.category_values)
                order.append(f"{descriptor.feature_id}__MISSING")
            else:
                order.append(descriptor.feature_id)
                if descriptor.missingness_policy.value == "explicit_missing":
                    order.append(f"{descriptor.feature_id}__MISSING")
        return tuple(order)

    def _encode(self, frame) -> tuple[float, ...]:
        by_id = {x.feature_id: x for x in frame.values}
        output: list[float] = []
        for descriptor in frame.descriptors:
            value = by_id[descriptor.feature_id]
            if descriptor.data_type is FeatureDataType.CATEGORY:
                output.extend(1.0 if not value.is_missing and value.value == category else 0.0 for category in descriptor.category_values)
                output.append(1.0 if value.is_missing else 0.0)
            else:
                if value.is_missing:
                    output.append(0.0)
                elif descriptor.data_type is FeatureDataType.BOOL:
                    output.append(1.0 if bool(value.value) else 0.0)
                else:
                    output.append(float(value.value))
                if descriptor.missingness_policy.value == "explicit_missing":
                    output.append(1.0 if value.is_missing else 0.0)
        return tuple(output)

    def compile(self, source: dict[str, Any], *, retain_views: bool = True) -> EncodedObservation:
        observation = self.package.observe(source)[0]
        frame = self.package.build_feature_frame(observation, source)
        rule = next(x for x in self.package.cluster_rules() if x.rule_id == "rthp.opportunity.v1")
        cluster = self._cluster_compiler.compile(rule, observation, cluster_dimensions(source, label_horizon_group="activation"))
        view_hashes: dict[str, str] = {}
        if retain_views:
            auxiliary = dict(source["auxiliary"])
            value_map = {x.feature_id: x.value for x in frame.values}
            sequence_windows: dict[str, list[Any]] = {}
            for descriptor in self.package.view_descriptors():
                if descriptor.kind is RepresentationKind.SEQUENCE:
                    for feature_id in descriptor.feature_ids:
                        sequence_windows[feature_id] = [value_map[feature_id]] * descriptor.shape[1]
            auxiliary["sequence_windows"] = sequence_windows
            for descriptor in self.package.view_descriptors():
                view_hashes[descriptor.view_id] = self._view_registry.compile(descriptor, frame, auxiliary).view_hash
        return EncodedObservation(
            source["event_id"], self.feature_order, self._encode(frame), observation.observation_id,
            observation.observation_hash, cluster.cluster_id, source["event_time_ms"], source["known_time_ms"], view_hashes,
        )
