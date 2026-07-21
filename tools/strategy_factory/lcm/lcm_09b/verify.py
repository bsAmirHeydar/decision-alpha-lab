from __future__ import annotations
from pathlib import Path
from .artifact_manifest import build_manifest
from .canonical import digest_object,file_digest
from .contracts import validate_package
from .errors import IntegrityError
from .factory_bridge import SetupFactoryReferencePort
from .io import load_json,load_jsonl
REQUIRED=("setup_migration_marker.json","input/lcm09a_binding.json","canonical_setup_registry.json","adapters/setup_adapter_registry.json","factory/setup_factory_registration.json","golden/setup_golden_cases.jsonl","golden/setup_golden_traces.jsonl","parity/setup_parity_registry.jsonl","parity/setup_parity_registry.json","parity/setup_variance_decisions.json","blockers/setup_blocker_registry.jsonl","dependencies/treatment_dependency_inventory_seed.jsonl","events/setup_migration_event_ledger.json","provenance/setup_migration_provenance_graph.json","reports/portfolio_closure_report.json","reports/hostile_review.json","reports/acceptance_report.json","handoff/lcm09b_to_lcm10a_handoff.json","LCM09B_TO_LCM10A_HANDOFF.json","required_artifact_locator.json","output_manifest.json","setup_migration_receipt.json")
def verify_package(root:Path)->dict:
    for rel in REQUIRED:
        if not (root/rel).is_file():raise IntegrityError("LCM09B_MISSING_ARTIFACT:"+rel)
    manifest=load_json(root/"output_manifest.json")
    for row in manifest["files"]:
        p=root/row["path"]
        if not p.is_file() or p.stat().st_size!=row["size_bytes"] or file_digest(p)!=row["sha256"]:raise IntegrityError("LCM09B_MANIFEST_MISMATCH:"+row["path"])
    registry=load_json(root/"canonical_setup_registry.json");packages=[]
    for row in registry["packages"]:
        p=root/row["package_path"];doc=load_json(p);packages.append(doc)
        failures=validate_package(doc)
        if failures:raise IntegrityError("LCM09B_PACKAGE_INVALID:"+doc["setup_id"]+":"+",".join(failures))
        if doc["package_digest"]!=row["package_digest"]:raise IntegrityError("LCM09B_REGISTRY_DIGEST_MISMATCH")
    if len(packages)!=60 or len({p["setup_id"] for p in packages})!=60:raise IntegrityError("LCM09B_PORTFOLIO_COUNT_MISMATCH")
    port=SetupFactoryReferencePort(root/"factory/setup_factory_registration.json")
    parity=load_jsonl(root/"parity/setup_parity_registry.jsonl")
    parity_registry=load_json(root/"parity/setup_parity_registry.json")
    if len(parity)!=60 or any(x["parity_status"]=="FAIL" for x in parity):raise IntegrityError("LCM09B_PARITY_DISPOSITION_INVALID")
    if parity_registry["records"]!=parity or parity_registry["record_count"]!=60 or digest_object(parity_registry,"registry_digest")!=parity_registry["registry_digest"]:raise IntegrityError("LCM09B_PARITY_REGISTRY_INVALID")
    acceptance=load_json(root/"reports/acceptance_report.json");hostile=load_json(root/"reports/hostile_review.json")
    if not acceptance["acceptance_gate_passed"] or not hostile["hostile_review_passed"]:raise IntegrityError("LCM09B_ACCEPTANCE_FAILED")
    handoff=load_json(root/"handoff/lcm09b_to_lcm10a_handoff.json")
    handoff_alias=load_json(root/"LCM09B_TO_LCM10A_HANDOFF.json")
    locator=load_json(root/"required_artifact_locator.json")
    if digest_object(handoff,"handoff_digest")!=handoff["handoff_digest"] or handoff_alias!=handoff:raise IntegrityError("LCM09B_HANDOFF_DIGEST_MISMATCH")
    if digest_object(locator,"locator_digest")!=locator["locator_digest"]:raise IntegrityError("LCM09B_ARTIFACT_LOCATOR_DIGEST_MISMATCH")
    for key in ("consumer_cutover_allowed","promotion_authority_created","runtime_authority_created","live_order_authority_created","capital_authority_created"):
        if handoff[key]:raise IntegrityError("LCM09B_AUTHORITY_EXPANSION:"+key)
    return {"passed":True,"migration_id":registry["migration_id"],"package_count":len(packages),"factory_registration_count":len(port.list_reference_candidates()),"parity_record_count":len(parity),"blocked_count":sum(p["package_status"]=="REFERENCE_BLOCKED" for p in packages),"ready_count":sum(p["package_status"]=="REFERENCE_READY" for p in packages),"manifest_file_count":manifest["file_count"]}
def verify_installation(repo_root:Path,package_root:Path,index_path:Path)->dict:
    paths=[x.strip() for x in index_path.read_text(encoding="utf-8").splitlines() if x.strip()]
    missing=[x for x in paths if not (repo_root/x).exists()]
    if missing:raise IntegrityError("LCM09B_INSTALLATION_MISSING:"+str(missing[:10]))
    forbidden=[x for x in paths if x.startswith(("mql5/Experts/","mql5/Include/Research/"))]
    if forbidden:raise IntegrityError("LCM09B_LEGACY_SOURCE_MUTATION:"+str(forbidden[:10]))
    return {**verify_package(package_root),"installation_passed":True,"indexed_path_count":len(paths)}
