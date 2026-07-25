from __future__ import annotations
from collections import defaultdict
from typing import Any
from .canonical import content_hash, stable_id

def build(families:list[dict[str,Any]], manifests:list[dict[str,Any]], trial_ledger:dict[str,Any], exposure_ledger:dict[str,Any])->dict[str,Any]:
    trial_counts=trial_ledger["family_trial_counts"]
    exposure_by_exp=defaultdict(int)
    for e in exposure_ledger["entries"]:
        if e.get("experiment_id"): exposure_by_exp[e["experiment_id"]]+=1
    exp_by_family=defaultdict(list)
    for m in manifests: exp_by_family[m["family_id"]].append(m)
    rows=[]
    for f in sorted(families,key=lambda x:x["family_id"]):
        exps=exp_by_family.get(f["family_id"],[])
        exposures=sum(exposure_by_exp[m["experiment_id"]] for m in exps)
        rows.append({"family_id":f["family_id"],"hypothesis_family":f["hypothesis_family"],"mode":f["mode"],"parameter_space_hash":f["parameter_space_hash"],"experiment_count":len(exps),"trial_count":int(trial_counts.get(f["family_id"],0)),"exposure_count":exposures,"selection_metric":f["selection_metric"],"frozen_before_search":True,"eligible_for_v4_28_online_fdr":True})
    payload={"phase":"SAED_V4_27","families":rows,"family_count":len(rows),"experiment_count":len(manifests),"trial_count":trial_ledger["observed_trial_count"],"exposure_count":exposure_ledger["event_count"],"complete_materially_related_universe":True,"failed_trials_included":True,"pruned_trials_included":True,"duplicates_included":True,"retries_included":True,"human_exposures_included":True,"agent_exposures_included":True,"selection_risk_ready":True}
    payload["multiplicity_universe_id"]=stable_id("multiplicity_universe",payload); payload["multiplicity_universe_hash"]=content_hash(payload)
    return payload
