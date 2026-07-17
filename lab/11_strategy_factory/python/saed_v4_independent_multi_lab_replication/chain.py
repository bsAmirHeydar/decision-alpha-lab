from __future__ import annotations
from typing import Any,Iterable
from .canonical import content_hash
from .errors import IntegrityError

def build_chain(records:Iterable[dict[str,Any]],domain:str)->list[dict[str,Any]]:
    out=[]; previous="0"*64
    for sequence,record in enumerate(records,1):
        body=dict(record); body.update({"sequence":sequence,"previous_hash":previous,"chain":domain})
        body["entry_hash"]=content_hash(body); previous=body["entry_hash"]; out.append(body)
    return out

def verify_chain(records:list[dict[str,Any]],domain:str)->dict[str,Any]:
    previous="0"*64
    for expected,record in enumerate(records,1):
        if record.get("sequence")!=expected or record.get("previous_hash")!=previous or record.get("chain")!=domain:
            raise IntegrityError(f"{domain} chain linkage failure")
        body=dict(record); observed=body.pop("entry_hash",None)
        if observed!=content_hash(body): raise IntegrityError(f"{domain} chain hash failure")
        previous=observed
    return {"chain":domain,"entry_count":len(records),"head_hash":previous,"verified":True}
