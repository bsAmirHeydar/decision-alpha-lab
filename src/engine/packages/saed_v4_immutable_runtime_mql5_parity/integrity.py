from __future__ import annotations
from copy import deepcopy
from .contracts import exact,sha256
from .errors import IntegrityError
from .canonical import content_hash,merkle_root,seal

def build_file_manifest(files:list[dict],bundle_hash:str)->dict:
 seen=set(); out=[]
 for f in files:
  exact(f,["path","role","content_hash","size_bytes","executable","research_only"]); sha256(f["content_hash"],"content_hash")
  if f["path"] in seen:raise IntegrityError("duplicate path")
  if f["research_only"] is not True:raise IntegrityError("research-only file required")
  seen.add(f["path"]); out.append(deepcopy(f))
 out=sorted(out,key=lambda x:x["path"]); root=merkle_root([x["content_hash"] for x in out])
 return seal({"phase":"SAED_V4_38","bundle_hash":bundle_hash,"files":out,"file_count":len(out),"file_merkle_root":root,"research_only":True},"v438_file_manifest","manifest_id","manifest_hash")
def verify_file_manifest(manifest:dict)->bool:return manifest["file_merkle_root"]==merkle_root([x["content_hash"] for x in manifest["files"]])
def synthetic_signature(payload_hash:str,key_id:str)->dict:
 # Evidence envelope only; not a production signature or key-custody claim.
 return seal({"phase":"SAED_V4_38","scheme":"SYNTHETIC_SHA256_ENVELOPE","key_id":key_id,"payload_hash":payload_hash,"signature":content_hash({"key_id":key_id,"payload_hash":payload_hash,"domain":"SAED_V4_38_RESEARCH"}),"production_signature":False,"research_only":True},"v438_signature","signature_id","signature_hash")
def verify_synthetic_signature(sig:dict)->bool:return sig["signature"]==content_hash({"key_id":sig["key_id"],"payload_hash":sig["payload_hash"],"domain":"SAED_V4_38_RESEARCH"}) and sig["production_signature"] is False
