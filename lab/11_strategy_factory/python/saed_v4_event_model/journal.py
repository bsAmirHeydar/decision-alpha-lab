from __future__ import annotations
from collections import defaultdict
from .canonical import content_hash,merkle_root
from .models import EventBatch,AppendResult
from .enums import AppendDisposition,EventKind,LatePolicy
from .errors import JournalError,SequenceError,DuplicateConflict,CorrectionError,LateEventError
from .temporal import validate_event_times,canonical_event_key
class EventJournal:
    def __init__(self,registry,watermarks):
        self.registry=registry;self.watermarks=watermarks;self._events={};self._streams=defaultdict(list);self._heads=defaultdict(int);self._quarantine=[]
    def _validate(self,manifest,event,expected_sequence):
        if event.stream_id!=manifest.stream_id or event.stream_version!=manifest.exact_version:raise JournalError('stream identity mismatch')
        if event.twin_id!=manifest.twin_id:raise JournalError('twin mismatch')
        if event.source_id!=manifest.source.source_id or event.source_hash!=manifest.source.source_hash:raise JournalError('source mismatch')
        if event.subject_id not in manifest.subject_ids:raise JournalError('subject not allowed')
        if event.event_kind not in manifest.accepted_kinds:raise JournalError('event kind not allowed')
        if content_hash(dict(event.payload))!=event.payload_hash:raise JournalError('payload hash mismatch')
        validate_event_times(event)
        if event.source_sequence!=expected_sequence:raise SequenceError(f'expected sequence {expected_sequence}, got {event.source_sequence}')
        if event.event_kind==EventKind.CORRECTION:
            if not event.correction_of or event.correction_of not in self._events:raise CorrectionError('unknown correction target')
            target=self._events[event.correction_of]
            if target.stream_id!=event.stream_id:raise CorrectionError('cross-stream correction forbidden')
            if 'replacement_payload' not in event.payload:raise CorrectionError('replacement_payload required')
    def append(self,batch:EventBatch)->AppendResult:
        manifest=self.registry.get(batch.stream_id,batch.stream_version)
        if content_hash([e.envelope_hash for e in batch.events])!=batch.batch_hash:raise JournalError('batch hash mismatch')
        committed=[];idem=[];quarantined=[];pending=[];next_seq=self._heads[batch.stream_id]+1
        for event in batch.events:
            old=self._events.get(event.event_id)
            if old:
                if old.envelope_hash!=event.envelope_hash:raise DuplicateConflict('event id conflict')
                idem.append(event.event_id);continue
            self._validate(manifest,event,next_seq);next_seq+=1
            late,record=self.watermarks.classify(manifest,event)
            if late and manifest.late_policy==LatePolicy.REJECT:raise LateEventError('late event rejected')
            if late and manifest.late_policy==LatePolicy.QUARANTINE:
                quarantined.append(event.event_id);self._quarantine.append(event);self.watermarks.add_late(record);continue
            pending.append((event,late,record));committed.append(event.event_id)
        for event,late,record in pending:
            self._events[event.event_id]=event;self._streams[event.stream_id].append(event);self._heads[event.stream_id]=event.source_sequence
            self.watermarks.observe(manifest,event,late)
            if record:self.watermarks.add_late(record)
        disp=AppendDisposition.QUARANTINED if quarantined and not committed else (AppendDisposition.IDEMPOTENT if idem and not committed and not quarantined else AppendDisposition.COMMITTED)
        return AppendResult(batch.batch_id,disp,tuple(committed),tuple(idem),tuple(quarantined),(),self._heads[batch.stream_id],self.journal_root())
    def all_events(self):return tuple(self._events[k] for k in sorted(self._events))
    def stream_events(self,stream_id):return tuple(sorted(self._streams[stream_id],key=lambda e:canonical_event_key(e,self.registry.get(e.stream_id,e.stream_version).source_priority)))
    def visible(self,twin_id,known_as_of,event_as_of=None):
        from .canonical import parse_time
        out=[]
        for e in self._events.values():
            if e.twin_id!=twin_id or parse_time(e.known_time)>parse_time(known_as_of):continue
            if event_as_of and parse_time(e.event_time)>parse_time(event_as_of):continue
            out.append(e)
        return tuple(sorted(out,key=lambda e:canonical_event_key(e,self.registry.get(e.stream_id,e.stream_version).source_priority)))
    def effective(self,twin_id,known_as_of,event_as_of=None):
        from dataclasses import replace
        events=list(self.visible(twin_id,known_as_of,event_as_of));corrections=[e for e in events if e.event_kind==EventKind.CORRECTION]
        base={e.event_id:e for e in events if e.event_kind!=EventKind.CORRECTION}
        for c in corrections:
            if c.correction_of in base:
                target=base[c.correction_of];payload=dict(c.payload['replacement_payload']);base[c.correction_of]=replace(target,payload=payload,payload_hash=content_hash(payload),known_time=c.known_time,tags=tuple(sorted(set(target.tags+('corrected',)))))
        return tuple(sorted(base.values(),key=lambda e:canonical_event_key(e,self.registry.get(e.stream_id,e.stream_version).source_priority)))
    def journal_root(self):return merkle_root(e.envelope_hash for e in self._events.values())
    def head(self,stream_id):return self._heads[stream_id]
    def quarantined(self):return tuple(self._quarantine)
