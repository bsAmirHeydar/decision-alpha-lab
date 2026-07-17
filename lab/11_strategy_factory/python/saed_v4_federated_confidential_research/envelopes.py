from __future__ import annotations
from .canonical import content_hash,seal,hash_chain

def build_envelopes(receipts:dict,study:dict)->tuple[dict,dict]:
    env=[]; sig=[]
    for r in receipts["receipts"]:
        commitment=content_hash({"cell_id":r["cell_id"],"round_id":r["round_id"],"update_digest":r["update_digest"],"study_hash":study["study_spec_hash"]})
        e={"envelope_id":"ENV-"+r["cell_id"],"cell_id":r["cell_id"],"round_id":r["round_id"],"message_type":"clipped_update_commitment","payload_digest":r["update_digest"],"commitment":commitment,"schema_hash":study["feature_schema_hash"],"raw_payload_present":False,"real_encryption_claimed":False,"real_signature_claimed":False,"synthetic_fixture":True}
        env.append(e)
        sig.append({"envelope_id":e["envelope_id"],"cell_id":e["cell_id"],"commitment":commitment,"attestation":"deterministic_reference_attestation","verified":True,"cryptographic_signature":"not_claimed"})
    return seal({"phase":"SAED_V4_33","envelopes":env,"count":len(env),"raw_payloads_present":False,"research_only":True},"v433_envelopes","registry_id","registry_hash"), seal({"phase":"SAED_V4_33","events":hash_chain(sig,"v433_signature_event"),"all_verified":True,"real_signature_verification":"not_claimed","research_only":True},"v433_signatures","ledger_id","ledger_hash")
