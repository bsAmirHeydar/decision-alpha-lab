from __future__ import annotations
from .canonical import seal,content_hash,merkle_root
def build_evidence(parts:dict)->dict:
 leaves=[]
 for name,obj in sorted(parts.items()):leaves.append({"name":name,"hash":content_hash(obj),"evidence_role":"SYNTHETIC_REFERENCE","external":False})
 return seal({"phase":"SAED_V4_41","leaves":leaves,"leaf_count":len(leaves),"evidence_merkle_root":merkle_root([x["hash"] for x in leaves]),"actual_external_surveillance_evidence_complete":False,"actual_retirement_drill_complete":False,"actual_mql5_route_revocation_verified":False,"actual_broker_reconciliation_verified":False,"synthetic_reference_complete":True,"research_only":True},"v441_evidence","evidence_bundle_id","evidence_bundle_hash")
