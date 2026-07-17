from __future__ import annotations
from .canonical import content_hash,merkle_root,seal

def bundle(items:dict)->dict:
 entries=[]
 for name,value in sorted(items.items()):entries.append({"name":name,"artifact_hash":content_hash(value),"evidence_class":"INTERNAL_REFERENCE" if name not in {"external_evidence_matrix","broker_qualification_matrix"} else "MIXED_EXTERNAL_STATUS","production_evidence":False})
 return seal({"phase":"SAED_V4_39","evidence_items":entries,"evidence_count":len(entries),"evidence_merkle_root":merkle_root([x["artifact_hash"] for x in entries]),"actual_micro_live_evidence_attached":False,"research_only":True,"production_authorized":False},"v439_evidence","evidence_bundle_id","evidence_bundle_hash")
