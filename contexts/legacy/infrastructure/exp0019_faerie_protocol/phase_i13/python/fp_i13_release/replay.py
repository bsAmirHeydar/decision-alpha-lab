from __future__ import annotations
from dataclasses import replace
from time import perf_counter_ns
import tracemalloc
from .contracts import *
from .canonical import sha256,stable_id
from .constants import CHECKPOINT_VERSION,DEFAULT_CHUNK_SIZE
from .errors import FPI13Error

class ReplayReducer:
    def __init__(self,fixture:ReplayFixture,instance:InstanceIdentity):
        self.fixture=fixture;self.instance=instance;self.last_sequence=0;self.chain_hash='0'*64
        self.event_hashes={};self.semantic={};self.visual={};self.alerts=set();self.suppressed_alerts=set();self.exports=set();self.health=[];self.duplicates=0;self.object_ops=0
    def apply(self,event:ReplayEvent):
        eid=event.computed_event_id;eh=event.event_hash
        prior=self.event_hashes.get(eid)
        if prior:
            if prior!=eh: raise FPI13Error('FP_REL_EVENT_ID_COLLISION','event id collision')
            self.duplicates+=1;return ReplayDisposition.DUPLICATE_IGNORED
        if event.sequence<=self.last_sequence: raise FPI13Error('FP_REL_SEQUENCE_REGRESSION','nonduplicate sequence regression')
        self.event_hashes[eid]=eh;self.last_sequence=event.sequence
        self.chain_hash=sha256({'prior':self.chain_hash,'sequence':event.sequence,'event_hash':eh})
        if event.event_type in (ReplayEventType.SEMANTIC_UPSERT,ReplayEventType.SEMANTIC_STATUS):
            self.semantic[event.semantic_id]=event.payload_hash
        elif event.event_type==ReplayEventType.VISUAL_FACT:
            oid=stable_id('FPOBJ',{'namespace':self.instance.object_namespace,'semantic_id':event.semantic_id,'kind':event.kind or 'GENERIC'},20)
            if self.visual.get(event.semantic_id)!=oid:self.object_ops+=1
            self.visual[event.semantic_id]=oid
        elif event.event_type==ReplayEventType.ALERT_FACT:
            aid=stable_id('FPALERT',{'semantic_id':event.semantic_id,'kind':event.kind or 'GENERIC','version':'1.0.0'})
            (self.suppressed_alerts if event.is_historical else self.alerts).add(aid)
        elif event.event_type==ReplayEventType.EXPORT_FACT:
            self.exports.add(stable_id('FPEXPORT',{'semantic_id':event.semantic_id,'payload_hash':event.payload_hash,'kind':event.kind or 'GENERIC'}))
        elif event.event_type==ReplayEventType.HEALTH_FACT:
            self.health.append(event.kind or 'READY')
        return ReplayDisposition.APPLIED
    def inventory(self)->ReplayInventory:
        semantic_payloads=tuple(sorted(self.semantic.items()))
        semantic_ids=tuple(k for k,_ in semantic_payloads)
        visual_semantics=tuple(sorted(self.visual))
        visual_objects=tuple(self.visual[k] for k in visual_semantics)
        alerts=tuple(sorted(self.alerts));supp=tuple(sorted(self.suppressed_alerts));exports=tuple(sorted(self.exports));health=tuple(self.health)
        body={'semantic_payloads':semantic_payloads,'visual_semantics':visual_semantics,'visual_objects':visual_objects,'alerts':alerts,'suppressed':supp,'exports':exports,'health':health,'event_chain_hash':self.chain_hash,'last_sequence':self.last_sequence}
        return ReplayInventory(semantic_ids,semantic_payloads,visual_semantics,visual_objects,alerts,supp,exports,health,self.chain_hash,self.last_sequence,sha256(body))

def _run(fixture,instance,mode,chart_tf,chunk_size=DEFAULT_CHUNK_SIZE,checkpoint_bytes=0):
    reducer=ReplayReducer(fixture,instance);chunk_count=0;max_chunk=0
    tracemalloc.start();t0=perf_counter_ns()
    if mode==ReplayMode.FULL:
        c0=perf_counter_ns()
        for e in fixture.events: reducer.apply(e)
        max_chunk=perf_counter_ns()-c0;chunk_count=1 if fixture.events else 0;full_scan=1
    else:
        full_scan=0
        for i in range(0,len(fixture.events),chunk_size):
            c0=perf_counter_ns()
            for e in fixture.events[i:i+chunk_size]: reducer.apply(e)
            max_chunk=max(max_chunk,perf_counter_ns()-c0);chunk_count+=1
    elapsed=perf_counter_ns()-t0;_,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
    inv=reducer.inventory();eps=(len(fixture.events)/(elapsed/1e9)) if elapsed else 0.0
    tel_body={'event_count':len(fixture.events),'chunk_count':chunk_count,'full_scan_count':full_scan,'duplicate_count':reducer.duplicates,'elapsed_ns':elapsed,'peak_memory_bytes':peak,'checkpoint_bytes':checkpoint_bytes,'object_count':len(inv.visual_object_ids),'object_ops':reducer.object_ops,'events_per_second':round(eps,6),'max_chunk_ns':max_chunk}
    tel=ReplayTelemetry(**tel_body,telemetry_hash=sha256(tel_body))
    rid=stable_id('FPRUN',{'fixture':fixture.fixture_id,'mode':mode.value,'instance':instance.instance_id,'chart_tf':chart_tf,'inventory':inv.inventory_hash,'telemetry_contract':'1.0.0'})
    body={'run_id':rid,'fixture_id':fixture.fixture_id,'mode':mode.value,'instance_id':instance.instance_id,'chart_tf':chart_tf,'host_tf':fixture.resolved_host_timeframe_minutes,'config_hash':fixture.config_hash,'inventory_hash':inv.inventory_hash}
    return ReplayRun(rid,fixture.fixture_id,mode,instance.instance_id,chart_tf,fixture.resolved_host_timeframe_minutes,fixture.config_hash,inv,tel,sha256(body))

def run_full(fixture,instance,chart_timeframe_minutes=1): return _run(fixture,instance,ReplayMode.FULL,chart_timeframe_minutes)
def run_incremental(fixture,instance,chart_timeframe_minutes=1,chunk_size=DEFAULT_CHUNK_SIZE):
    if chunk_size<1: raise FPI13Error('FP_REL_CHUNK_INVALID','chunk size must be positive')
    return _run(fixture,instance,ReplayMode.INCREMENTAL,chart_timeframe_minutes,chunk_size)
