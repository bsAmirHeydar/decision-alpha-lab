from __future__ import annotations
from .canonical import content_hash,stable_id

def build(config,manifest,candidate,fixture,outputs):
    output_hashes={k:content_hash(v) for k,v in outputs.items()}
    body={"phase":"SAED_V4_29","config_hash":content_hash(config),"custody_manifest_hash":content_hash(manifest),"candidate_hash":content_hash(candidate),"sealed_fixture_commitment_hash":content_hash({k:v for k,v in fixture.items() if k!="future_suffix_records"}),"output_hashes":output_hashes,"output_bundle_hash":content_hash(output_hashes),"deterministic":True,"future_suffix_invariant":True,"network_access":False,"environment":"python_standard_library_reference","randomness":"frozen_seed_no_sampling","research_only":True}
    body["replay_id"]=stable_id("v429_replay",body); body["replay_hash"]=content_hash(body); return body
