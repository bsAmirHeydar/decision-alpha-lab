from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Mapping
from .canonical import content_hash, stable_id
from .enums import EVIDENCE_CLASSES, EVIDENCE_ROLES, SCENARIO_KINDS
from .errors import ContractError


def _positive(name: str, value: float) -> float:
    if value <= 0:
        raise ContractError(f"{name} must be positive")
    return value


def _non_negative(name: str, value: float) -> float:
    if value < 0:
        raise ContractError(f"{name} must be non-negative")
    return value

@dataclass(frozen=True)
class LatencyProfile:
    submit_ms: int
    acknowledgement_ms: int
    fill_ms: int
    cancel_ms: int
    jitter_ms: int
    latency_points_per_second: float

    @classmethod
    def from_mapping(cls, x: Mapping[str, Any]) -> "LatencyProfile":
        obj = cls(int(x["submit_ms"]), int(x["acknowledgement_ms"]), int(x["fill_ms"]), int(x["cancel_ms"]), int(x["jitter_ms"]), float(x["latency_points_per_second"]))
        for name in ("submit_ms", "acknowledgement_ms", "fill_ms", "cancel_ms", "jitter_ms"):
            _non_negative(name, float(getattr(obj, name)))
        _non_negative("latency_points_per_second", obj.latency_points_per_second)
        return obj

@dataclass(frozen=True)
class QueueProfile:
    base_queue_units: float
    uncertainty_units: float
    participation_rate: float
    maximum_partial_fills: int

    @classmethod
    def from_mapping(cls, x: Mapping[str, Any]) -> "QueueProfile":
        obj = cls(float(x["base_queue_units"]), float(x["uncertainty_units"]), float(x["participation_rate"]), int(x["maximum_partial_fills"]))
        _non_negative("base_queue_units", obj.base_queue_units)
        _non_negative("uncertainty_units", obj.uncertainty_units)
        if not 0 < obj.participation_rate <= 1:
            raise ContractError("participation_rate must be in (0,1]")
        if obj.maximum_partial_fills < 1:
            raise ContractError("maximum_partial_fills must be positive")
        return obj

@dataclass(frozen=True)
class FillHazardProfile:
    base_probability: float
    spread_sensitivity: float
    queue_sensitivity: float
    latency_sensitivity: float
    minimum_probability: float

    @classmethod
    def from_mapping(cls, x: Mapping[str, Any]) -> "FillHazardProfile":
        obj = cls(*(float(x[k]) for k in ("base_probability", "spread_sensitivity", "queue_sensitivity", "latency_sensitivity", "minimum_probability")))
        if not 0 <= obj.minimum_probability <= obj.base_probability <= 1:
            raise ContractError("fill probabilities are invalid")
        for name in ("spread_sensitivity", "queue_sensitivity", "latency_sensitivity"):
            _non_negative(name, getattr(obj, name))
        return obj

@dataclass(frozen=True)
class ImpactProfile:
    linear_points_per_unit: float
    square_root_points_per_sqrt_unit: float
    temporary_decay_fraction: float

    @classmethod
    def from_mapping(cls, x: Mapping[str, Any]) -> "ImpactProfile":
        obj = cls(float(x["linear_points_per_unit"]), float(x["square_root_points_per_sqrt_unit"]), float(x["temporary_decay_fraction"]))
        _non_negative("linear_points_per_unit", obj.linear_points_per_unit)
        _non_negative("square_root_points_per_sqrt_unit", obj.square_root_points_per_sqrt_unit)
        if not 0 <= obj.temporary_decay_fraction <= 1:
            raise ContractError("temporary_decay_fraction must be in [0,1]")
        return obj

@dataclass(frozen=True)
class AdverseSelectionProfile:
    base_points: float
    latency_coefficient: float
    non_fill_coefficient: float

    @classmethod
    def from_mapping(cls, x: Mapping[str, Any]) -> "AdverseSelectionProfile":
        obj = cls(float(x["base_points"]), float(x["latency_coefficient"]), float(x["non_fill_coefficient"]))
        for name in ("base_points", "latency_coefficient", "non_fill_coefficient"):
            _non_negative(name, getattr(obj, name))
        return obj

@dataclass(frozen=True)
class BrokerProfile:
    broker_id: str
    exact_version: str
    minimum_volume: float
    maximum_volume: float
    volume_step: float
    maximum_deviation_points: float
    maximum_open_orders: int
    stop_level_points: float
    freeze_level_points: float
    partial_fills_allowed: bool
    allowed_order_types: tuple[str, ...]

    @classmethod
    def from_mapping(cls, x: Mapping[str, Any]) -> "BrokerProfile":
        obj = cls(str(x["broker_id"]), str(x["exact_version"]), float(x["minimum_volume"]), float(x["maximum_volume"]), float(x["volume_step"]), float(x["maximum_deviation_points"]), int(x["maximum_open_orders"]), float(x["stop_level_points"]), float(x["freeze_level_points"]), bool(x["partial_fills_allowed"]), tuple(sorted(str(v) for v in x["allowed_order_types"])))
        if not obj.broker_id or not obj.exact_version:
            raise ContractError("broker identity is required")
        _positive("minimum_volume", obj.minimum_volume)
        if obj.maximum_volume < obj.minimum_volume:
            raise ContractError("maximum_volume below minimum_volume")
        _positive("volume_step", obj.volume_step)
        for name in ("maximum_deviation_points", "stop_level_points", "freeze_level_points"):
            _non_negative(name, getattr(obj, name))
        if obj.maximum_open_orders < 1 or not obj.allowed_order_types:
            raise ContractError("broker capability set is empty")
        return obj

@dataclass(frozen=True)
class Scenario:
    scenario_id: str
    kind: str
    latency_multiplier: float
    spread_multiplier: float
    queue_multiplier: float
    impact_multiplier: float
    rejection_threshold: float
    partial_fill_cap: float

    @classmethod
    def from_mapping(cls, x: Mapping[str, Any]) -> "Scenario":
        obj = cls(str(x["scenario_id"]), str(x["kind"]), float(x["latency_multiplier"]), float(x["spread_multiplier"]), float(x["queue_multiplier"]), float(x["impact_multiplier"]), float(x["rejection_threshold"]), float(x["partial_fill_cap"]))
        if not obj.scenario_id or obj.kind not in SCENARIO_KINDS:
            raise ContractError("invalid scenario identity or kind")
        for name in ("latency_multiplier", "spread_multiplier", "queue_multiplier", "impact_multiplier"):
            _positive(name, getattr(obj, name))
        if not 0 <= obj.rejection_threshold <= 1 or not 0 <= obj.partial_fill_cap <= 1:
            raise ContractError("scenario probability/cap outside [0,1]")
        return obj

    def semantic_payload(self) -> dict[str, Any]:
        return self.__dict__.copy()

    @property
    def scenario_hash(self) -> str:
        return content_hash(self.semantic_payload())

@dataclass(frozen=True)
class ExecutionTwinProfile:
    profile_name: str
    exact_version: str
    evidence_class: str
    synthetic_watermark: bool
    point_size: float
    notional_units: float
    order_volume: float
    latency: LatencyProfile
    queue: QueueProfile
    fill_hazard: FillHazardProfile
    impact: ImpactProfile
    adverse_selection: AdverseSelectionProfile
    broker: BrokerProfile
    scenarios: tuple[Scenario, ...]
    maximum_source_rows: int
    maximum_scenarios: int
    maximum_lifecycle_events_per_row: int
    allowed_evidence_roles: tuple[str, ...]

    @classmethod
    def from_mapping(cls, x: Mapping[str, Any]) -> "ExecutionTwinProfile":
        obj = cls(
            str(x["profile_name"]), str(x["exact_version"]), str(x["evidence_class"]), bool(x["synthetic_watermark"]),
            float(x["point_size"]), float(x["notional_units"]), float(x["order_volume"]),
            LatencyProfile.from_mapping(x["latency"]), QueueProfile.from_mapping(x["queue"]), FillHazardProfile.from_mapping(x["fill_hazard"]),
            ImpactProfile.from_mapping(x["impact"]), AdverseSelectionProfile.from_mapping(x["adverse_selection"]), BrokerProfile.from_mapping(x["broker"]),
            tuple(Scenario.from_mapping(v) for v in x["scenarios"]), int(x["maximum_source_rows"]), int(x["maximum_scenarios"]), int(x["maximum_lifecycle_events_per_row"]),
            tuple(sorted(str(v) for v in x["allowed_evidence_roles"])),
        )
        if not obj.profile_name or not obj.exact_version or obj.evidence_class not in EVIDENCE_CLASSES:
            raise ContractError("invalid profile identity or evidence class")
        _positive("point_size", obj.point_size); _positive("notional_units", obj.notional_units); _positive("order_volume", obj.order_volume)
        if obj.evidence_class == "reference_synthetic" and not obj.synthetic_watermark:
            raise ContractError("reference_synthetic profile requires synthetic_watermark")
        if not obj.scenarios or len({s.scenario_id for s in obj.scenarios}) != len(obj.scenarios):
            raise ContractError("scenarios must be non-empty and uniquely identified")
        if len(obj.scenarios) > obj.maximum_scenarios or min(obj.maximum_source_rows, obj.maximum_scenarios, obj.maximum_lifecycle_events_per_row) < 1:
            raise ContractError("profile budgets are invalid")
        if not set(obj.allowed_evidence_roles).issubset(EVIDENCE_ROLES):
            raise ContractError("unknown evidence role")
        return obj

    def semantic_payload(self) -> dict[str, Any]:
        return {
            "profile_name": self.profile_name, "exact_version": self.exact_version, "evidence_class": self.evidence_class,
            "synthetic_watermark": self.synthetic_watermark, "point_size": self.point_size, "notional_units": self.notional_units,
            "order_volume": self.order_volume, "latency": self.latency.__dict__, "queue": self.queue.__dict__, "fill_hazard": self.fill_hazard.__dict__,
            "impact": self.impact.__dict__, "adverse_selection": self.adverse_selection.__dict__,
            "broker": {**self.broker.__dict__, "allowed_order_types": list(self.broker.allowed_order_types)},
            "scenarios": [s.semantic_payload() for s in sorted(self.scenarios, key=lambda s: s.scenario_id)],
            "maximum_source_rows": self.maximum_source_rows, "maximum_scenarios": self.maximum_scenarios,
            "maximum_lifecycle_events_per_row": self.maximum_lifecycle_events_per_row,
            "allowed_evidence_roles": list(self.allowed_evidence_roles),
        }

    @property
    def profile_hash(self) -> str:
        return content_hash(self.semantic_payload())

    @property
    def profile_id(self) -> str:
        return stable_id("exectwinprofile", self.semantic_payload())
