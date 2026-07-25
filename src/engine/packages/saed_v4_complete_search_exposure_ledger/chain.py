from __future__ import annotations
from typing import Any, Iterable
from .canonical import content_hash
from .errors import IntegrityError
GENESIS="0"*64

def build_chain(raw_entries: Iterable[dict[str,Any]], chain_name:str)->list[dict[str,Any]]:
    out=[]; prev=GENESIS
    for seq, raw in enumerate(raw_entries,1):
        payload={"chain":chain_name,"sequence":seq,"previous_hash":prev,**dict(raw)}
        payload["entry_hash"]=content_hash(payload)
        out.append(payload); prev=payload["entry_hash"]
    return out

def verify_chain(entries:list[dict[str,Any]], chain_name:str)->dict[str,Any]:
    prev=GENESIS
    for seq, entry in enumerate(entries,1):
        if entry.get("chain")!=chain_name or entry.get("sequence")!=seq or entry.get("previous_hash")!=prev:
            raise IntegrityError(f"{chain_name} continuity failure at {seq}")
        copy=dict(entry); observed=copy.pop("entry_hash",None)
        expected=content_hash(copy)
        if observed!=expected: raise IntegrityError(f"{chain_name} hash failure at {seq}")
        prev=observed
    return {"chain":chain_name,"entry_count":len(entries),"genesis_hash":GENESIS,"head_hash":prev,"verified":True}
