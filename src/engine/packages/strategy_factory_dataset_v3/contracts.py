from __future__ import annotations
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Mapping, Sequence
from .canonical import canonical_value, safe_id, sha256, stable_id
from .enums import *
from .errors import ContractError, CausalityError

@dataclass(frozen=True, slots=True)
class SourceRef:
    source_id:str; revision:str; content_hash:str; available_time_ms:int
    def __post_init__(self): safe_id(self.source_id,'source_id'); safe_id(self.revision,'revision'); safe_id(self.content_hash,'content_hash')
    def to_dict(self): return {"source_id":self.source_id,"revision":self.revision,"content_hash":self.content_hash,"available_time_ms":self.available_time_ms}

@dataclass(frozen=True, slots=True)
class OpportunityAnchor:
    context_package_key:str; context_occurrence_id:str; dependence_cluster_id:str; symbol:str; timeframe:str; side:TradeSide;
    event_time_ms:int; decision_time_ms:int; known_time_ms:int; feature_frame_hash:str; representation_hashes:Mapping[str,str];
    source_inventory:tuple[SourceRef,...]; eligible:bool=True; ineligibility_reason:str=""; tags:Mapping[str,str]=field(default_factory=dict)
    def __post_init__(self):
        for n,v in (("context_package_key",self.context_package_key),("context_occurrence_id",self.context_occurrence_id),("dependence_cluster_id",self.dependence_cluster_id),("symbol",self.symbol),("timeframe",self.timeframe),("feature_frame_hash",self.feature_frame_hash)): safe_id(v,n)
        if self.event_time_ms>self.decision_time_ms or self.decision_time_ms>self.known_time_ms: raise CausalityError("invalid_anchor_time_order","event <= decision <= known is required")
        for s in self.source_inventory:
            if s.available_time_ms>self.known_time_ms: raise CausalityError("future_source_in_anchor","source became available after anchor known time",{"source_id":s.source_id})
    def identity_material(self):
        return {"context_package_key":self.context_package_key,"context_occurrence_id":self.context_occurrence_id,"dependence_cluster_id":self.dependence_cluster_id,"symbol":self.symbol,"timeframe":self.timeframe,"side":self.side.value,"event_time_ms":self.event_time_ms,"decision_time_ms":self.decision_time_ms,"known_time_ms":self.known_time_ms,"feature_frame_hash":self.feature_frame_hash,"representation_hashes":dict(self.representation_hashes),"source_inventory":[x.to_dict() for x in self.source_inventory],"eligible":self.eligible,"ineligibility_reason":self.ineligibility_reason,"tags":dict(self.tags)}
    @property
    def opportunity_id(self): return stable_id("uceopp",self.identity_material())
    @property
    def anchor_hash(self): return sha256(self.identity_material())
    def to_dict(self): return {"opportunity_id":self.opportunity_id,"anchor_hash":self.anchor_hash,**self.identity_material()}

@dataclass(frozen=True, slots=True)
class PathObservation:
    sequence:int; event_time_ms:int; known_time_ms:int; bid:Decimal; ask:Decimal; available_volume:Decimal=Decimal("1"); source_revision:str="path.v1"; gap:bool=False
    def __post_init__(self):
        if self.sequence<0: raise ContractError("negative_sequence","path sequence must be nonnegative")
        if self.event_time_ms>self.known_time_ms: raise CausalityError("path_known_before_event","path known time precedes event")
        if self.ask<self.bid: raise ContractError("crossed_quote","ask cannot be below bid")
        if self.available_volume<0: raise ContractError("negative_available_volume","available volume cannot be negative")
    def to_dict(self): return {"sequence":self.sequence,"event_time_ms":self.event_time_ms,"known_time_ms":self.known_time_ms,"bid":self.bid,"ask":self.ask,"available_volume":self.available_volume,"source_revision":self.source_revision,"gap":self.gap}

@dataclass(frozen=True, slots=True)
class EconomicScenario:
    scenario_id:str; version:str; commission_cash:Decimal=Decimal("0"); slippage_price:Decimal=Decimal("0"); financing_cash:Decimal=Decimal("0"); gap_reserve_cash:Decimal=Decimal("0"); cost_multiplier:Decimal=Decimal("1")
    def __post_init__(self):
        safe_id(self.scenario_id,'scenario_id'); safe_id(self.version,'version')
        if self.cost_multiplier<0: raise ContractError("negative_cost_multiplier","cost multiplier cannot be negative")
    @property
    def exact_key(self): return f"{self.scenario_id}@{self.version}"
    @property
    def scenario_hash(self): return sha256(self.to_dict())
    def to_dict(self): return {"scenario_id":self.scenario_id,"version":self.version,"commission_cash":self.commission_cash,"slippage_price":self.slippage_price,"financing_cash":self.financing_cash,"gap_reserve_cash":self.gap_reserve_cash,"cost_multiplier":self.cost_multiplier}

@dataclass(frozen=True, slots=True)
class TreatmentSibling:
    treatment_id:str; treatment_family_id:str; side:TradeSide; entry_style:EntryStyle; entry_price:Decimal|None; stop_price:Decimal; target_price:Decimal|None;
    trail_distance:Decimal|None; entry_expiry_ms:int; exit_horizon_ms:int; volume:Decimal; cash_per_price_unit:Decimal; estimated_cost_cash:Decimal;
    maximum_loss_cash:Decimal; economic_envelope_hash:str; admissible:bool=True; rejection_reason:str=""; manual_baseline:bool=False; metadata:Mapping[str,Any]=field(default_factory=dict)
    def __post_init__(self):
        for n,v in (("treatment_id",self.treatment_id),("treatment_family_id",self.treatment_family_id),("economic_envelope_hash",self.economic_envelope_hash)): safe_id(v,n)
        if self.volume<=0 or self.cash_per_price_unit<=0: raise ContractError("invalid_treatment_scale","volume and cash-per-price-unit must be positive")
        if self.maximum_loss_cash<=0: raise ContractError("invalid_maximum_loss","maximum loss must be positive")
        if self.entry_expiry_ms<0 or self.exit_horizon_ms<=0: raise ContractError("invalid_treatment_horizon","entry expiry must be nonnegative and exit horizon positive")
    def to_dict(self): return {"treatment_id":self.treatment_id,"treatment_family_id":self.treatment_family_id,"side":self.side.value,"entry_style":self.entry_style.value,"entry_price":self.entry_price,"stop_price":self.stop_price,"target_price":self.target_price,"trail_distance":self.trail_distance,"entry_expiry_ms":self.entry_expiry_ms,"exit_horizon_ms":self.exit_horizon_ms,"volume":self.volume,"cash_per_price_unit":self.cash_per_price_unit,"estimated_cost_cash":self.estimated_cost_cash,"maximum_loss_cash":self.maximum_loss_cash,"economic_envelope_hash":self.economic_envelope_hash,"admissible":self.admissible,"rejection_reason":self.rejection_reason,"manual_baseline":self.manual_baseline,"metadata":canonical_value(self.metadata)}

@dataclass(frozen=True, slots=True)
class MaturityEvidence:
    state:OutcomeState; censoring:CensoringKind; observation_end_ms:int; required_end_ms:int; mature:bool; event_observed:bool; competing_event:str=""; reason:str=""
    @property
    def evidence_id(self): return stable_id("ucemat",self.to_dict())
    def to_dict(self): return {"state":self.state.value,"censoring":self.censoring.value,"observation_end_ms":self.observation_end_ms,"required_end_ms":self.required_end_ms,"mature":self.mature,"event_observed":self.event_observed,"competing_event":self.competing_event,"reason":self.reason}

@dataclass(frozen=True, slots=True)
class OutcomeCell:
    opportunity_id:str; treatment_id:str; scenario_key:str; horizon_ms:int; state:OutcomeState; terminal_reason:TerminalReason; maturity:MaturityEvidence;
    entry_time_ms:int|None; exit_time_ms:int|None; entry_price:Decimal|None; exit_price:Decimal|None; filled_fraction:Decimal; gross_pnl_cash:Decimal;
    total_cost_cash:Decimal; net_pnl_cash:Decimal; net_r:Decimal; mfe_r:Decimal; mae_r:Decimal; max_drawdown_r:Decimal; time_to_fill_ms:int|None;
    time_to_exit_ms:int|None; path_hash:str; economic_envelope_hash:str; tail_loss:bool=False; diagnostics:Mapping[str,Any]=field(default_factory=dict)
    def __post_init__(self):
        if not Decimal("0")<=self.filled_fraction<=Decimal("1"): raise ContractError("invalid_fill_fraction","fill fraction must be in [0,1]")
    @property
    def cell_id(self): return stable_id("ucecell",{"opportunity_id":self.opportunity_id,"treatment_id":self.treatment_id,"scenario_key":self.scenario_key,"horizon_ms":self.horizon_ms,"path_hash":self.path_hash,"economic_envelope_hash":self.economic_envelope_hash})
    def metric(self,name:str)->Decimal:
        values={"net_r":self.net_r,"net_pnl_cash":self.net_pnl_cash,"gross_pnl_cash":self.gross_pnl_cash,"mfe_r":self.mfe_r,"mae_r":self.mae_r,"max_drawdown_r":self.max_drawdown_r,"total_cost_cash":self.total_cost_cash,"filled_fraction":self.filled_fraction}
        if name not in values: raise ContractError("unknown_outcome_metric",f"unknown metric {name}")
        return values[name]
    def to_dict(self): return {"cell_id":self.cell_id,"opportunity_id":self.opportunity_id,"treatment_id":self.treatment_id,"scenario_key":self.scenario_key,"horizon_ms":self.horizon_ms,"state":self.state.value,"terminal_reason":self.terminal_reason.value,"maturity":self.maturity.to_dict(),"entry_time_ms":self.entry_time_ms,"exit_time_ms":self.exit_time_ms,"entry_price":self.entry_price,"exit_price":self.exit_price,"filled_fraction":self.filled_fraction,"gross_pnl_cash":self.gross_pnl_cash,"total_cost_cash":self.total_cost_cash,"net_pnl_cash":self.net_pnl_cash,"net_r":self.net_r,"mfe_r":self.mfe_r,"mae_r":self.mae_r,"max_drawdown_r":self.max_drawdown_r,"time_to_fill_ms":self.time_to_fill_ms,"time_to_exit_ms":self.time_to_exit_ms,"path_hash":self.path_hash,"economic_envelope_hash":self.economic_envelope_hash,"tail_loss":self.tail_loss,"diagnostics":canonical_value(self.diagnostics)}

@dataclass(frozen=True, slots=True)
class OutcomeCube:
    opportunity_id:str; anchor_hash:str; path_hash:str; treatment_matrix_hash:str; scenario_set_hash:str; cells:tuple[OutcomeCell,...]; compiler_version:str="3.0.0"
    @property
    def cube_hash(self): return sha256(self.to_dict(include_hash=False))
    def to_dict(self,include_hash:bool=True):
        d={"opportunity_id":self.opportunity_id,"anchor_hash":self.anchor_hash,"path_hash":self.path_hash,"treatment_matrix_hash":self.treatment_matrix_hash,"scenario_set_hash":self.scenario_set_hash,"cells":[x.to_dict() for x in sorted(self.cells,key=lambda c:(c.treatment_id,c.scenario_key,c.horizon_ms))],"compiler_version":self.compiler_version}
        if include_hash:d["cube_hash"]=sha256(d)
        return d

@dataclass(frozen=True, slots=True)
class LabelTaskContract:
    task_id:str; version:str; task_kind:TaskKind; metric:str; horizon_ms:int; scenario_key:str; threshold:Decimal=Decimal("0"); direction:UtilityDirection=UtilityDirection.MAXIMIZE;
    maturity_policies:tuple[LabelMaturityPolicy,...]=(LabelMaturityPolicy.REQUIRE_RESOLVED,); comparison_group:str="opportunity"; quantile:Decimal|None=None;
    bounded_min_utility:Decimal|None=None; allowed_terminal_reasons:tuple[str,...]=(); metadata:Mapping[str,Any]=field(default_factory=dict)
    def __post_init__(self):
        safe_id(self.task_id,'task_id'); safe_id(self.version,'version')
        if self.horizon_ms<=0: raise ContractError("invalid_label_horizon","label horizon must be positive")
        if self.quantile is not None and not Decimal("0")<self.quantile<Decimal("1"): raise ContractError("invalid_quantile","quantile must be in (0,1)")
    @property
    def exact_key(self): return f"{self.task_id}@{self.version}"
    @property
    def contract_hash(self): return sha256(self.to_dict())
    def to_dict(self): return {"task_id":self.task_id,"version":self.version,"task_kind":self.task_kind.value,"metric":self.metric,"horizon_ms":self.horizon_ms,"scenario_key":self.scenario_key,"threshold":self.threshold,"direction":self.direction.value,"maturity_policies":[x.value for x in self.maturity_policies],"comparison_group":self.comparison_group,"quantile":self.quantile,"bounded_min_utility":self.bounded_min_utility,"allowed_terminal_reasons":list(self.allowed_terminal_reasons),"metadata":canonical_value(self.metadata)}

@dataclass(frozen=True, slots=True)
class LabelRecord:
    opportunity_id:str; treatment_id:str; task_key:str; cell_id:str; mature:bool; mask:bool; scalar_value:Decimal|None=None; class_value:int|None=None;
    category_value:str=""; vector_value:tuple[Decimal,...]=(); duration_ms:int|None=None; event_observed:bool|None=None; competing_event:str=""; rank:int|None=None;
    sample_weight:Decimal=Decimal("1"); known_time_ms:int=0; reason:str=""; evidence_hash:str=""
    @property
    def label_id(self): return stable_id("ucelabel",self.to_dict(include_id=False))
    def to_dict(self,include_id:bool=True):
        d={"opportunity_id":self.opportunity_id,"treatment_id":self.treatment_id,"task_key":self.task_key,"cell_id":self.cell_id,"mature":self.mature,"mask":self.mask,"scalar_value":self.scalar_value,"class_value":self.class_value,"category_value":self.category_value,"vector_value":list(self.vector_value),"duration_ms":self.duration_ms,"event_observed":self.event_observed,"competing_event":self.competing_event,"rank":self.rank,"sample_weight":self.sample_weight,"known_time_ms":self.known_time_ms,"reason":self.reason,"evidence_hash":self.evidence_hash}
        if include_id:d["label_id"]=stable_id("ucelabel",d)
        return d

@dataclass(frozen=True, slots=True)
class FoldWindow:
    fold_id:str; train_start_ms:int; train_end_ms:int; test_start_ms:int; test_end_ms:int; purge_ms:int; embargo_ms:int
    def __post_init__(self): safe_id(self.fold_id,'fold_id')
    def to_dict(self): return {"fold_id":self.fold_id,"train_start_ms":self.train_start_ms,"train_end_ms":self.train_end_ms,"test_start_ms":self.test_start_ms,"test_end_ms":self.test_end_ms,"purge_ms":self.purge_ms,"embargo_ms":self.embargo_ms}

@dataclass(frozen=True, slots=True)
class SplitAssignment:
    fold_id:str; opportunity_id:str; dependence_cluster_id:str; role:FoldRole; decision_time_ms:int; reason:str=""
    @property
    def assignment_id(self): return stable_id("ucefold",self.to_dict())
    def to_dict(self): return {"fold_id":self.fold_id,"opportunity_id":self.opportunity_id,"dependence_cluster_id":self.dependence_cluster_id,"role":self.role.value,"decision_time_ms":self.decision_time_ms,"reason":self.reason}

@dataclass(frozen=True, slots=True)
class SplitPlan:
    plan_id:str; version:str; folds:tuple[FoldWindow,...]; assignments:tuple[SplitAssignment,...]; cluster_rule_hash:str; sibling_lock:bool=True; nested:bool=False
    @property
    def plan_hash(self): return sha256(self.to_dict(include_hash=False))
    def to_dict(self,include_hash:bool=True):
        d={"plan_id":self.plan_id,"version":self.version,"folds":[x.to_dict() for x in self.folds],"assignments":[x.to_dict() for x in sorted(self.assignments,key=lambda a:(a.fold_id,a.opportunity_id))],"cluster_rule_hash":self.cluster_rule_hash,"sibling_lock":self.sibling_lock,"nested":self.nested}
        if include_hash:d["plan_hash"]=sha256(d)
        return d

@dataclass(frozen=True, slots=True)
class TransformPlan:
    transform_id:str; version:str; fold_id:str; feature_names:tuple[str,...]; kinds:tuple[TransformKind,...]; fit_opportunity_ids:tuple[str,...]; parameters:Mapping[str,Any]; missingness_mask:bool=True
    @property
    def plan_hash(self): return sha256(self.to_dict(include_hash=False))
    def to_dict(self,include_hash:bool=True):
        d={"transform_id":self.transform_id,"version":self.version,"fold_id":self.fold_id,"feature_names":list(self.feature_names),"kinds":[x.value for x in self.kinds],"fit_opportunity_ids":list(sorted(self.fit_opportunity_ids)),"parameters":canonical_value(self.parameters),"missingness_mask":self.missingness_mask}
        if include_hash:d["plan_hash"]=sha256(d)
        return d

@dataclass(frozen=True, slots=True)
class DatasetRow:
    opportunity_id:str; treatment_id:str; cell_id:str; label_id:str; fold_roles:Mapping[str,str]; feature_frame_hash:str; representation_hashes:Mapping[str,str]; feature_values:Mapping[str,Decimal|None]; label:LabelRecord; row_known_time_ms:int; row_lineage_hash:str
    @property
    def row_id(self): return stable_id("ucerow",self.to_dict(include_id=False))
    def to_dict(self,include_id:bool=True):
        d={"opportunity_id":self.opportunity_id,"treatment_id":self.treatment_id,"cell_id":self.cell_id,"label_id":self.label_id,"fold_roles":dict(self.fold_roles),"feature_frame_hash":self.feature_frame_hash,"representation_hashes":dict(self.representation_hashes),"feature_values":canonical_value(self.feature_values),"label":self.label.to_dict(),"row_known_time_ms":self.row_known_time_ms,"row_lineage_hash":self.row_lineage_hash}
        if include_id:d["row_id"]=stable_id("ucerow",d)
        return d

@dataclass(frozen=True, slots=True)
class LeakageFinding:
    code:str; severity:LeakageSeverity; blocking:bool; message:str; evidence:Mapping[str,Any]=field(default_factory=dict)
    @property
    def finding_id(self): return stable_id("uceleak",self.to_dict())
    def to_dict(self): return {"code":self.code,"severity":self.severity.value,"blocking":self.blocking,"message":self.message,"evidence":canonical_value(self.evidence)}

@dataclass(frozen=True, slots=True)
class DatasetLeakageReport:
    dataset_id:str; findings:tuple[LeakageFinding,...]; future_perturbation_passed:bool; reproducibility_passed:bool; source_revision_passed:bool
    @property
    def blocked(self): return any(x.blocking for x in self.findings) or not(self.future_perturbation_passed and self.reproducibility_passed and self.source_revision_passed)
    @property
    def report_hash(self): return sha256(self.to_dict(include_hash=False))
    def to_dict(self,include_hash:bool=True):
        d={"dataset_id":self.dataset_id,"findings":[x.to_dict() for x in self.findings],"future_perturbation_passed":self.future_perturbation_passed,"reproducibility_passed":self.reproducibility_passed,"source_revision_passed":self.source_revision_passed,"blocked":self.blocked}
        if include_hash:d["report_hash"]=sha256(d)
        return d

@dataclass(frozen=True, slots=True)
class DatasetManifest:
    dataset_id:str; version:str; context_package_key:str; task_keys:tuple[str,...]; opportunity_count:int; treatment_count:int; row_count:int; anchor_table_hash:str; outcome_cube_set_hash:str; label_set_hash:str; split_plan_hash:str; transform_plan_hashes:tuple[str,...]; source_inventory_hash:str; code_hash:str; rows_hash:str; leakage_report_hash:str; created_time_ms:int=0
    @property
    def manifest_hash(self): return sha256(self.to_dict(include_hash=False))
    def to_dict(self,include_hash:bool=True):
        d={"dataset_id":self.dataset_id,"version":self.version,"context_package_key":self.context_package_key,"task_keys":list(self.task_keys),"opportunity_count":self.opportunity_count,"treatment_count":self.treatment_count,"row_count":self.row_count,"anchor_table_hash":self.anchor_table_hash,"outcome_cube_set_hash":self.outcome_cube_set_hash,"label_set_hash":self.label_set_hash,"split_plan_hash":self.split_plan_hash,"transform_plan_hashes":list(self.transform_plan_hashes),"source_inventory_hash":self.source_inventory_hash,"code_hash":self.code_hash,"rows_hash":self.rows_hash,"leakage_report_hash":self.leakage_report_hash,"created_time_ms":self.created_time_ms}
        if include_hash:d["manifest_hash"]=sha256(d)
        return d

@dataclass(frozen=True, slots=True)
class DatasetBuildReport:
    dataset_id:str; accepted:bool; anchor_count:int; cube_count:int; label_count:int; row_count:int; rejected_treatment_count:int; censored_count:int; masked_label_count:int; findings:tuple[str,...]; manifest_hash:str
    def to_dict(self): return {"dataset_id":self.dataset_id,"accepted":self.accepted,"anchor_count":self.anchor_count,"cube_count":self.cube_count,"label_count":self.label_count,"row_count":self.row_count,"rejected_treatment_count":self.rejected_treatment_count,"censored_count":self.censored_count,"masked_label_count":self.masked_label_count,"findings":list(self.findings),"manifest_hash":self.manifest_hash}
