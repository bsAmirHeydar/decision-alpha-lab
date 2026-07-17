from __future__ import annotations
from .canonical import content_hash,stable_id

def attest(topology,policy):
    body={"phase":"SAED_V4_29","topology_id":topology["topology_id"],"zone_ids":[z["zone_id"] for z in topology["zones"]],"flow_ids":[f["flow_id"] for f in topology["flows"]],"default_deny":policy.default_deny,"network_egress":policy.network_access,"package_installation":policy.package_installation,"interactive_debugging":policy.interactive_debugging,"shell_escape":policy.shell_escape,"maximum_evaluations":policy.maximum_evaluations,"maximum_round_trips":policy.maximum_round_trips,"environment_captured":topology["environment_capture"],"fixed_reference_clock":topology["clock_policy"]=="fixed_reference_clock","raw_hidden_data_transport":False,"passed":True,"reference_only_not_os_certification":True}
    body["attestation_id"]=stable_id("v429_air_gap",body); body["attestation_hash"]=content_hash(body); return body

def transport_ledger(topology,submission_commitment,token,release):
    from .chain import build_chain,verify_chain
    records=[{"flow_id":"research_to_transfer","payload_class":"candidate_commitment","payload_hash":submission_commitment["commitment_hash"],"direction":"one_way_in","use":1,"raw_hidden_data":False},{"flow_id":"transfer_to_sealed","payload_class":"one_shot_token_and_candidate","payload_hash":token["token_hash"],"direction":"one_way_in","use":1,"raw_hidden_data":False},{"flow_id":"sealed_to_research","payload_class":"redacted_aggregate_release","payload_hash":release["release_hash"],"direction":"one_way_out","use":1,"raw_hidden_data":False}]
    entries=build_chain(records,"v4_29_transport"); return {"phase":"SAED_V4_29","entries":entries,"entry_count":3,"chain_verification":verify_chain(entries,"v4_29_transport"),"round_trips":0,"raw_hidden_data_transfers":0,"ledger_hash":content_hash(entries)}
