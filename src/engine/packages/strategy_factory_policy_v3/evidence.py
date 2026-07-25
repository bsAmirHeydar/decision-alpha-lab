from __future__ import annotations
from dataclasses import dataclass,asdict
from typing import Any,Mapping
from .canonical import canonical_sha256
from .errors import PolicyError
@dataclass(frozen=True,slots=True)
class TraceEntry:
    sequence:int; node_id:str; node_kind:str; status:str; payload:Mapping[str,Any]; previous_hash:str; entry_hash:str

def append_trace(entries:list[TraceEntry],node_id:str,node_kind:str,status:str,payload:Mapping[str,Any])->TraceEntry:
    prev=entries[-1].entry_hash if entries else '0'*64
    body={'sequence':len(entries),'node_id':node_id,'node_kind':node_kind,'status':status,'payload':dict(payload),'previous_hash':prev}
    e=TraceEntry(**body,entry_hash=canonical_sha256(body)); entries.append(e); return e

def verify_trace(entries)->bool:
    prev='0'*64
    for i,e in enumerate(entries):
        body={'sequence':i,'node_id':e.node_id,'node_kind':e.node_kind,'status':e.status,'payload':dict(e.payload),'previous_hash':prev}
        if e.sequence!=i or e.previous_hash!=prev or e.entry_hash!=canonical_sha256(body):return False
        prev=e.entry_hash
    return True
