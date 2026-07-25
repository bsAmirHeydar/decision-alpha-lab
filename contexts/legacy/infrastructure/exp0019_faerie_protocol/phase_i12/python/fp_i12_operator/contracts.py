from __future__ import annotations
from dataclasses import dataclass,replace
from .canonical import require_id,require_hash,sha256,stable_id,sorted_unique
from .constants import *
from .enums import *
from .errors import FPI12Error

@dataclass(frozen=True,slots=True)
class OperatorItem:
    semantic_id:str; object_id:str; kind:str; relation:str=''; direction:str='NONE'; state:str=''; disposition:str=''; session_kind:str='NONE'; symbol:str=''; event_time:int=0; is_historical:bool=False; reason_codes:tuple[str,...]=(); semantic_hash:str=''
    def __post_init__(self):
        require_id(self.semantic_id,'semantic_id');require_id(self.object_id,'object_id')
        if self.relation and self.relation not in ALLOWED_RELATIONS: raise FPI12Error('FP_UX_RELATION_INVALID','relation invalid')
        if self.direction not in ALLOWED_DIRECTIONS: raise FPI12Error('FP_UX_DIRECTION_INVALID','direction invalid')
        if self.session_kind not in ALLOWED_SESSIONS: raise FPI12Error('FP_UX_SESSION_INVALID','session invalid')
        if self.event_time<0: raise FPI12Error('FP_UX_TIME_INVALID','event time invalid')
        if self.semantic_hash: require_hash(self.semantic_hash,'semantic_hash')
        if self.reason_codes!=sorted_unique(self.reason_codes): raise FPI12Error('FP_UX_REASONS_NONCANONICAL','reasons must be sorted unique')

@dataclass(frozen=True,slots=True)
class PanelConfig:
    enabled:bool=True; dock:PanelDock=PanelDock.TOP_RIGHT; state:PanelState=PanelState.EXPANDED; mode:PanelMode=PanelMode.TRADING; page_size:int=DEFAULT_PAGE_SIZE; show_open_decisions:bool=True
    def __post_init__(self):
        if not 1<=self.page_size<=MAX_PAGE_SIZE: raise FPI12Error('FP_UX_PAGE_SIZE_INVALID','page size outside policy')
    @property
    def config_hash(self): return sha256(self)

@dataclass(frozen=True,slots=True)
class FilterConfig:
    relations:tuple[str,...]=ALLOWED_RELATIONS; directions:tuple[str,...]=('BEARISH','BULLISH','NONE'); states:tuple[str,...]=(); dispositions:tuple[str,...]=(); sessions:tuple[str,...]=('A','L','N','NONE','W'); symbols:tuple[str,...]=(); kinds:tuple[str,...]=(); include_historical:bool=True; focus_semantic_id:str=''
    def __post_init__(self):
        if any(x not in ALLOWED_RELATIONS for x in self.relations): raise FPI12Error('FP_UX_FILTER_RELATION_INVALID','invalid relation filter')
        if any(x not in ALLOWED_DIRECTIONS for x in self.directions): raise FPI12Error('FP_UX_FILTER_DIRECTION_INVALID','invalid direction filter')
        if any(x not in ALLOWED_SESSIONS for x in self.sessions): raise FPI12Error('FP_UX_FILTER_SESSION_INVALID','invalid session filter')
        if self.focus_semantic_id: require_id(self.focus_semantic_id,'focus_semantic_id')
        for name,values in [('relations',self.relations),('directions',self.directions),('states',self.states),('dispositions',self.dispositions),('sessions',self.sessions),('symbols',self.symbols),('kinds',self.kinds)]:
            if tuple(values)!=sorted_unique(values): raise FPI12Error('FP_UX_FILTER_NONCANONICAL',f'{name} must be sorted unique')
    @property
    def filter_hash(self): return sha256(self)

@dataclass(frozen=True,slots=True)
class AlertConfig:
    enabled:bool=True; channels:tuple[AlertChannel,...]=(AlertChannel.LOG,); suppress_historical:bool=True; startup_watermark:int=0; max_per_minute:int=DEFAULT_ALERT_RATE_PER_MINUTE; alert_types:tuple[AlertType,...]=tuple(sorted(AlertType,key=lambda x:x.value))
    def __post_init__(self):
        if self.startup_watermark<0: raise FPI12Error('FP_ALERT_WATERMARK_INVALID','watermark invalid')
        if not 1<=self.max_per_minute<=MAX_ALERT_RATE_PER_MINUTE: raise FPI12Error('FP_ALERT_RATE_INVALID','rate invalid')
        if tuple(self.channels)!=tuple(sorted(set(self.channels),key=lambda x:x.value)): raise FPI12Error('FP_ALERT_CHANNELS_NONCANONICAL','channels must be sorted unique')
        if tuple(self.alert_types)!=tuple(sorted(set(self.alert_types),key=lambda x:x.value)): raise FPI12Error('FP_ALERT_TYPES_NONCANONICAL','types must be sorted unique')
    @property
    def config_hash(self): return sha256(self)

@dataclass(frozen=True,slots=True)
class ExportConfig:
    enabled:bool=False; formats:tuple[ExportFormat,...]=(ExportFormat.CSV,ExportFormat.JSONL); include_suppressed:bool=True; include_blocked:bool=True; file_prefix:str='EXP0019_FP_AUDIT'; auto_export_on_change:bool=False
    def __post_init__(self):
        if not self.file_prefix or any(c in self.file_prefix for c in '<>:"/|?*'): raise FPI12Error('FP_EXPORT_PREFIX_INVALID','file prefix invalid')
        if tuple(self.formats)!=tuple(sorted(set(self.formats),key=lambda x:x.value)): raise FPI12Error('FP_EXPORT_FORMATS_NONCANONICAL','formats must be sorted unique')
    @property
    def config_hash(self): return sha256(self)

@dataclass(frozen=True,slots=True)
class OperatorConfig:
    instance_id:str; object_namespace:str; panel:PanelConfig=PanelConfig(); filters:FilterConfig=FilterConfig(); alerts:AlertConfig=AlertConfig(); export:ExportConfig=ExportConfig(); open_decision_state:str='UNSET'
    def __post_init__(self):
        require_id(self.instance_id,'instance_id')
        if not self.object_namespace.startswith('FP19::'): raise FPI12Error('FP_UX_NAMESPACE_INVALID','namespace must be instance scoped')
        if self.open_decision_state not in ('UNSET','RESOLVED'): raise FPI12Error('FP_UX_DECISION_STATE_INVALID','decision state invalid')
    @property
    def config_hash(self): return sha256(self)

@dataclass(frozen=True,slots=True)
class OperatorSnapshot:
    snapshot_id:str; generated_at:int; revision_id:str; health:OperatorHealth; data_readiness:str; active_ww_direction:str; quota_winner_signal_id:str; ledger_event_count:int; source_revision_sequence:int; items:tuple[OperatorItem,...]; open_decision_state:str='UNSET'; snapshot_hash:str=''
    def __post_init__(self):
        require_id(self.snapshot_id,'snapshot_id');require_id(self.revision_id,'revision_id')
        if self.generated_at<0 or self.ledger_event_count<0 or self.source_revision_sequence<0: raise FPI12Error('FP_UX_SNAPSHOT_INVALID','snapshot counters invalid')
        if self.quota_winner_signal_id: require_id(self.quota_winner_signal_id,'quota_winner_signal_id')
        if self.open_decision_state not in ('UNSET','RESOLVED'): raise FPI12Error('FP_UX_DECISION_STATE_INVALID','decision state invalid')
        if self.snapshot_hash: require_hash(self.snapshot_hash,'snapshot_hash')
    @property
    def computed_hash(self): return sha256(replace(self,snapshot_hash=''))

@dataclass(frozen=True,slots=True)
class FilterDecisionRecord:
    semantic_id:str; outcome:FilterOutcome; reason_code:str; filter_hash:str
@dataclass(frozen=True,slots=True)
class FilterResult:
    included:tuple[OperatorItem,...]; excluded:tuple[FilterDecisionRecord,...]; filter_hash:str; source_snapshot_hash:str; result_hash:str

@dataclass(frozen=True,slots=True)
class PanelMetric:
    key:str; label:str; value:str; severity:str='INFO'
@dataclass(frozen=True,slots=True)
class PanelSection:
    section_id:str; title:str; metrics:tuple[PanelMetric,...]
@dataclass(frozen=True,slots=True)
class PanelModel:
    panel_id:str; instance_id:str; mode:PanelMode; state:PanelState; dock:PanelDock; page:int; page_count:int; total_items:int; sections:tuple[PanelSection,...]; visible_item_ids:tuple[str,...]; panel_hash:str

@dataclass(frozen=True,slots=True)
class AlertCandidate:
    semantic_id:str; alert_type:AlertType; event_time:int; severity:AlertSeverity; title:str; message:str; is_historical:bool=False; payload_hash:str=''
    def __post_init__(self):
        require_id(self.semantic_id,'semantic_id')
        if self.event_time<0: raise FPI12Error('FP_ALERT_TIME_INVALID','event time invalid')
        if self.payload_hash: require_hash(self.payload_hash,'payload_hash')
    @property
    def alert_id(self): return stable_id('FPALERT',{'semantic_id':self.semantic_id,'type':self.alert_type.value,'version':ALERT_VERSION})

@dataclass(frozen=True,slots=True)
class AlertDelivery:
    alert_id:str; channel:AlertChannel; disposition:AlertDisposition; delivered_at:int; reason_code:str
@dataclass(frozen=True,slots=True)
class AlertEvent:
    alert_id:str; candidate:AlertCandidate; deliveries:tuple[AlertDelivery,...]; disposition:AlertDisposition; acknowledged:bool; event_hash:str
@dataclass(frozen=True,slots=True)
class AlertStateSnapshot:
    instance_id:str; delivered_ids:tuple[str,...]; acknowledged_ids:tuple[str,...]; minute_buckets:tuple[tuple[int,int],...]; state_hash:str

@dataclass(frozen=True,slots=True)
class AuditRecord:
    record_id:str; instance_id:str; snapshot_id:str; semantic_id:str; record_type:str; event_time:int; relation:str; direction:str; state:str; disposition:str; session_kind:str; symbol:str; reason_codes:tuple[str,...]; source_revision_sequence:int; payload_hash:str
@dataclass(frozen=True,slots=True)
class ExportBatch:
    batch_id:str; format:ExportFormat; records:tuple[AuditRecord,...]; appended_count:int; duplicate_count:int; content:str; content_hash:str; disposition:ExportDisposition

@dataclass(frozen=True,slots=True)
class OperatorPreferences:
    panel:PanelConfig; filters:FilterConfig; acknowledged_alert_ids:tuple[str,...]=(); page:int=0; preferences_hash:str=''
    @property
    def computed_hash(self): return sha256(replace(self,preferences_hash=''))

@dataclass(frozen=True,slots=True)
class ActionRequest:
    action_id:str; action:OperatorAction; value:str=''; requested_at:int=0
    def __post_init__(self): require_id(self.action_id,'action_id')
@dataclass(frozen=True,slots=True)
class ActionResult:
    action_id:str; disposition:ActionDisposition; reason_code:str; preferences:OperatorPreferences; rebuild_requested:bool=False; export_requested:bool=False

@dataclass(frozen=True,slots=True)
class OperatorCheckpoint:
    checkpoint_id:str; version:str; instance_id:str; config_hash:str; preferences:OperatorPreferences; alert_state:AlertStateSnapshot; last_snapshot_hash:str; payload_hash:str

@dataclass(frozen=True,slots=True)
class OperatorDiagnostic:
    diagnostic_id:str; health:OperatorHealth; panel_hash:str; filter_hash:str; alert_state_hash:str; last_export_hash:str; reason_codes:tuple[str,...]; diagnostic_hash:str

@dataclass(frozen=True,slots=True)
class OperatorOutput:
    output_id:str; snapshot_hash:str; panel:PanelModel; filters:FilterResult; alerts:tuple[AlertEvent,...]; exports:tuple[ExportBatch,...]; preferences:OperatorPreferences; diagnostic:OperatorDiagnostic; output_hash:str
