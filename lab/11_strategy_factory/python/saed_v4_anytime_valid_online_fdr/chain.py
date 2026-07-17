from __future__ import annotations
from .canonical import content_hash
from .errors import IntegrityError
GENESIS="0"*64

def build_chain(entries,chain_name):
    out=[]; prev=GENESIS
    for seq,raw in enumerate(entries,1):
        x={"chain":chain_name,"sequence":seq,"previous_hash":prev,**dict(raw)}; x["entry_hash"]=content_hash(x); out.append(x); prev=x["entry_hash"]
    return out

def verify_chain(entries,chain_name):
    prev=GENESIS
    for seq,e in enumerate(entries,1):
        if e.get("chain")!=chain_name or e.get("sequence")!=seq or e.get("previous_hash")!=prev: raise IntegrityError(f"{chain_name} continuity failure at {seq}")
        x=dict(e); observed=x.pop("entry_hash",None)
        if observed!=content_hash(x): raise IntegrityError(f"{chain_name} hash failure at {seq}")
        prev=observed
    return {"chain":chain_name,"entry_count":len(entries),"genesis_hash":GENESIS,"head_hash":prev,"verified":True}
