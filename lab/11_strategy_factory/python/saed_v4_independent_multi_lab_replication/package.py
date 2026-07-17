from __future__ import annotations
from .canonical import content_hash,stable_id
from .contracts import require_exact

def build_package_identity(manifest:dict,upstream:dict,protocol:dict)->dict:
    require_exact(manifest,["candidate_id","candidate_commitment_hash","dataset_commitment_hash","sealed_result_hash","disclosure_hash","preprocessing_contract_hash","feature_contract_hash","evaluation_entrypoint_hash","payload_commitment_hash","research_only"],name="replication_package_manifest")
    body={"phase":"SAED_V4_30","candidate_id":manifest["candidate_id"],"candidate_commitment_hash":manifest["candidate_commitment_hash"],"dataset_commitment_hash":manifest["dataset_commitment_hash"],"sealed_result_hash":manifest["sealed_result_hash"],"disclosure_hash":manifest["disclosure_hash"],"preprocessing_contract_hash":manifest["preprocessing_contract_hash"],"feature_contract_hash":manifest["feature_contract_hash"],"evaluation_entrypoint_hash":manifest["evaluation_entrypoint_hash"],"payload_commitment_hash":manifest["payload_commitment_hash"],"upstream_certificate_hash":upstream["certificate_hash"],"upstream_handoff_hash":upstream["handoff_hash"],"protocol_id":protocol["protocol_id"],"protocol_hash":protocol["protocol_hash"],"blinded":True,"raw_protected_rows_included":False,"hidden_labels_included":False,"custody_key_shares_included":False,"research_only":True}
    body["package_id"]=stable_id("v430_package",body); body["package_hash"]=content_hash(body)
    return body
