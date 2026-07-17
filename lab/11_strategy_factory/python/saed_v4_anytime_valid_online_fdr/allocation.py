from __future__ import annotations
from collections import defaultdict
from .canonical import content_hash, stable_id

def build(allocations,upstream_universe,target_fdr):
    upstream={x["family_id"]:x for x in upstream_universe["families"]}; rows=[]
    for a in allocations:
        if a["family_id"] not in upstream: raise ValueError("allocation family absent upstream")
        u=upstream[a["family_id"]]
        if a["maximum_hypotheses"]>u["trial_count"]: raise ValueError("allocation maximum exceeds frozen universe")
        rows.append({"family_id":a["family_id"],"weight":a["weight"],"target_fdr":target_fdr*a["weight"],"maximum_hypotheses":a["maximum_hypotheses"],"owner_actor_id":a["owner_actor_id"],"allocation_basis":a["allocation_basis"],"frozen_before_first_test":True,"upstream_trial_count":u["trial_count"],"upstream_exposure_count":u["exposure_count"]})
    payload={"phase":"SAED_V4_28","method":"fixed_predictable_family_weights","rows":rows,"family_count":len(rows),"weight_sum":sum(x["weight"] for x in rows),"target_fdr":target_fdr,"frozen":True,"predictable":True,"retroactive_reallocation":False}
    payload["allocation_id"]=stable_id("family_fdr_allocation",payload); payload["allocation_hash"]=content_hash(payload); return payload

def group(records):
    out=defaultdict(list)
    for r in records: out[r["family_id"]].append(r)
    return {k:sorted(v,key=lambda x:x["sequence"]) for k,v in out.items()}
