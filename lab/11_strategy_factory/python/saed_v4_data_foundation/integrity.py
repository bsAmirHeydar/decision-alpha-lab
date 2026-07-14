from __future__ import annotations
from dataclasses import dataclass
from typing import Mapping
from .canonical import content_hash,merkle_root
@dataclass(frozen=True)
class IntegrityReceipt:
    receipt_id:str; object_hash:str; component_root:str; status:str; details:Mapping[str,str]
def build_integrity_receipt(object_hash:str,components:Mapping[str,str])->IntegrityReceipt:
    root=merkle_root(f'{k}:{v}' for k,v in sorted(components.items())); payload={'object_hash':object_hash,'component_root':root,'status':'pass','details':dict(components)}
    return IntegrityReceipt('int_'+content_hash(payload)[:24],object_hash,root,'pass',dict(components))
def verify_integrity_receipt(receipt:IntegrityReceipt)->bool:
    return receipt.component_root==merkle_root(f'{k}:{v}' for k,v in sorted(receipt.details.items())) and receipt.status=='pass'
