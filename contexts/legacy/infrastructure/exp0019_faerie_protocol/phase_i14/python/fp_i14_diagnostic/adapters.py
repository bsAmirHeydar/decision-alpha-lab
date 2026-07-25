from __future__ import annotations
from dataclasses import dataclass
from .contracts import *
from .canonical import sha256,sorted_unique

@dataclass(frozen=True,slots=True)
class SemanticFact:
    sequence:int; event_time_utc_ms:int; event_type:TraceEventType; semantic_id:str; payload:object; state:str=""; relation:str=""; direction:str=""; owner_session_id:str=""; buffer_index:int=-1; numeric_value:float=0.0; reason_codes:tuple[str,...]=()

def adapt_fact(product:ProductKind,manifest:ProductManifest,fact:SemanticFact):
    return TraceEvent(fact.sequence,fact.event_time_utc_ms,product,fact.event_type,fact.semantic_id,sha256(fact.payload),manifest.config_hash,manifest.source_revision_id,fact.state,fact.relation,fact.direction,fact.owner_session_id,fact.buffer_index,fact.numeric_value,sorted_unique(fact.reason_codes))

def adapt_facts(product,manifest,facts): return tuple(adapt_fact(product,manifest,f) for f in facts)

def clone_for_product(events,product):
    return tuple(TraceEvent(e.sequence,e.event_time_utc_ms,product,e.event_type,e.semantic_id,e.payload_hash,e.config_hash,e.source_revision_id,e.state,e.relation,e.direction,e.owner_session_id,e.buffer_index,e.numeric_value,e.reason_codes,e.event_id) for e in events)
