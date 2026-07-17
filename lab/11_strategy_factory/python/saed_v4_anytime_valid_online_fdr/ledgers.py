from __future__ import annotations
from .chain import build_chain, verify_chain
from .canonical import content_hash, stable_id

def build_alpha_and_wealth(records_by_family,allocations,decisions,procedure,target_fdr):
    rows=[]
    for a in allocations:
        fid=a["family_id"]; recs=records_by_family.get(fid,[]); decs=decisions.get(fid,[])
        for r,d in zip(recs,decs):
            rows.append({"global_hypothesis_sequence":r["sequence"],"hypothesis_id":r["hypothesis_id"],"family_id":fid,"family_local_index":d.local_index,"procedure":procedure,"family_target_fdr":target_fdr*a["weight"],"alpha":d.alpha,"anytime_p_value":r["anytime_p_value"],"e_value":r["e_value"],"eligible":r["eligible"],"rejected":d.rejected,"candidate":d.candidate,"discarded":d.discarded,"wealth_before":d.wealth_before,"alpha_spent":d.alpha,"reward":d.reward,"wealth_after":d.wealth_after,"decision_time":r["decision_time"],"evidence_hash":r["evidence_hash"]})
    rows=sorted(rows,key=lambda x:x["global_hypothesis_sequence"])
    chain=build_chain(rows,"v4_28_online_fdr_wealth")
    verify=verify_chain(chain,"v4_28_online_fdr_wealth")
    payload={"phase":"SAED_V4_28","procedure":procedure,"entries":chain,"entry_count":len(chain),"family_count":len(allocations),"target_fdr":target_fdr,"all_wealth_nonnegative":all(x["wealth_after"]>=0 for x in chain),"all_alpha_nonnegative":all(x["alpha"]>=0 for x in chain),"chain_verification":verify}
    payload["ledger_id"]=stable_id("online_fdr_wealth_ledger",payload); payload["ledger_hash"]=content_hash(payload); return payload

def build_rejections(wealth_ledger):
    rows=[]
    for e in wealth_ledger["entries"]:
        if e["rejected"]:
            rows.append({"hypothesis_id":e["hypothesis_id"],"global_hypothesis_sequence":e["global_hypothesis_sequence"],"family_id":e["family_id"],"family_local_index":e["family_local_index"],"procedure":e["procedure"],"alpha":e["alpha"],"anytime_p_value":e["anytime_p_value"],"e_value":e["e_value"],"decision_time":e["decision_time"],"threshold_crossed":True,"evidence_hash":e["evidence_hash"]})
    chain=build_chain(rows,"v4_28_rejection")
    payload={"phase":"SAED_V4_28","entries":chain,"rejection_count":len(chain),"threshold_crossing_required":True,"all_thresholds_crossed":all(x["anytime_p_value"]<=x["alpha"] for x in chain if x["procedure"]!="e_lond"),"chain_verification":verify_chain(chain,"v4_28_rejection")}
    payload["ledger_id"]=stable_id("online_fdr_rejection_ledger",payload); payload["ledger_hash"]=content_hash(payload); return payload
