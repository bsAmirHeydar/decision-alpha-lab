from __future__ import annotations
from pathlib import Path
from .io import load_json,load_jsonl
from .canonical import digest_object,file_digest
from .constants import CLAIM_CEILING

def verify_package(root:Path)->dict:
    errors=[]
    packages=load_jsonl(root/"registries/treatment_package_registry.jsonl");adapters=load_jsonl(root/"execution_adapter_contracts/execution_adapter_contract_registry.jsonl");blockers=load_jsonl(root/"blockers/treatment_blocker_registry.jsonl");bindings=load_jsonl(root/"bindings/setup_treatment_package_binding_registry.jsonl")
    atoms=sum(x["atom_count"] for x in packages)
    if atoms!=1109:errors.append(f"PACKAGED_ATOM_COUNT:{atoms}")
    if len(adapters)!=483:errors.append(f"ADAPTER_COUNT:{len(adapters)}")
    if len(bindings)!=60:errors.append(f"SETUP_BINDING_COUNT:{len(bindings)}")
    if any(x["submission_capability_default"] or x["live_mode_allowed"] or x["paper_mode_allowed"] for x in adapters):errors.append("ADAPTER_AUTHORITY_NOT_FALSE")
    for x in packages:
        p=load_json(root/x["package_path"])
        if p["package_digest"]!=digest_object(p,"package_digest"):errors.append(f"PACKAGE_DIGEST:{p['treatment_package_id']}")
    m=load_json(root/"output_manifest.json")
    for x in m["files"]:
        p=root/x["path"]
        if not p.is_file() or file_digest(p)!=x["sha256"]:errors.append(f"MANIFEST:{x['path']}")
    h=load_json(root/"handoff/lcm10b_to_lcm10c_handoff.json")
    if h["handoff_digest"]!=digest_object(h,"handoff_digest"):errors.append("HANDOFF_DIGEST")
    a=load_json(root/"reports/acceptance_report.json")
    if not a["acceptance_gate_passed"]:errors.append("ACCEPTANCE_NOT_PASSED")
    return {"passed":not errors,"errors":errors,"treatment_package_count":len(packages),"packaged_atom_count":atoms,"adapter_count":len(adapters),"blocker_count":len(blockers),"setup_binding_count":len(bindings)}
