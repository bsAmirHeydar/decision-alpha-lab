from __future__ import annotations
from .canonical import content_hash
from .errors import DisclosureError

def release(result,policy):
    precision=policy["metric_precision"]
    metrics={k:round(float(v),precision) for k,v in result["aggregate_metrics"].items()}
    baseline={"candidate_balanced_accuracy":round(result["aggregate_metrics"]["balanced_accuracy"],precision),"baseline_balanced_accuracy":round(result["baseline_metrics"]["balanced_accuracy"],precision),"delta":round(result["aggregate_metrics"]["delta_balanced_accuracy_vs_baseline"],precision)}
    out={"evaluation_id":result["evaluation_id"],"candidate_id":result["candidate_id"],"dataset_commitment_hash":result["dataset_commitment_hash"],"protocol_id":result["protocol_id"],"decision":result["decision"],"aggregate_metrics":metrics,"baseline_comparison":baseline}
    if set(out)!=(set(policy["allowed_fields"])-{"release_hash"}): raise DisclosureError("release allowlist mismatch")
    serialized=str(out).lower()
    for field in policy["forbidden_fields"]:
        if f"'{field.lower()}'" in serialized: raise DisclosureError("forbidden result field")
    out["release_hash"]=content_hash(out)
    if set(out)!=set(policy["allowed_fields"]): raise DisclosureError("release shape mismatch")
    return out
