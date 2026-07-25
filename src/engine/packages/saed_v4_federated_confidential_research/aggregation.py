from __future__ import annotations
import statistics
from .canonical import content_hash,seal,hash_chain
from .errors import AggregationError

def plan(study:dict,eligible:dict,privacy:dict)->dict:
    if not eligible["threshold_met"]: raise AggregationError("eligibility threshold not met")
    body={"phase":"SAED_V4_33","study_id":study["study_id"],"round_id":"ROUND-001","participant_cell_ids":[r["cell_id"] for r in eligible["records"] if r["eligible"]],"minimum_participants":study["minimum_participants"],"dropout_tolerance":len([r for r in eligible["records"] if r["eligible"]])-study["minimum_participants"],"aggregation_rule":"sample_weighted_clipped_mean_after_robust_screen","privacy_mechanism":privacy["mechanism"],"deterministic_reference":True,"real_secure_multiparty_computation":"not_claimed","network_protocol":"not_claimed","research_only":True}
    return seal(body,"v433_aggregation_plan","plan_id","plan_hash")

def screen(vectors:dict[str,list[float]],receipts:dict)->dict:
    norms={r["cell_id"]:r["raw_norm"] for r in receipts["receipts"]}
    vals=list(norms.values()); med=statistics.median(vals); deviations=[abs(x-med) for x in vals]; mad=statistics.median(deviations) or 1e-12
    records=[]
    for cid in sorted(vectors):
        robust_z=abs(norms[cid]-med)/(1.4826*mad)
        quarantine=robust_z>6.0
        records.append({"cell_id":cid,"raw_norm":norms[cid],"median_norm":round(med,12),"mad":round(mad,12),"robust_z":round(robust_z,12),"quarantined":quarantine,"reason":"norm_outlier" if quarantine else "accepted"})
    return seal({"phase":"SAED_V4_33","records":records,"accepted_cell_ids":[r["cell_id"] for r in records if not r["quarantined"]],"quarantined_cell_ids":[r["cell_id"] for r in records if r["quarantined"]],"real_byzantine_resistance":"not_claimed","research_only":True},"v433_byzantine_screen","report_id","report_hash")

def aggregate(vectors:dict[str,list[float]],receipts:dict,screening:dict,study:dict,plan_doc:dict)->tuple[dict,dict,dict]:
    accepted=screening["accepted_cell_ids"]
    if len(accepted)<study["minimum_participants"]: raise AggregationError("accepted participant threshold not met")
    samples={r["cell_id"]:r["sample_count"] for r in receipts["receipts"]}; total=sum(samples[c] for c in accepted)
    dim=len(study["initial_model"]); avg=[]
    for j in range(dim): avg.append(round(sum(vectors[c][j]*samples[c] for c in accepted)/total,12))
    global_model=[round(study["initial_model"][j]+avg[j],12) for j in range(dim)]
    events=[]
    for cid in sorted(vectors): events.append({"cell_id":cid,"round_id":"ROUND-001","status":"included" if cid in accepted else "quarantined","update_digest":next(r["update_digest"] for r in receipts["receipts"] if r["cell_id"]==cid),"sample_count":samples[cid]})
    transcript=seal({"phase":"SAED_V4_33","study_id":study["study_id"],"round_id":"ROUND-001","events":hash_chain(events,"v433_aggregation_event"),"accepted_cell_ids":accepted,"quarantined_cell_ids":screening["quarantined_cell_ids"],"aggregate_update":avg,"aggregate_digest":content_hash(avg),"participant_threshold_met":True,"raw_individual_vectors_disclosed":False,"deterministic_reference":True,"real_secure_aggregation":"not_claimed","research_only":True},"v433_aggregation_transcript","transcript_id","transcript_hash")
    dropout=seal({"phase":"SAED_V4_33","round_id":"ROUND-001","planned_cell_ids":plan_doc["participant_cell_ids"],"completed_cell_ids":sorted(vectors),"missing_cell_ids":sorted(set(plan_doc["participant_cell_ids"])-set(vectors)),"dropout_count":len(set(plan_doc["participant_cell_ids"])-set(vectors)),"dropout_tolerance":plan_doc["dropout_tolerance"],"recovery_required":False,"threshold_preserved":True,"real_secret_share_recovery":"not_claimed","research_only":True},"v433_dropout","ledger_id","ledger_hash")
    model=seal({"phase":"SAED_V4_33","study_id":study["study_id"],"round_id":"ROUND-001","baseline_id":study["baseline_id"],"initial_model_hash":content_hash(study["initial_model"]),"aggregate_update_hash":content_hash(avg),"global_model":global_model,"global_model_hash":content_hash(global_model),"accepted_cell_count":len(accepted),"sample_count":total,"synthetic_fixture":True,"promotion_eligible":False,"runtime_executable":False,"research_only":True},"v433_global_model","receipt_id","receipt_hash")
    return transcript,dropout,model
