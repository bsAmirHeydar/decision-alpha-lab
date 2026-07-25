from __future__ import annotations
from copy import deepcopy
from .contracts import require_exact,require_list,require_unique,require_sorted_unique_strings,require_positive_int,require_nonnegative,require_sha256
from .errors import InventoryError
from .canonical import content_hash,seal

def freeze_domains(items:list[dict])->dict:
    items=require_list(items,"domains",3); require_unique(items,"domain_id","domains"); out=[]
    for d in items:
        require_exact(d,["domain_id","jurisdiction","residency_zone","operator_id","independence_group","status","allowed_compute_classes","raw_data_must_remain_local"])
        if d["status"]!="active" or d["raw_data_must_remain_local"] is not True: raise InventoryError("domain unavailable or non-sovereign")
        require_sorted_unique_strings(d["allowed_compute_classes"],"allowed_compute_classes"); out.append(deepcopy(d))
    return seal({"phase":"SAED_V4_34","domains":sorted(out,key=lambda x:x["domain_id"]),"domain_count":len(out),"cross_domain_raw_data_access":False,"research_only":True},"v434_domains","registry_id","registry_hash")

def freeze_nodes(items:list[dict],domains:dict)->dict:
    items=require_list(items,"nodes",4); require_unique(items,"node_id","nodes"); dids={d["domain_id"] for d in domains["domains"]}; out=[]
    for n in items:
        require_exact(n,["node_id","domain_id","compute_class","cpu_cores","gpu_units","memory_gb","scratch_gb","attestation_fingerprint","runtime_image_hash","status","network_zone"])
        if n["domain_id"] not in dids or n["status"]!="ready": raise InventoryError("node domain/status invalid")
        require_positive_int(n["cpu_cores"],"cpu_cores"); require_nonnegative(n["gpu_units"],"gpu_units"); require_nonnegative(n["memory_gb"],"memory_gb"); require_nonnegative(n["scratch_gb"],"scratch_gb"); require_sha256(n["runtime_image_hash"],"runtime_image_hash")
        out.append(deepcopy(n))
    return seal({"phase":"SAED_V4_34","nodes":sorted(out,key=lambda x:x["node_id"]),"node_count":len(out),"all_nodes_ready":True,"research_only":True},"v434_nodes","registry_id","registry_hash")

def attest_nodes(registry:dict,items:list[dict],cutoff_time:str)->dict:
    require_unique(items,"attestation_id","attestations"); by={x["node_id"]:x for x in items}; out=[]
    expected={n["node_id"] for n in registry["nodes"]}
    if set(by)!=expected: raise InventoryError("attestation set must exactly match node registry")
    for n in registry["nodes"]:
        a=by.get(n["node_id"])
        if not a: raise InventoryError("missing node attestation")
        require_exact(a,["attestation_id","node_id","attestation_fingerprint","runtime_image_hash","known_time","expires_time","human_approved","synthetic_fixture"])
        if a["attestation_fingerprint"]!=n["attestation_fingerprint"] or a["runtime_image_hash"]!=n["runtime_image_hash"] or a["known_time"]>cutoff_time or a["human_approved"] is not True or a["synthetic_fixture"] is not True: raise InventoryError("attestation mismatch")
        out.append(deepcopy(a))
    return seal({"phase":"SAED_V4_34","attestations":sorted(out,key=lambda x:x["node_id"]),"all_nodes_attested":True,"hardware_attestation":"not_claimed","research_only":True},"v434_attest","ledger_id","ledger_hash")

def freeze_network(policy:dict,domains:dict)->dict:
    require_exact(policy,["policy_id","default_deny","public_egress_allowed","allowed_routes","forbidden_protocols","cross_domain_payload_classes","max_message_bytes","research_only"])
    if policy["default_deny"] is not True or policy["public_egress_allowed"] or policy["research_only"] is not True: raise InventoryError("network policy must be default-deny and research-only")
    require_unique(policy["allowed_routes"],"route_id","routes"); dids={d["domain_id"] for d in domains["domains"]}
    for r in policy["allowed_routes"]:
        require_exact(r,["route_id","source_domain","target_domain","message_class","encrypted_transport_required","raw_data_allowed"])
        if r["source_domain"] not in dids or r["target_domain"] not in dids or r["raw_data_allowed"] or r["encrypted_transport_required"] is not True: raise InventoryError("invalid route")
    body=deepcopy(policy); body["policy_hash"]=content_hash(body); return body

def freeze_artifacts(items:list[dict],cutoff_time:str)->dict:
    require_unique(items,"artifact_id","artifacts"); out=[]
    for a in items:
        require_exact(a,["artifact_id","artifact_type","content_hash","schema_hash","known_time","immutable","contains_raw_rows","residency_domain","synthetic_fixture"])
        require_sha256(a["content_hash"],"content_hash"); require_sha256(a["schema_hash"],"schema_hash")
        if a["known_time"]>cutoff_time or a["immutable"] is not True or a["contains_raw_rows"] or a["synthetic_fixture"] is not True: raise InventoryError("artifact boundary violated")
        out.append(deepcopy(a))
    return seal({"phase":"SAED_V4_34","artifacts":sorted(out,key=lambda x:x["artifact_id"]),"artifact_count":len(out),"all_immutable":True,"raw_rows_exported":False,"research_only":True},"v434_artifacts","registry_id","registry_hash")
