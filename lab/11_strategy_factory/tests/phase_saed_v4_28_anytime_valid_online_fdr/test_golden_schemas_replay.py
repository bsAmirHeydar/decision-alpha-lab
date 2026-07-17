import json,pytest
from pathlib import Path
from saed_v4_anytime_valid_online_fdr.canonical import canonical_json,content_hash
ART={
"upstream_receipt":"GOLDEN_UPSTREAM_RECEIPT.JSON","anytime_evidence_registry":"GOLDEN_ANYTIME_EVIDENCE_REGISTRY.JSON","family_allocation":"GOLDEN_FAMILY_ALLOCATION.JSON","wealth_ledger":"GOLDEN_ONLINE_FDR_WEALTH_LEDGER.JSON","rejection_ledger":"GOLDEN_REJECTION_LEDGER.JSON","stopping_rule_audit":"GOLDEN_STOPPING_RULE_AUDIT.JSON","online_fdr_audit":"GOLDEN_ONLINE_FDR_AUDIT.JSON","challenger_comparison":"GOLDEN_CHALLENGER_COMPARISON.JSON","known_time_review":"KNOWN_TIME_LEAKAGE_REVIEW.JSON","security_review":"SECURITY_REVIEW.JSON","model_risk_review":"MODEL_RISK_REVIEW.JSON","authority_boundary":"GOLDEN_AUTHORITY_BOUNDARY.JSON","certificate":"GOLDEN_ANYTIME_VALID_ONLINE_FDR_CERTIFICATE.JSON","handoff":"V4_28_TO_V4_29_HANDOFF.JSON","replay_receipt":"GOLDEN_REPLAY_RECEIPT.JSON"}
def test_golden_exact(outputs,request):
    ar=request.config.rootpath/"lab/11_strategy_factory/artifacts/saed_v4_28"
    for k,n in ART.items(): assert outputs[k]==json.loads((ar/n).read_text(encoding="utf-8")),k
def test_canonical_deterministic(): assert canonical_json({"b":1,"a":2})=='{"a":2,"b":1}'
def test_hash_deterministic(): assert content_hash({"x":1})==content_hash({"x":1})
def test_replay_deterministic(outputs): assert outputs["replay_receipt"]["deterministic"]
def test_replay_no_network(outputs): assert outputs["replay_receipt"]["network_access"] is False
def test_replay_future_invariant(outputs): assert outputs["replay_receipt"]["future_suffix_invariant"]
def test_security_review(outputs):
    x=outputs["security_review"]; assert x["passed"] and not x["network_access"] and not x["broker_connection"] and not x["order_submission"]
def test_model_risk_scope(outputs): assert outputs["model_risk_review"]["real_world_fdr_guarantee"] is False
@pytest.mark.parametrize("name",list(ART.values()))
def test_artifact_exists(request,name): assert (request.config.rootpath/"lab/11_strategy_factory/artifacts/saed_v4_28"/name).is_file()
