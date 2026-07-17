from __future__ import annotations
from .canonical import content_hash,stable_id
from .errors import TokenError

def issue(commitment,custody_receipt,issued_at,expires_at):
    body={"phase":"SAED_V4_29","candidate_id":commitment["candidate_id"],"candidate_commitment_hash":commitment["commitment_hash"],"dataset_commitment_hash":custody_receipt["plaintext_commitment_hash"],"protocol_hash":commitment["protocol_hash"],"issued_at":issued_at,"expires_at":expires_at,"maximum_uses":1,"used_count":0,"revoked":False,"issuer_actor_id":"custodian_quorum","bound":True,"research_only":True}
    body["token_id"]=stable_id("v429_one_shot",body); body["token_hash"]=content_hash(body); return body

def consume(token,commitment,custody_receipt,consumed_at):
    if token["revoked"] or token["maximum_uses"]!=1 or token["used_count"]!=0: raise TokenError("one-shot token unavailable")
    if token["candidate_commitment_hash"]!=commitment["commitment_hash"] or token["dataset_commitment_hash"]!=custody_receipt["plaintext_commitment_hash"] or token["protocol_hash"]!=commitment["protocol_hash"]: raise TokenError("token binding mismatch")
    out=dict(token); out["used_count"]=1; out["consumed_at"]=consumed_at; out["consumption_receipt_hash"]=content_hash({"token_hash":token["token_hash"],"commitment_hash":commitment["commitment_hash"],"dataset_hash":custody_receipt["plaintext_commitment_hash"],"consumed_at":consumed_at}); return out

def ledger(issued,consumed):
    from .chain import build_chain,verify_chain
    records=[{"event":"token_issued","token_id":issued["token_id"],"token_hash":issued["token_hash"],"use_count":0,"actor_id":issued["issuer_actor_id"]},{"event":"token_consumed","token_id":consumed["token_id"],"token_hash":consumed["token_hash"],"use_count":1,"actor_id":"sealed_evaluator"}]
    entries=build_chain(records,"v4_29_token"); return {"phase":"SAED_V4_29","entries":entries,"entry_count":2,"chain_verification":verify_chain(entries,"v4_29_token"),"reuse_attempts":0,"ledger_hash":content_hash(entries)}
