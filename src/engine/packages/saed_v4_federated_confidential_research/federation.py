from __future__ import annotations
from copy import deepcopy
from .contracts import require_exact,require_list,require_unique,require_sorted_unique_strings,require_positive_int
from .errors import FederationError
from .canonical import content_hash,seal

def freeze_constitution(value:dict)->dict:
    require_exact(value,["constitution_id","version","clauses","research_only","raw_data_export_allowed","central_raw_data_access_allowed"])
    if value["research_only"] is not True or value["raw_data_export_allowed"] or value["central_raw_data_access_allowed"]: raise FederationError("constitution must deny raw-data export and central raw access")
    clauses=require_list(value["clauses"],"clauses",8); require_unique(clauses,"clause_id","clauses")
    for c in clauses:
        require_exact(c,["clause_id","priority","requirement","failure_action"])
        require_positive_int(c["priority"],"priority")
    out=deepcopy(value); out["clauses"]=sorted(clauses,key=lambda x:(x["priority"],x["clause_id"])); out["constitution_hash"]=content_hash(out); return out

def freeze_cells(cells:list[dict])->dict:
    cells=require_list(cells,"cells",3); require_unique(cells,"cell_id","cells")
    out=[]
    for c in cells:
        require_exact(c,["cell_id","jurisdiction","residency_zone","operator_id","identity_fingerprint","status","allowed_protocols","independence_group"])
        if c["status"]!="active": raise FederationError("inactive cell")
        require_sorted_unique_strings(c["allowed_protocols"],"allowed_protocols")
        out.append(deepcopy(c))
    out=sorted(out,key=lambda x:x["cell_id"])
    return seal({"phase":"SAED_V4_33","cells":out,"cell_count":len(out),"cross_cell_raw_data_access":False,"research_only":True},"v433_cell_registry","registry_id","registry_hash")

def attest_cells(registry:dict,attestations:list[dict])->dict:
    require_unique(attestations,"attestation_id","attestations"); by={a["cell_id"]:a for a in attestations}
    records=[]
    for c in registry["cells"]:
        a=by.get(c["cell_id"])
        if not a: raise FederationError("missing attestation")
        require_exact(a,["attestation_id","cell_id","identity_fingerprint","known_time","expires_time","human_approved","synthetic_fixture"])
        if a["identity_fingerprint"]!=c["identity_fingerprint"] or a["human_approved"] is not True or a["synthetic_fixture"] is not True: raise FederationError("attestation mismatch")
        records.append(deepcopy(a))
    return seal({"phase":"SAED_V4_33","attestations":sorted(records,key=lambda x:x["cell_id"]),"all_cells_attested":True,"cryptographic_hardware_attestation":"not_claimed","research_only":True},"v433_cell_attestations","ledger_id","ledger_hash")

def freeze_classifications(classes:list[dict])->dict:
    require_unique(classes,"class_id","classifications"); out=[]
    for x in classes:
        require_exact(x,["class_id","description","export_policy","aggregate_export_allowed","row_level_export_allowed","retention_class"])
        if x["row_level_export_allowed"]: raise FederationError("row-level export forbidden")
        out.append(deepcopy(x))
    return seal({"phase":"SAED_V4_33","classifications":sorted(out,key=lambda x:x["class_id"]),"default_class":"protected_local","research_only":True},"v433_classification","registry_id","registry_hash")

def freeze_residency(policies:list[dict],registry:dict)->dict:
    require_unique(policies,"cell_id","residency policies"); by={x["cell_id"]:x for x in policies}; out=[]
    for c in registry["cells"]:
        p=by.get(c["cell_id"])
        if not p: raise FederationError("missing residency policy")
        require_exact(p,["cell_id","residency_zone","raw_data_must_remain_local","permitted_exports","forbidden_exports","deletion_receipt_required"])
        if p["residency_zone"]!=c["residency_zone"] or p["raw_data_must_remain_local"] is not True: raise FederationError("residency mismatch")
        if "raw_rows" not in p["forbidden_exports"] or "credentials" not in p["forbidden_exports"]: raise FederationError("forbidden export set incomplete")
        out.append(deepcopy(p))
    return seal({"phase":"SAED_V4_33","policies":sorted(out,key=lambda x:x["cell_id"]),"all_raw_data_local":True,"research_only":True},"v433_residency","policy_id","policy_hash")

def freeze_protocols(protocols:list[dict])->dict:
    require_unique(protocols,"protocol_id","protocols"); out=[]
    for p in protocols:
        require_exact(p,["protocol_id","version","purpose","deterministic_reference","real_cryptography_claimed","network_transport_claimed","allowed_message_types"])
        if p["real_cryptography_claimed"] or p["network_transport_claimed"]: raise FederationError("reference phase cannot claim real cryptography or transport")
        require_sorted_unique_strings(p["allowed_message_types"],"allowed_message_types"); out.append(deepcopy(p))
    return seal({"phase":"SAED_V4_33","protocols":sorted(out,key=lambda x:x["protocol_id"]),"closed":True,"research_only":True},"v433_protocols","registry_id","registry_hash")

def freeze_study(spec:dict,registry:dict,protocols:dict)->dict:
    require_exact(spec,["study_id","objective","cutoff_time","round_count","minimum_participants","aggregation_protocol_id","privacy_protocol_id","model_family","feature_schema_hash","initial_model","baseline_id","synthetic_fixture","research_only"])
    if spec["synthetic_fixture"] is not True or spec["research_only"] is not True: raise FederationError("study must be synthetic research")
    if spec["minimum_participants"]<3 or spec["minimum_participants"]>registry["cell_count"]: raise FederationError("minimum participant threshold invalid")
    pids={p["protocol_id"] for p in protocols["protocols"]}
    if spec["aggregation_protocol_id"] not in pids or spec["privacy_protocol_id"] not in pids: raise FederationError("unknown protocol")
    if not isinstance(spec["initial_model"],list) or not spec["initial_model"]: raise FederationError("initial model invalid")
    body=deepcopy(spec); body["participant_cell_ids"]=[c["cell_id"] for c in registry["cells"]]; return seal(body,"v433_study","study_spec_id","study_spec_hash")

def eligibility(registry:dict,attestations:dict,study:dict)->dict:
    attested={a["cell_id"] for a in attestations["attestations"]}; records=[]
    for c in registry["cells"]:
        reasons=[]
        if c["cell_id"] not in attested: reasons.append("missing_attestation")
        if study["aggregation_protocol_id"] not in c["allowed_protocols"]: reasons.append("aggregation_protocol_not_allowed")
        if study["privacy_protocol_id"] not in c["allowed_protocols"]: reasons.append("privacy_protocol_not_allowed")
        records.append({"cell_id":c["cell_id"],"eligible":not reasons,"reasons":reasons})
    eligible=sum(x["eligible"] for x in records)
    return seal({"phase":"SAED_V4_33","study_id":study["study_id"],"records":records,"eligible_count":eligible,"threshold_met":eligible>=study["minimum_participants"],"research_only":True},"v433_eligibility","ledger_id","ledger_hash")
