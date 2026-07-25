from __future__ import annotations
from .canonical import content_hash, stable_id, merkle_root
from .errors import IntegrityError

def build_integrity_receipt(named_artifacts:dict[str,dict])->dict:
    entries=[]
    for name,obj in sorted(named_artifacts.items()):
        entries.append({"name":name,"content_hash":content_hash(obj),"declared_identity":next((v for k,v in obj.items() if k.endswith('_id')),None),"declared_hash":next((v for k,v in obj.items() if k.endswith('_hash')),None)})
    payload={"phase":"SAED_V4_11","entries":entries,"entry_count":len(entries),"merkle_root":merkle_root([x['content_hash'] for x in entries]),"complete":True,"authority":"reference_synthetic_only"}
    payload['receipt_id']=stable_id('v411integrity',payload);payload['receipt_hash']=content_hash(payload);return payload

def verify_integrity_receipt(receipt:dict,named_artifacts:dict[str,dict])->None:
    rebuilt=build_integrity_receipt(named_artifacts)
    for key in ('entry_count','merkle_root'):
        if rebuilt[key]!=receipt.get(key): raise IntegrityError(f'integrity receipt {key} mismatch')
