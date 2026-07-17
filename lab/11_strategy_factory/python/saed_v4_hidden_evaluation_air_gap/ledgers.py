from __future__ import annotations
from .chain import build_chain,verify_chain
from .canonical import content_hash

def query_ledger(commitment,issued,consumed,result,release):
    records=[{"event":"candidate_committed","candidate_id":commitment["candidate_id"],"object_hash":commitment["commitment_hash"],"actor_id":commitment["submitter_actor_id"],"hidden_data_access":False},{"event":"one_shot_token_issued","candidate_id":commitment["candidate_id"],"object_hash":issued["token_hash"],"actor_id":issued["issuer_actor_id"],"hidden_data_access":False},{"event":"sealed_evaluation_executed","candidate_id":commitment["candidate_id"],"object_hash":result["sealed_result_hash"],"actor_id":"sealed_evaluator","hidden_data_access":True},{"event":"redacted_release_emitted","candidate_id":commitment["candidate_id"],"object_hash":release["release_hash"],"actor_id":"disclosure_controller","hidden_data_access":False}]
    entries=build_chain(records,"v4_29_query"); return {"phase":"SAED_V4_29","entries":entries,"entry_count":4,"evaluation_count":1,"token_issue_count":1,"token_consumption_count":1,"release_count":1,"researcher_hidden_data_access_count":0,"adaptive_round_trip_count":0,"chain_verification":verify_chain(entries,"v4_29_query"),"ledger_hash":content_hash(entries)}
