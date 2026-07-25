from __future__ import annotations
from dataclasses import asdict, dataclass, field
from typing import Any

@dataclass(frozen=True)
class VisualSite:
    visual_object_id: str
    source_path: str
    source_digest: str
    line: int
    function_name: str
    surface_kind: str
    object_type: str
    observed_name_expression: str
    chart_scope_expression: str
    raw_arguments: tuple[str, ...]
    active_status: str
    owner: str
    subsystem: str
    source_event_type: str
    source_event_binding_status: str
    source_event_evidence: str
    blocker_ids: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["raw_arguments"] = list(self.raw_arguments)
        value["blocker_ids"] = list(self.blocker_ids)
        return value

@dataclass(frozen=True)
class NamespaceContract:
    namespace_id: str
    visual_object_id: str
    canonical_object_id_template: str
    canonical_cleanup_prefix_template: str
    observed_name_expression: str
    observed_scope_status: str
    collision_risk: str
    deterministic: bool
    collision_resistant: bool
    randomness_forbidden: bool

    def to_dict(self) -> dict[str, Any]: return asdict(self)

@dataclass(frozen=True)
class AnchorContract:
    anchor_contract_id: str
    visual_object_id: str
    anchor_kind: str
    chart_projection_scope: str
    source_candle_semantics: str
    availability_time_semantics: str
    time_anchor_1: str | None
    price_anchor_1: str | None
    time_anchor_2: str | None
    price_anchor_2: str | None
    extension_behavior: str
    host_chart_dependency: str
    validation_status: str
    blocker_ids: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        value=asdict(self); value["blocker_ids"]=list(self.blocker_ids); return value

@dataclass(frozen=True)
class LifecycleContract:
    lifecycle_contract_id: str
    visual_object_id: str
    initialization_policy: str
    backfill_policy: str
    incremental_update_policy: str
    restart_policy: str
    timeframe_change_policy: str
    symbol_change_policy: str
    deinitialization_policy: str
    cleanup_scope: str
    observed_delete_policy: str
    canonical_states: tuple[str, ...]
    validation_status: str
    blocker_ids: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        value=asdict(self); value["canonical_states"]=list(self.canonical_states); value["blocker_ids"]=list(self.blocker_ids); return value
