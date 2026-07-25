from __future__ import annotations
import copy
from typing import Any
from .canonical import content_hash, stable_id
from .contracts import AttributionContract, FaithfulnessContract
from .model import forward
from .numerics import cosine, mean, pearson, rank_correlation

def faithfulness(records, attribution_bundle, contract:FaithfulnessContract):
    sums=[]; score_deltas=[]; deletion=[]
    for r,row in zip(records,attribution_bundle["records"]):
        attrs=[x["integrated_gradient"] for x in row["feature_attributions"]]; sums.append(sum(attrs)); score_deltas.append(row["score"]-row["baseline_score"])
        order=sorted(range(len(attrs)),key=lambda i:(-abs(attrs[i]),i)); x=list(r["feature_values"]); base=row["score"]
        for i in order[:2]: x[i]=0.0
        deletion.append(base-forward(r,features=x)["score"])
    corr=pearson(sums,score_deltas); drop=mean(deletion)
    payload={"phase":"SAED_V4_26","attribution_score_correlation":corr,"mean_top_two_deletion_drop":drop,"minimum_correlation":contract.minimum_attribution_score_correlation,"minimum_deletion_drop":contract.minimum_deletion_drop,"reference_gate_passed":corr>=contract.minimum_attribution_score_correlation and drop>=contract.minimum_deletion_drop,"interpretability_is_not_proof":True}
    payload["faithfulness_report_id"]=stable_id("faithfulness",payload); payload["faithfulness_report_hash"]=content_hash(payload)
    return payload

def sanity(records, attribution_bundle, attribution_contract:AttributionContract, faithfulness_contract:FaithfulnessContract):
    from .attribution import integrated_gradients
    correlations=[]
    for r,row in zip(records,attribution_bundle["records"]):
        randomized=dict(r); randomized["feature_weights"]=list(reversed([-x for x in r["feature_weights"]]))
        original=[x["integrated_gradient"] for x in row["feature_attributions"]]; challenger=integrated_gradients(randomized,attribution_contract)
        correlations.append(rank_correlation(original,challenger))
    rc=mean(correlations)
    payload={"phase":"SAED_V4_26","parameter_randomization_mean_rank_correlation":rc,"ceiling":faithfulness_contract.randomization_rank_correlation_ceiling,"label_randomization_queries":0,"reference_gate_passed":rc<=faithfulness_contract.randomization_rank_correlation_ceiling,"sanity_method":"frozen_parameter_sign_reverse_and_permutation"}
    payload["sanity_report_id"]=stable_id("sanity_check",payload); payload["sanity_report_hash"]=content_hash(payload)
    return payload

def stability(records, attribution_bundle, attribution_contract:AttributionContract, faithfulness_contract:FaithfulnessContract):
    from .attribution import integrated_gradients
    scores=[]
    for index,(r,row) in enumerate(zip(records,attribution_bundle["records"])):
        perturbed=dict(r); perturbed["feature_values"]=[x+(0.005 if (index+j)%2==0 else -0.005) for j,x in enumerate(r["feature_values"])]
        original=[x["integrated_gradient"] for x in row["feature_attributions"]]; challenger=integrated_gradients(perturbed,attribution_contract); scores.append(cosine(original,challenger))
    value=mean(scores)
    payload={"phase":"SAED_V4_26","mean_attribution_cosine":value,"floor":faithfulness_contract.stability_cosine_floor,"perturbation_magnitude":0.005,"reference_gate_passed":value>=faithfulness_contract.stability_cosine_floor,"transport_claim":False}
    payload["stability_report_id"]=stable_id("mechanism_stability",payload); payload["stability_report_hash"]=content_hash(payload)
    return payload

def shortcuts(attribution_bundle, faithfulness_contract:FaithfulnessContract):
    findings=[]
    for row in attribution_bundle["records"]:
        for item in row["feature_attributions"]:
            if any(token in item["feature"] for token in ("proxy","identifier","latency")) and abs(item["normalized_attribution"])>0.35:
                findings.append({"record_id":row["record_id"],"feature":item["feature"],"severity":"high","normalized_attribution":item["normalized_attribution"],"response":"quarantine"})
        if row["concentration_breach"]:
            findings.append({"record_id":row["record_id"],"feature":"aggregate_concentration","severity":"medium","normalized_attribution":row["maximum_feature_concentration"],"response":"manual_review"})
    critical=any(f["severity"]=="critical" for f in findings)
    payload={"phase":"SAED_V4_26","findings":findings,"finding_count":len(findings),"critical_finding_count":sum(f["severity"]=="critical" for f in findings),"critical_shortcuts_absent":not critical,"reference_gate_passed":not critical if faithfulness_contract.critical_shortcuts_forbidden else True}
    payload["shortcut_audit_id"]=stable_id("shortcut_audit",payload); payload["shortcut_audit_hash"]=content_hash(payload)
    return payload

def failure_catalogue(*reports):
    entries=[]
    for report in reports:
        if report.get("reference_gate_passed") is False:
            entries.append({"source_id":next((v for k,v in report.items() if k.endswith("_id")),"unknown"),"severity":"critical","failure_class":"reference_gate_failure","response":"reject","reproducible":True})
    payload={"phase":"SAED_V4_26","entries":entries,"entry_count":len(entries),"critical_count":sum(e["severity"]=="critical" for e in entries),"fail_closed":True}
    payload["failure_catalogue_id"]=stable_id("mechanistic_failure_catalogue",payload); payload["failure_catalogue_hash"]=content_hash(payload)
    return payload
