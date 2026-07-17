from __future__ import annotations
from copy import deepcopy
from .contracts import require_exact,require_unique
from .errors import FederationError
from .canonical import content_hash,seal
from .privacy import clip

def local_manifests(items:list[dict],registry:dict,cutoff_time:str)->dict:
    require_unique(items,"manifest_id","local manifests"); by={x["cell_id"]:x for x in items}; records=[]
    for c in registry["cells"]:
        m=by.get(c["cell_id"])
        if not m: raise FederationError("missing local manifest")
        require_exact(m,["manifest_id","cell_id","dataset_hash","schema_hash","record_count","known_time","latest_event_time","contains_raw_rows","synthetic_fixture"])
        if m["contains_raw_rows"] or m["synthetic_fixture"] is not True: raise FederationError("manifest boundary violated")
        if m["known_time"]>cutoff_time or m["latest_event_time"]>cutoff_time: raise FederationError("future data in local manifest")
        records.append(deepcopy(m))
    return seal({"phase":"SAED_V4_33","manifests":sorted(records,key=lambda x:x["cell_id"]),"raw_rows_exported":False,"all_known_by_cutoff":True,"research_only":True},"v433_local_manifests","registry_id","registry_hash")

def train_receipts(updates:list[dict],registry:dict,study:dict,privacy:dict)->tuple[dict,dict,dict[str,list[float]]]:
    require_unique(updates,"update_id","updates"); active={c["cell_id"] for c in registry["cells"]}; receipts=[]; clip_events=[]; vectors={}
    for u in sorted(updates,key=lambda x:x["cell_id"]):
        require_exact(u,["update_id","cell_id","round_id","known_time","sample_count","vector","local_loss_before","local_loss_after","synthetic_fixture"])
        if u["cell_id"] not in active or u["round_id"]!="ROUND-001" or u["synthetic_fixture"] is not True: raise FederationError("local update invalid")
        if u["known_time"]>study["cutoff_time"]: continue
        if len(u["vector"])!=len(study["initial_model"]): raise FederationError("update dimension mismatch")
        clipped,raw_norm,was_clipped=clip(u["vector"],privacy["clip_norm"]); vectors[u["cell_id"]]=clipped
        digest=content_hash({"cell_id":u["cell_id"],"round_id":u["round_id"],"vector":clipped,"sample_count":u["sample_count"]})
        receipts.append({"update_id":u["update_id"],"cell_id":u["cell_id"],"round_id":u["round_id"],"known_time":u["known_time"],"sample_count":u["sample_count"],"update_digest":digest,"dimension":len(clipped),"raw_norm":raw_norm,"clipped":was_clipped,"local_loss_before":u["local_loss_before"],"local_loss_after":u["local_loss_after"],"raw_vector_exported":False,"synthetic_fixture":True})
        clip_events.append({"cell_id":u["cell_id"],"round_id":u["round_id"],"raw_norm":raw_norm,"clip_norm":privacy["clip_norm"],"clipped":was_clipped,"update_digest":digest})
    receipt=seal({"phase":"SAED_V4_33","study_id":study["study_id"],"receipts":receipts,"receipt_count":len(receipts),"raw_vectors_exported":False,"research_only":True},"v433_local_receipts","registry_id","registry_hash")
    clipping=seal({"phase":"SAED_V4_33","events":clip_events,"event_count":len(clip_events),"clip_norm":privacy["clip_norm"],"all_updates_accounted":len(clip_events)==len(receipts),"research_only":True},"v433_clipping","ledger_id","ledger_hash")
    return receipt,clipping,vectors
