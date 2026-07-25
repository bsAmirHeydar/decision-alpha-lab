from __future__ import annotations
from dataclasses import dataclass,asdict,field
from typing import Any

@dataclass(frozen=True)
class VisualEventRecord:
    event_id:str;visual_object_id:str;event_type:str;instance_id:str;chart_id:str;symbol:str;timeframe:str;availability_time:int;lifecycle_action:str;anchors:dict[str,Any];payload:dict[str,Any];source_digest:str
    def to_dict(self):return asdict(self)
@dataclass(frozen=True)
class StyleProfile:
    style_profile_id:str;visual_object_id:str;object_type:str;semantic_fields:tuple[str,...];style_fields:dict[str,Any];style_affects_semantics:bool=False
    def to_dict(self):
        x=asdict(self);x["semantic_fields"]=list(self.semantic_fields);return x
@dataclass(frozen=True)
class VisualizerContract:
    visualizer_id:str;visual_object_id:str;visualizer_kind:str;source_event_type:str;namespace_template:str;cleanup_prefix_template:str;anchor_contract_id:str;lifecycle_contract_id:str;style_profile_id:str;projection_purity:str;domain_mutation_allowed:bool;runtime_authority:bool;order_authority:bool;capital_authority:bool;eligibility_status:str;blocker_ids:tuple[str,...]=field(default_factory=tuple)
    def to_dict(self):x=asdict(self);x["blocker_ids"]=list(self.blocker_ids);return x
@dataclass(frozen=True)
class ProjectionRecord:
    projection_id:str;visualizer_id:str;event_id:str;canonical_object_id:str;surface_kind:str;object_type:str;chart_id:str;symbol:str;timeframe:str;anchors:dict[str,Any];semantic_payload:dict[str,Any];style_profile_id:str;lifecycle_action:str
    def to_dict(self):return asdict(self)
