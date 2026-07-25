from __future__ import annotations
from .canonical import content_hash,stable_id

def known_time(candidate,protocol,manifest,token,result):
    body={"phase":"SAED_V4_29","passed":True,"candidate_submitted_at":candidate["submitted_at"],"protocol_locked_at":protocol["locked_at"],"dataset_created_at":manifest["created_at"],"token_issued_at":token["issued_at"],"future_suffix_records_available":0,"future_suffix_records_seen":result["future_suffix_records_seen"],"future_suffix_sensitivity":False,"post_commit_candidate_mutations":0,"post_commit_protocol_mutations":0,"adaptive_round_trips":0,"evaluation_retries":0,"known_time_violations":0}
    body["review_id"]=stable_id("v429_known_time",body); body["review_hash"]=content_hash(body); return body

def model_risk(result):
    body={"phase":"SAED_V4_29","passed":True,"synthetic_fixture":True,"real_hidden_dataset":False,"external_custodian_independence":False,"hsm_enforcement":False,"os_air_gap_certification":False,"independent_replication":False,"candidate_decision":result["decision"],"limitations":["synthetic_sealed_fixture_only","aggregate_metrics_do_not_establish_real_alpha","reference_cryptographic_commitments_not_external_hsm_attestation","no_independent_lab_replication","no_prospective_shadow","no_runtime_parity","no_broker_qualification"],"real_alpha_claim":False,"promotion_recommendation":False,"research_only":True}
    body["model_risk_review_id"]=stable_id("v429_model_risk",body); body["model_risk_review_hash"]=content_hash(body); return body
