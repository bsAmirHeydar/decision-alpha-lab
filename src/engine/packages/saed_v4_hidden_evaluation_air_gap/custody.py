from __future__ import annotations
from .canonical import content_hash,stable_id
from .errors import IntegrityError

def verify(manifest,fixture):
    clean={k:v for k,v in fixture.items() if k!="future_suffix_records"}
    observed=content_hash(clean)
    if observed!=manifest["plaintext_commitment_hash"]: raise IntegrityError("protected plaintext commitment mismatch")
    if fixture["schema_hash"]!=manifest["schema_hash"]: raise IntegrityError("protected schema hash mismatch")
    body={"phase":"SAED_V4_29","dataset_id":manifest["dataset_id"],"dataset_version":manifest["dataset_version"],"plaintext_commitment_hash":manifest["plaintext_commitment_hash"],"encrypted_blob_hash":manifest["encrypted_blob_hash"],"schema_hash":manifest["schema_hash"],"row_count":manifest["row_count"],"feature_count":manifest["feature_count"],"custodian_count":len(manifest["custodian_ids"]),"threshold":manifest["threshold"],"storage_zone":manifest["storage_zone"],"synthetic_fixture":True,"researcher_read_access":False,"evaluator_read_access":True,"commitment_verified":True,"key_shares_reconstructed_in_reference":False,"external_hsm_attestation":False,"immutable":True}
    body["custody_receipt_id"]=stable_id("v429_custody",body); body["custody_receipt_hash"]=content_hash(body); return body

def ledger(manifest,receipt):
    from .chain import build_chain,verify_chain
    records=[{"event":"custody_manifest_registered","actor_id":"custodian_quorum","dataset_id":manifest["dataset_id"],"commitment_hash":manifest["plaintext_commitment_hash"],"plaintext_access":False},{"event":"custody_commitment_verified","actor_id":"sealed_evaluator","dataset_id":manifest["dataset_id"],"commitment_hash":receipt["custody_receipt_hash"],"plaintext_access":True},{"event":"custody_zone_resealed","actor_id":"custodian_quorum","dataset_id":manifest["dataset_id"],"commitment_hash":manifest["encrypted_blob_hash"],"plaintext_access":False}]
    entries=build_chain(records,"v4_29_custody"); return {"phase":"SAED_V4_29","entries":entries,"entry_count":len(entries),"chain_verification":verify_chain(entries,"v4_29_custody"),"researcher_plaintext_access_events":0,"ledger_hash":content_hash(entries)}
