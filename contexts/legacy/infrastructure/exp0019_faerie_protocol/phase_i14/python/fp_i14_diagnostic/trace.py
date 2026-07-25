from __future__ import annotations
from .contracts import *
from .canonical import sha256,stable_id
from .constants import MAX_TRACE_EVENTS,ZERO_HASH
from .errors import FPI14Error

class TraceLedger:
    def __init__(self,manifest:ProductManifest,fixture_id:str):
        self.manifest=manifest;self.fixture_id=fixture_id;self.events=[];self.event_hashes={};self.chain_hash=ZERO_HASH;self.duplicates=0
    def append(self,event:TraceEvent):
        if event.product!=self.manifest.product: raise FPI14Error("FP_DIAG_PRODUCT_MISMATCH","event product differs from manifest")
        if event.config_hash!=self.manifest.config_hash: raise FPI14Error("FP_DIAG_CONFIG_MISMATCH","event config differs from manifest")
        eid=event.computed_event_id;sem=event.semantic_hash
        prior=self.event_hashes.get(eid)
        if prior:
            if prior!=sem: raise FPI14Error("FP_DIAG_DUPLICATE_COLLISION","duplicate event id has different semantic hash")
            self.duplicates+=1;return TraceDisposition.DUPLICATE_IGNORED
        if len(self.events)>=MAX_TRACE_EVENTS: raise FPI14Error("FP_DIAG_TRACE_TOO_LARGE","trace event limit exceeded")
        if self.events and event.sequence<=self.events[-1].sequence: raise FPI14Error("FP_DIAG_SEQUENCE_REGRESSION","sequence must increase")
        self.event_hashes[eid]=sem;self.events.append(event)
        self.chain_hash=sha256({"prior":self.chain_hash,"sequence":event.sequence,"semantic_hash":sem})
        return TraceDisposition.APPLIED
    def inventory(self):
        semantic_ids=tuple(e.semantic_id for e in self.events)
        hashes=tuple((e.computed_event_id,e.semantic_hash) for e in self.events)
        signal_ids=tuple(e.semantic_id for e in self.events if e.event_type in (TraceEventType.SIGNAL,TraceEventType.CONFIRMATION))
        ww=tuple(e.semantic_id for e in self.events if e.event_type==TraceEventType.WW_CONTEXT)
        quota=tuple(e.semantic_id for e in self.events if e.event_type==TraceEventType.QUOTA and e.state in ("QUOTA_WINNER","RESERVED","FINAL"))
        buffers=tuple((e.buffer_index,e.numeric_value) for e in self.events if e.event_type==TraceEventType.BUFFER)
        visuals=tuple(e.semantic_id for e in self.events if e.event_type==TraceEventType.VISUAL)
        health=tuple(e.state for e in self.events if e.event_type==TraceEventType.HEALTH)
        body={"event_count":len(self.events),"semantic_ids":semantic_ids,"hashes":hashes,"signals":signal_ids,"ww":ww,"quota":quota,"buffers":buffers,"visuals":visuals,"health":health,"chain":self.chain_hash}
        return TraceInventory(len(self.events),semantic_ids,hashes,signal_ids,ww,quota,buffers,visuals,health,self.chain_hash,sha256(body))
    def run(self):
        inv=self.inventory();rid=stable_id("FPDRUN",{"fixture":self.fixture_id,"product":self.manifest.product.value,"manifest":self.manifest.semantic_manifest_hash,"inventory":inv.inventory_hash})
        return TraceRun(rid,self.fixture_id,self.manifest.product,self.manifest,tuple(self.events),inv,self.duplicates,sha256({"run_id":rid,"inventory":inv.inventory_hash,"manifest":self.manifest.semantic_manifest_hash}))

def build_run(manifest,fixture_id,events):
    ledger=TraceLedger(manifest,fixture_id)
    for e in events: ledger.append(e)
    return ledger.run()
