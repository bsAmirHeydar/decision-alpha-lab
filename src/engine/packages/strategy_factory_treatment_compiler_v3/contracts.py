from __future__ import annotations
from dataclasses import dataclass,field
from decimal import Decimal
from typing import Any,Mapping
from strategy_factory_treatments_v3.enums import TradeSide,RuntimeMode,TreatmentKind
from strategy_factory_treatments_v3.plans import EntryPlan,StopPlan,TargetPlan,TrailingPlan,ManagementPlan,SizingPlan
from .enums import *
from .utils import stable_id,canonical_value,safe_id,dec

@dataclass(frozen=True,slots=True)
class AtomSelection:
    role:TreatmentKind; exact_key:str; parameters:Mapping[str,Any]=field(default_factory=dict); alias:str=''
    def __post_init__(self): safe_id(self.exact_key,'exact_key')
    @property
    def selection_id(self): return stable_id('ucesel',self.to_dict())
    def to_dict(self): return {'role':self.role.value,'exact_key':self.exact_key,'parameters':canonical_value(self.parameters),'alias':self.alias}

@dataclass(frozen=True,slots=True)
class CompatibilityRule:
    rule_id:str; version:str; rule_type:RuleType; severity:RuleSeverity=RuleSeverity.ERROR; subject:str=''; object_value:str='';
    operator:str=''; threshold:Decimal|None=None; message:str=''; applies_to_modes:tuple[str,...]=()
    def __post_init__(self): safe_id(self.rule_id,'rule_id'); safe_id(self.version,'version')
    @property
    def exact_key(self): return f'{self.rule_id}@{self.version}'
    @property
    def definition_id(self): return stable_id('ucerule',self.to_dict())
    def to_dict(self): return {'rule_id':self.rule_id,'version':self.version,'rule_type':self.rule_type.value,'severity':self.severity.value,'subject':self.subject,'object_value':self.object_value,'operator':self.operator,'threshold':self.threshold,'message':self.message,'applies_to_modes':list(self.applies_to_modes)}

@dataclass(frozen=True,slots=True)
class RuleFinding:
    rule_definition_id:str; passed:bool; severity:RuleSeverity; code:str; message:str; evidence:Mapping[str,Any]=field(default_factory=dict)
    def to_dict(self): return {'rule_definition_id':self.rule_definition_id,'passed':self.passed,'severity':self.severity.value,'code':self.code,'message':self.message,'evidence':canonical_value(self.evidence)}

@dataclass(frozen=True,slots=True)
class IntrabarPolicy:
    policy_id:str='intrabar.canonical'; version:str='1.0.0'; fidelity:FidelityMode=FidelityMode.BAR; ambiguity:AmbiguityPolicy=AmbiguityPolicy.WORST_CASE;
    gap:GapPolicy=GapPolicy.WORST_EXECUTABLE; partial_priority:PartialFillPriority=PartialFillPriority.FIFO; stale_quote:StaleQuotePolicy=StaleQuotePolicy.REJECT;
    max_quote_age_ms:int=2000; latency_ms:int=0
    def __post_init__(self): safe_id(self.policy_id,'policy_id')
    @property
    def definition_id(self): return stable_id('uceip',self.to_dict())
    def to_dict(self): return {'policy_id':self.policy_id,'version':self.version,'fidelity':self.fidelity.value,'ambiguity':self.ambiguity.value,'gap':self.gap.value,'partial_priority':self.partial_priority.value,'stale_quote':self.stale_quote.value,'max_quote_age_ms':self.max_quote_age_ms,'latency_ms':self.latency_ms}

@dataclass(frozen=True,slots=True)
class TreatmentDraft:
    draft_name:str; side:TradeSide; runtime_mode:RuntimeMode; compiler_mode:CompilerMode; selections:tuple[AtomSelection,...];
    intrabar_policy:IntrabarPolicy=field(default_factory=IntrabarPolicy); market_mode:MarketMode=MarketMode.ANY; account_mode:AccountMode=AccountMode.ANY;
    required_capabilities:tuple[str,...]=(); tags:Mapping[str,str]=field(default_factory=dict); pinned:bool=False
    def __post_init__(self): safe_id(self.draft_name,'draft_name')
    @property
    def draft_id(self): return stable_id('ucedraft',self.to_dict())
    def to_dict(self): return {'draft_name':self.draft_name,'side':self.side.value,'runtime_mode':self.runtime_mode.value,'compiler_mode':self.compiler_mode.value,'selections':[x.to_dict() for x in self.selections],'intrabar_policy':self.intrabar_policy.to_dict(),'market_mode':self.market_mode.value,'account_mode':self.account_mode.value,'required_capabilities':list(self.required_capabilities),'tags':canonical_value(self.tags),'pinned':self.pinned}

@dataclass(frozen=True,slots=True)
class ActionStep:
    sequence:int; phase:str; action_type:str; source_exact_key:str; source_plan_id:str; priority:int; payload:Mapping[str,Any]
    def to_dict(self): return {'sequence':self.sequence,'phase':self.phase,'action_type':self.action_type,'source_exact_key':self.source_exact_key,'source_plan_id':self.source_plan_id,'priority':self.priority,'payload':canonical_value(self.payload)}

@dataclass(frozen=True,slots=True)
class CompiledTreatment:
    treatment_id:str; draft_id:str; context_occurrence_id:str; feature_frame_hash:str; side:TradeSide; decision_time_ms:int;
    entry:EntryPlan; stop:StopPlan; target:TargetPlan; trailing:TrailingPlan; management:tuple[ManagementPlan,...]; sizing:SizingPlan;
    selections:tuple[AtomSelection,...]; action_order:tuple[ActionStep,...]; required_capabilities:tuple[str,...]; compatibility_findings:tuple[RuleFinding,...];
    intrabar_policy:IntrabarPolicy; compiler_version:str; manual_baseline:bool=False; metadata:Mapping[str,Any]=field(default_factory=dict)
    def to_dict(self): return {'treatment_id':self.treatment_id,'draft_id':self.draft_id,'context_occurrence_id':self.context_occurrence_id,'feature_frame_hash':self.feature_frame_hash,'side':self.side.value,'decision_time_ms':self.decision_time_ms,'entry':self.entry.to_dict(),'stop':self.stop.to_dict(),'target':self.target.to_dict(),'trailing':self.trailing.to_dict(),'management':[x.to_dict() for x in self.management],'sizing':self.sizing.to_dict(),'selections':[x.to_dict() for x in self.selections],'action_order':[x.to_dict() for x in self.action_order],'required_capabilities':list(self.required_capabilities),'compatibility_findings':[x.to_dict() for x in self.compatibility_findings],'intrabar_policy':self.intrabar_policy.to_dict(),'compiler_version':self.compiler_version,'manual_baseline':self.manual_baseline,'metadata':canonical_value(self.metadata)}

@dataclass(frozen=True,slots=True)
class CompileReport:
    draft_id:str; accepted:bool; findings:tuple[RuleFinding,...]; treatment_id:str=''; duration_us:int=0; telemetry:Mapping[str,int]=field(default_factory=dict)
    def to_dict(self): return {'draft_id':self.draft_id,'accepted':self.accepted,'findings':[x.to_dict() for x in self.findings],'treatment_id':self.treatment_id,'duration_us':self.duration_us,'telemetry':dict(self.telemetry)}

@dataclass(frozen=True,slots=True)
class PathEvent:
    sequence:int; event_type:PathEventType; event_time_ms:int; known_time_ms:int; price:Decimal|None=None; quantity_fraction:Decimal=Decimal('0');
    source:str=''; reason:str=''; metadata:Mapping[str,Any]=field(default_factory=dict)
    @property
    def event_id(self): return stable_id('ucepe',self.to_dict())
    def to_dict(self): return {'sequence':self.sequence,'event_type':self.event_type.value,'event_time_ms':self.event_time_ms,'known_time_ms':self.known_time_ms,'price':self.price,'quantity_fraction':self.quantity_fraction,'source':self.source,'reason':self.reason,'metadata':canonical_value(self.metadata)}

@dataclass(frozen=True,slots=True)
class PathSnapshot:
    treatment_id:str; state:PathState; last_sequence:int; last_event_time_ms:int; last_known_time_ms:int; filled_fraction:Decimal=Decimal('0');
    open_fraction:Decimal=Decimal('0'); exited_fraction:Decimal=Decimal('0'); average_entry_price:Decimal|None=None; active_stop_price:Decimal|None=None;
    last_trail_price:Decimal|None=None; terminal_reason:str=''; transition_count:int=0
    @property
    def snapshot_id(self): return stable_id('uceps',self.to_dict())
    def to_dict(self): return {'treatment_id':self.treatment_id,'state':self.state.value,'last_sequence':self.last_sequence,'last_event_time_ms':self.last_event_time_ms,'last_known_time_ms':self.last_known_time_ms,'filled_fraction':self.filled_fraction,'open_fraction':self.open_fraction,'exited_fraction':self.exited_fraction,'average_entry_price':self.average_entry_price,'active_stop_price':self.active_stop_price,'last_trail_price':self.last_trail_price,'terminal_reason':self.terminal_reason,'transition_count':self.transition_count}

@dataclass(frozen=True,slots=True)
class BarObservation:
    open_time_ms:int; close_time_ms:int; open:Decimal; high:Decimal; low:Decimal; close:Decimal; known_time_ms:int
    def to_dict(self): return {'open_time_ms':self.open_time_ms,'close_time_ms':self.close_time_ms,'open':self.open,'high':self.high,'low':self.low,'close':self.close,'known_time_ms':self.known_time_ms}

@dataclass(frozen=True,slots=True)
class MatrixAxisValue:
    exact_key:str; parameters:Mapping[str,Any]=field(default_factory=dict); alias:str=''
    def to_dict(self): return {'exact_key':self.exact_key,'parameters':canonical_value(self.parameters),'alias':self.alias}
@dataclass(frozen=True,slots=True)
class MatrixAxis:
    role:TreatmentKind; values:tuple[MatrixAxisValue,...]; allow_multiple:bool=False
    def to_dict(self): return {'role':self.role.value,'values':[x.to_dict() for x in self.values],'allow_multiple':self.allow_multiple}
@dataclass(frozen=True,slots=True)
class MatrixSpec:
    matrix_id:str; version:str; side:TradeSide; runtime_mode:RuntimeMode; compiler_mode:CompilerMode; axes:tuple[MatrixAxis,...];
    intrabar_policies:tuple[IntrabarPolicy,...]=(IntrabarPolicy(),); max_combinations:int=10000; max_compiled:int=1000; overflow_policy:MatrixOverflowPolicy=MatrixOverflowPolicy.REJECT; seed:int=0; tags:Mapping[str,str]=field(default_factory=dict)
    def __post_init__(self): safe_id(self.matrix_id,'matrix_id')
    @property
    def definition_id(self): return stable_id('ucemx',self.to_dict())
    def to_dict(self): return {'matrix_id':self.matrix_id,'version':self.version,'side':self.side.value,'runtime_mode':self.runtime_mode.value,'compiler_mode':self.compiler_mode.value,'axes':[x.to_dict() for x in self.axes],'intrabar_policies':[x.to_dict() for x in self.intrabar_policies],'max_combinations':self.max_combinations,'max_compiled':self.max_compiled,'overflow_policy':self.overflow_policy.value,'seed':self.seed,'tags':canonical_value(self.tags)}

@dataclass(frozen=True,slots=True)
class MatrixResult:
    matrix_definition_id:str; generated_count:int; compiled_count:int; rejected_count:int; truncated_count:int; treatment_ids:tuple[str,...]; rejection_codes:Mapping[str,int]; deterministic_order_hash:str
    def to_dict(self): return {'matrix_definition_id':self.matrix_definition_id,'generated_count':self.generated_count,'compiled_count':self.compiled_count,'rejected_count':self.rejected_count,'truncated_count':self.truncated_count,'treatment_ids':list(self.treatment_ids),'rejection_codes':dict(self.rejection_codes),'deterministic_order_hash':self.deterministic_order_hash}

@dataclass(frozen=True,slots=True)
class ManualTreatmentBundle:
    bundle_id:str; version:str; owner_id:str; draft:TreatmentDraft; expected_treatment_id:str=''; approval_note:str=''; frozen:bool=True
    def __post_init__(self): safe_id(self.bundle_id,'bundle_id'); safe_id(self.version,'version'); safe_id(self.owner_id,'owner_id')
    @property
    def definition_id(self): return stable_id('ucemb',self.to_dict())
    def to_dict(self): return {'bundle_id':self.bundle_id,'version':self.version,'owner_id':self.owner_id,'draft':self.draft.to_dict(),'expected_treatment_id':self.expected_treatment_id,'approval_note':self.approval_note,'frozen':self.frozen}
