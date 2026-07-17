from __future__ import annotations
from .canonical import content_hash,stable_id

def commit(candidate,protocol,dataset_commitment_hash):
    body={"phase":"SAED_V4_29","candidate_id":candidate["candidate_id"],"candidate_version":candidate["candidate_version"],"candidate_hash":content_hash(candidate),"model_artifact_hash":candidate["model_artifact_hash"],"preprocessing_hash":candidate["preprocessing_hash"],"feature_contract_hash":candidate["feature_contract_hash"],"source_commit_hash":candidate["source_commit_hash"],"protocol_id":protocol["protocol_id"],"protocol_hash":content_hash(protocol),"dataset_commitment_hash":dataset_commitment_hash,"submitted_at":candidate["submitted_at"],"submitter_actor_id":candidate["submitter_actor_id"],"frozen":True,"hidden_data_touched":False,"adaptive_to_final_evaluation":False,"network_dependency_count":0,"irreversible":True}
    body["commitment_id"]=stable_id("v429_submission",body); body["commitment_hash"]=content_hash(body); return body
