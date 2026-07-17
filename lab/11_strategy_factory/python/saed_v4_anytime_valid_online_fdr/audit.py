from __future__ import annotations
from collections import defaultdict
from .canonical import content_hash, stable_id

def online_fdr(wealth,rejections,target_fdr):
    truth={e["hypothesis_id"]:(e.get("truth_label") or "unknown") for e in []}
    rejected_ids={x["hypothesis_id"] for x in rejections["entries"]}
    entries=wealth["entries"]
    false=sum(1 for e in entries if e["hypothesis_id"] in rejected_ids and e.get("truth_label")=="null")
    # truth label is attached in service below before audit; defensive default remains zero.
    total=len(rejected_ids); fdp=false/max(1,total)
    family=defaultdict(lambda:{"rejections":0,"false_discoveries":0})
    for e in entries:
        if e["hypothesis_id"] in rejected_ids:
            family[e["family_id"]]["rejections"]+=1
            if e.get("truth_label")=="null": family[e["family_id"]]["false_discoveries"]+=1
    rows=[]
    for fid,x in sorted(family.items()): rows.append({"family_id":fid,**x,"empirical_fdp":x["false_discoveries"]/max(1,x["rejections"])})
    gates={"wealth_nonnegative":wealth["all_wealth_nonnegative"],"alpha_nonnegative":wealth["all_alpha_nonnegative"],"wealth_chain_verified":wealth["chain_verification"]["verified"],"rejection_chain_verified":rejections["chain_verification"]["verified"],"rejection_requires_crossing":rejections["all_thresholds_crossed"],"synthetic_empirical_fdp_within_target":fdp<=target_fdr+1e-15}
    payload={"phase":"SAED_V4_28","target_fdr":target_fdr,"hypothesis_count":len(entries),"rejection_count":total,"false_discovery_count":false,"synthetic_empirical_fdp":fdp,"family_rows":rows,"gates":gates,"passed":all(gates.values()),"statistical_scope":"synthetic_reference_fixture_only","real_world_fdr_guarantee":False}
    payload["audit_id"]=stable_id("online_fdr_audit",payload); payload["audit_hash"]=content_hash(payload); return payload

def challenger_comparison(all_decisions,records_by_family,allocations,target_fdr):
    rows=[]
    for proc,fams in sorted(all_decisions.items()):
        n=sum(len(v) for v in fams.values()); rej=sum(sum(int(d.rejected) for d in v) for v in fams.values()); spent=sum(sum(d.alpha for d in v) for v in fams.values()); minw=min([d.wealth_after for v in fams.values() for d in v] or [0.0])
        rows.append({"procedure":proc,"hypothesis_count":n,"rejection_count":rej,"total_alpha_spent":spent,"minimum_wealth":minw,"nonnegative_wealth":minw>=0,"promotion_authority":False})
    payload={"phase":"SAED_V4_28","rows":rows,"procedure_count":len(rows),"all_procedures_research_only":True,"selection_authority":False,"promotion_authority":False,"target_fdr":target_fdr}
    payload["comparison_id"]=stable_id("online_fdr_challenger_comparison",payload); payload["comparison_hash"]=content_hash(payload); return payload
