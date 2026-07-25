from __future__ import annotations
from .metrics import predict,calculate
from .canonical import content_hash,stable_id

def evaluate(candidate,fixture,protocol,consumed_token,commitment):
    records=fixture["records"]
    labels=[]; scores=[]; preds=[]
    for record in records:
        score,pred=predict(candidate["model_spec"],record["features"]); labels.append(record["hidden_label"]); scores.append(score); preds.append(pred)
    metrics=calculate(labels,scores,preds)
    baseline_pred=1 if sum(labels)/len(labels)>=0.5 else 0
    baseline_preds=[baseline_pred]*len(labels); baseline_scores=[sum(labels)/len(labels)]*len(labels)
    baseline=calculate(labels,baseline_scores,baseline_preds)
    metrics["delta_balanced_accuracy_vs_baseline"]=metrics["balanced_accuracy"]-baseline["balanced_accuracy"]
    rule=protocol["pass_rule"]
    gates={"minimum_balanced_accuracy":metrics["balanced_accuracy"]>=rule["minimum_balanced_accuracy"],"maximum_brier_score":metrics["brier_score"]<=rule["maximum_brier_score"],"minimum_delta_vs_baseline":metrics["delta_balanced_accuracy_vs_baseline"]>=rule["minimum_delta_vs_baseline"]}
    body={"phase":"SAED_V4_29","candidate_id":candidate["candidate_id"],"candidate_commitment_hash":commitment["commitment_hash"],"dataset_id":fixture["dataset_id"],"dataset_commitment_hash":consumed_token["dataset_commitment_hash"],"protocol_id":protocol["protocol_id"],"protocol_hash":commitment["protocol_hash"],"token_id":consumed_token["token_id"],"token_consumption_receipt_hash":consumed_token["consumption_receipt_hash"],"record_count":len(records),"aggregate_metrics":metrics,"baseline_metrics":baseline,"pass_gates":gates,"decision":"pass" if all(gates.values()) else "fail","evaluation_count":1,"future_suffix_records_seen":0,"network_access":False,"adaptive_changes":False,"raw_rows_exported":False,"synthetic_fixture":True,"deterministic":True,"research_only":True}
    body["evaluation_id"]=stable_id("v429_sealed_eval",body); body["sealed_result_hash"]=content_hash(body); return body
