from __future__ import annotations
from dataclasses import dataclass,field,asdict
from typing import Any,Mapping
from .canonical import content_hash,stable_id
from .enums import EventKind,ClockDomain,LatePolicy,AppendDisposition,ProjectionReducer,ProjectionStatus,AlignmentStatus,GapSeverity

@dataclass(frozen=True)
class EventAuthorityBoundary:
    read_twin:bool=True; register_stream:bool=True; append_event:bool=True; build_projection:bool=True; replay:bool=True
    mutate_ucee_truth:bool=False; mutate_twin_manifest:bool=False; select_treatment:bool=False; allocate_risk:bool=False; activate_runtime:bool=False; send_order:bool=False; network_access:bool=False
    def to_dict(self):return asdict(self)

@dataclass(frozen=True)
class EventSourceDescriptor:
    source_id:str; source_version:str; clock_domain:ClockDomain; source_hash:str; trusted:bool; timezone:str='UTC'; metadata:Mapping[str,Any]=field(default_factory=dict)
    @property
    def descriptor_hash(self):return content_hash({**asdict(self),'clock_domain':self.clock_domain.value,'metadata':dict(self.metadata)})

@dataclass(frozen=True)
class EventStreamManifest:
    stream_id:str; exact_version:str; twin_id:str; source:EventSourceDescriptor; subject_ids:tuple[str,...]; accepted_kinds:tuple[EventKind,...]; source_priority:int; maximum_lateness_ms:int; late_policy:LatePolicy; schema_version:str; authority:EventAuthorityBoundary; limitations:tuple[str,...]=()
    def semantic_payload(self):
        return {'stream_id':self.stream_id,'exact_version':self.exact_version,'twin_id':self.twin_id,'source':{**asdict(self.source),'clock_domain':self.source.clock_domain.value,'metadata':dict(self.source.metadata)},'subject_ids':sorted(self.subject_ids),'accepted_kinds':sorted(x.value for x in self.accepted_kinds),'source_priority':self.source_priority,'maximum_lateness_ms':self.maximum_lateness_ms,'late_policy':self.late_policy.value,'schema_version':self.schema_version,'authority':self.authority.to_dict(),'limitations':sorted(self.limitations)}
    @property
    def semantic_hash(self):return content_hash(self.semantic_payload())

@dataclass(frozen=True)
class EventEnvelope:
    stream_id:str; stream_version:str; twin_id:str; source_id:str; source_sequence:int; event_kind:EventKind; subject_id:str; event_time:str; known_time:str; payload:Mapping[str,Any]; payload_hash:str; source_hash:str; correlation_id:str|None=None; correction_of:str|None=None; tags:tuple[str,...]=()
    def identity_payload(self):
        return {'stream_id':self.stream_id,'stream_version':self.stream_version,'twin_id':self.twin_id,'source_id':self.source_id,'source_sequence':self.source_sequence,'event_kind':self.event_kind.value,'subject_id':self.subject_id,'event_time':self.event_time,'known_time':self.known_time,'payload_hash':self.payload_hash,'source_hash':self.source_hash,'correlation_id':self.correlation_id,'correction_of':self.correction_of,'tags':sorted(self.tags)}
    @property
    def event_id(self):return stable_id('evt',self.identity_payload())
    @property
    def envelope_hash(self):return content_hash({**self.identity_payload(),'payload':dict(self.payload)})

@dataclass(frozen=True)
class EventBatch:
    batch_id:str; stream_id:str; stream_version:str; events:tuple[EventEnvelope,...]; batch_hash:str

@dataclass(frozen=True)
class AppendResult:
    batch_id:str; disposition:AppendDisposition; committed_event_ids:tuple[str,...]; idempotent_event_ids:tuple[str,...]; quarantined_event_ids:tuple[str,...]; reasons:tuple[str,...]; head_sequence:int; journal_root:str

@dataclass(frozen=True)
class WatermarkState:
    stream_id:str; maximum_event_time:str|None; watermark_time:str|None; maximum_lateness_ms:int; accepted_events:int; late_events:int
    @property
    def watermark_id(self):return stable_id('wm',asdict(self))

@dataclass(frozen=True)
class LateEventRecord:
    event_id:str; stream_id:str; event_time:str; observed_watermark:str; policy:LatePolicy; disposition:AppendDisposition; reason:str
    @property
    def record_id(self):return stable_id('late',asdict(self))

@dataclass(frozen=True)
class GapRecord:
    stream_id:str; subject_id:str; left_event_id:str|None; right_event_id:str|None; gap_start:str; gap_end:str; duration_ms:int; severity:GapSeverity; reason:str
    @property
    def gap_id(self):return stable_id('gap',asdict(self))

@dataclass(frozen=True)
class ProjectionFieldDefinition:
    field_id:str; event_kinds:tuple[EventKind,...]; payload_path:str; reducer:ProjectionReducer; window_seconds:int|None=None; subject_ids:tuple[str,...]=(); required:bool=False; maximum_staleness_ms:int|None=None; default:Any=None

@dataclass(frozen=True)
class EventProjectionDefinition:
    projection_name:str; exact_version:str; twin_id:str; fields:tuple[ProjectionFieldDefinition,...]; description:str; limitations:tuple[str,...]=()
    def semantic_payload(self):
        return {'projection_name':self.projection_name,'exact_version':self.exact_version,'twin_id':self.twin_id,'fields':[{'field_id':f.field_id,'event_kinds':sorted(x.value for x in f.event_kinds),'payload_path':f.payload_path,'reducer':f.reducer.value,'window_seconds':f.window_seconds,'subject_ids':sorted(f.subject_ids),'required':f.required,'maximum_staleness_ms':f.maximum_staleness_ms,'default':f.default} for f in sorted(self.fields,key=lambda x:x.field_id)],'description':self.description,'limitations':sorted(self.limitations)}
    @property
    def projection_id(self):return stable_id('projdef',self.semantic_payload())
    @property
    def semantic_hash(self):return content_hash(self.semantic_payload())

@dataclass(frozen=True)
class ProjectionValue:
    field_id:str; value:Any; event_ids:tuple[str,...]; last_event_time:str|None; stale:bool; missing:bool

@dataclass(frozen=True)
class EventStateProjection:
    projection_id:str; projection_version:str; twin_id:str; known_as_of:str; event_as_of:str; status:ProjectionStatus; values:tuple[ProjectionValue,...]; included_event_ids:tuple[str,...]; late_event_ids:tuple[str,...]; gap_ids:tuple[str,...]; watermark_ids:tuple[str,...]; sequence:int; state_hash:str

@dataclass(frozen=True)
class AlignmentEntry:
    subject_id:str; event_id:str|None; event_time:str|None; age_ms:int|None; stale:bool; payload_hash:str|None

@dataclass(frozen=True)
class AlignmentSnapshot:
    twin_id:str; known_as_of:str; event_as_of:str; status:AlignmentStatus; entries:tuple[AlignmentEntry,...]; missing_subjects:tuple[str,...]; stale_subjects:tuple[str,...]
    @property
    def alignment_id(self):return stable_id('align',asdict(self))

@dataclass(frozen=True)
class EventIntegrityReceipt:
    twin_id:str; journal_root:str; projection_hash:str|None; stream_manifest_hashes:tuple[str,...]; watermark_ids:tuple[str,...]; component_root:str; status:str; details:Mapping[str,Any]=field(default_factory=dict)
    @property
    def receipt_id(self):return stable_id('evtreceipt',asdict(self))

@dataclass(frozen=True)
class EventReplayReceipt:
    projection_id:str; known_as_of:str; event_as_of:str; expected_state_hash:str; observed_state_hash:str; event_count:int; status:str
    @property
    def receipt_id(self):return stable_id('evtreplay',asdict(self))
