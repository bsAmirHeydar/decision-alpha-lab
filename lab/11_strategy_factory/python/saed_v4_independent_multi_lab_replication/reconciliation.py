from __future__ import annotations
from itertools import combinations
from .canonical import content_hash,stable_id

def reconcile(results:dict,protocol:dict)->tuple[dict,dict]:
    records=results["records"]
    semantic_values={r["semantic_output_hash"] for r in records}
    semantic_pairs=[]
    for a,b in combinations(records,2):
        same=a["semantic_output_hash"]==b["semantic_output_hash"]
        semantic_pairs.append({"left_lab_id":a["lab_id"],"right_lab_id":b["lab_id"],"left_hash":a["semantic_output_hash"],"right_hash":b["semantic_output_hash"],"match":same})
    semantic={"phase":"SAED_V4_30","pairs":semantic_pairs,"pair_count":len(semantic_pairs),"unique_semantic_hashes":len(semantic_values),"all_match":len(semantic_values)==1,"research_only":True}
    semantic["reconciliation_id"]=stable_id("v430_semantic_reconciliation",semantic); semantic["reconciliation_hash"]=content_hash(semantic)
    tolerances=protocol["metric_tolerance_policy"]; comparisons=[]; all_within=True
    for a,b in combinations(records,2):
        for metric in protocol["metrics"]:
            mid=metric["metric_id"]; left=float(a["aggregate_metrics"][mid]); right=float(b["aggregate_metrics"][mid]); delta=abs(left-right); tol=float(tolerances[mid]); within=delta<=tol; all_within &= within
            comparisons.append({"left_lab_id":a["lab_id"],"right_lab_id":b["lab_id"],"metric_id":mid,"left_value":left,"right_value":right,"absolute_delta":delta,"tolerance":tol,"within_tolerance":within})
    metrics={"phase":"SAED_V4_30","comparisons":comparisons,"comparison_count":len(comparisons),"all_within_tolerance":all_within,"baseline_preserved":True,"research_only":True}
    metrics["reconciliation_id"]=stable_id("v430_metric_reconciliation",metrics); metrics["reconciliation_hash"]=content_hash(metrics)
    return semantic,metrics
