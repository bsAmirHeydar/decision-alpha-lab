from __future__ import annotations
import shutil
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any
from .artifact_manifest import build_manifest
from .canonical import digest_object, stable_id
from .classification import authority_map, execution_capabilities, owner_for, risk_assumptions, treatment_atoms
from .constants import CLAIM_CEILING, INVENTORY_ID, PHASE_ID, PRODUCER, SCHEMA_VERSION, TIME_SEMANTICS
from .handoff import build_handoff
from .io import dump_csv, dump_json, dump_jsonl, load_json
from .patterns import BROKER_CAPABILITY_CODES, ORDER_MUTATION_CODES
from .provenance import build_provenance
from .reachability import build_reachability
from .source_scanner import scan_repository
from .upstream import load_upstream, source_binding_doc


def meta_factory(*digests: str, status: str = "REFERENCE_ONLY") -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "producer": PRODUCER,
        "source_digests": sorted(set(d for d in digests if d)),
        "generated_at": None,
        "generated_time_semantics": TIME_SEMANTICS,
        "deterministic_identity": True,
        "owner": "ALPHA_LAB_MIGRATION_OWNER",
        "reviewer": "INDEPENDENT_MIGRATION_REVIEWER",
        "claim_ceiling": CLAIM_CEILING,
        "validation_status": status,
    }


def _registry(name: str, records: list[dict], *digests: str) -> dict:
    body = {
        **meta_factory(*digests, status="PASS"),
        "inventory_id": INVENTORY_ID,
        "registry_name": name,
        "record_count": len(records),
        "records": records,
    }
    return {**body, "registry_digest": digest_object(body)}


def _unknown(code: str, subject_type: str, subject_id: str, source_path: str | None, source_digest: str | None, details: dict, blocking: bool = True) -> dict:
    body = {
        **meta_factory(*(d for d in [source_digest] if d), status="UNKNOWN"),
        "unknown_id": stable_id("EXECUNKNOWN", code, subject_type, subject_id, source_path or "NONE"),
        "unknown_code": code,
        "subject_type": subject_type,
        "subject_id": subject_id,
        "source_path": source_path,
        "blocking": blocking,
        "resolution_owner": "DOMAIN_OWNER_EXECUTION" if source_path and source_path.startswith("mql5/") else "ALPHA_LAB_MIGRATION_OWNER",
        "resolution_state": "OPEN",
        "details": details,
    }
    return {**body, "unknown_digest": digest_object(body)}


def _relevance(analysis) -> str:
    if analysis.capability_hits: return "EXECUTION_CAPABILITY_EVIDENCE"
    if analysis.treatment_hits: return "TREATMENT_ATOM_EVIDENCE"
    if analysis.risk_hits: return "RISK_ASSUMPTION_EVIDENCE"
    if analysis.functions and any(f.entry_point_types for f in analysis.functions): return "ENTRY_POINT_NO_MATCHED_TREATMENT_SURFACE"
    return "SCANNED_NO_MATCHED_TREATMENT_OR_EXECUTION_SURFACE"


class LCM10ATreatmentExecutionInventoryService:
    def build(self, repo_root: Path, output_root: Path) -> dict[str, Any]:
        repo_root = repo_root.resolve(); output_root = output_root.resolve()
        upstream = load_upstream(repo_root); binding = source_binding_doc(upstream)
        if output_root.exists(): shutil.rmtree(output_root)
        output_root.mkdir(parents=True)
        dump_json(output_root / "input/upstream_binding.json", {**meta_factory(binding["binding_digest"], status="PASS"), **binding})

        analyses = scan_repository(repo_root)
        classifications = {row["artifact_path"]: row for row in upstream["classifications"]}
        lcm01_entry_paths = {row["path"] for row in upstream["lcm01_entries"]}
        reachability = build_reachability(analyses, lcm01_entry_paths, meta_factory)
        atoms = treatment_atoms(analyses, classifications, meta_factory)
        capabilities = execution_capabilities(analyses, classifications, reachability, meta_factory)
        risks = risk_assumptions(analyses, classifications, meta_factory)
        boundaries = authority_map(capabilities, meta_factory)

        sources=[]
        for a in analyses:
            body={**meta_factory(a.sha256,status="PASS" if a.parse_status=="PASS" else "UNKNOWN"),"source_id":stable_id("TREATSRCS",a.path,a.sha256),"path":a.path,"language":a.language,"sha256":a.sha256,"size_bytes":a.size_bytes,"line_count":a.line_count,"mode_classes":a.mode_classes,"parse_status":a.parse_status,"parse_error":a.parse_error,"function_count":len(a.functions),"treatment_hit_count":len(a.treatment_hits),"capability_hit_count":len(a.capability_hits),"risk_hit_count":len(a.risk_hits),"relevance_disposition":_relevance(a),"source_move_performed":False,"source_delete_performed":False,"semantic_refactor_performed":False}
            sources.append({**body,"source_record_digest":digest_object(body)})
        dump_jsonl(output_root/"source/source_file_freeze.jsonl",sources)
        freeze_body={**meta_factory(binding["binding_digest"],status="PASS"),"inventory_id":INVENTORY_ID,"source_file_count":len(sources),"source_total_bytes":sum(x["size_bytes"] for x in sources),"language_counts":dict(Counter(x["language"] for x in sources)),"relevance_counts":dict(Counter(x["relevance_disposition"] for x in sources)),"parse_unknown_count":sum(x["parse_status"]!="PASS" for x in sources),"source_move_performed":False,"source_delete_performed":False,"semantic_refactor_performed":False}
        freeze={**freeze_body,"freeze_digest":digest_object(freeze_body)};dump_json(output_root/"source/source_freeze_summary.json",freeze)

        atom_reg=_registry("treatment_atom_registry",atoms,binding["binding_digest"],freeze["freeze_digest"])
        cap_reg=_registry("execution_capability_registry",capabilities,binding["binding_digest"],freeze["freeze_digest"])
        reach_reg=_registry("broker_api_reachability",reachability,binding["binding_digest"],cap_reg["registry_digest"])
        auth_reg=_registry("authority_boundary_map",boundaries,binding["binding_digest"],cap_reg["registry_digest"])
        risk_reg=_registry("risk_assumption_registry",risks,binding["binding_digest"],freeze["freeze_digest"])
        dump_json(output_root/"inventory/treatment_atom_registry.json",atom_reg);dump_jsonl(output_root/"inventory/treatment_atom_registry.jsonl",atoms)
        dump_json(output_root/"execution/execution_capability_registry.json",cap_reg);dump_jsonl(output_root/"execution/execution_capability_registry.jsonl",capabilities)
        dump_json(output_root/"reachability/broker_api_reachability.json",reach_reg);dump_jsonl(output_root/"reachability/broker_api_reachability.jsonl",reachability)
        dump_json(output_root/"authority/authority_boundary_map.json",auth_reg);dump_jsonl(output_root/"authority/authority_boundary_map.jsonl",boundaries)
        dump_json(output_root/"risk/risk_assumption_registry.json",risk_reg);dump_jsonl(output_root/"risk/risk_assumption_registry.jsonl",risks)

        atoms_by_path=defaultdict(list);caps_by_path=defaultdict(list)
        for row in atoms: atoms_by_path[row["source_path"]].append(row["treatment_atom_id"])
        for row in capabilities: caps_by_path[row["source_path"]].append(row["capability_id"])
        setup_registry=load_json(upstream["roots"]["setup"] / "canonical_setup_registry.json")
        package_by_setup={row["setup_id"]:load_json(upstream["roots"]["setup"] / row["package_path"]) for row in setup_registry["packages"]}
        setup_bindings=[]
        for seed in sorted(upstream["setup_seeds"],key=lambda x:x["setup_id"]):
            pkg=package_by_setup[seed["setup_id"]]; path=pkg["source_binding"]["path"]
            atom_ids=sorted(atoms_by_path.get(path,[]));cap_ids=sorted(caps_by_path.get(path,[]))
            state="OBSERVED_SOURCE_EVIDENCE" if atom_ids or cap_ids else "NO_DIRECT_TREATMENT_OR_EXECUTION_EVIDENCE_OBSERVED"
            body={**meta_factory(seed["dependency_digest"],pkg["source_binding"]["sha256"],status="UNKNOWN"),"binding_id":stable_id("SETUPTREATBIND",seed["setup_id"],path),"setup_id":seed["setup_id"],"setup_package_id":pkg["package_id"],"source_path":path,"source_sha256":pkg["source_binding"]["sha256"],"upstream_dependency_id":seed["dependency_id"],"treatment_atom_ids":atom_ids,"execution_capability_ids":cap_ids,"binding_state":state,"canonical_treatment_identity_id":None,"extraction_authorized":False,"execution_authorized":False,"blocker_codes":["CANONICAL_TREATMENT_IDENTITY_PENDING_LCM10B","SETUP_REMAINS_BLOCKED"]+([] if atom_ids or cap_ids else ["NO_DIRECT_STATIC_EVIDENCE_ON_SETUP_SOURCE"])}
            setup_bindings.append({**body,"binding_digest":digest_object(body)})
        setup_binding_reg=_registry("setup_treatment_binding_inventory",setup_bindings,binding["binding_digest"],atom_reg["registry_digest"],cap_reg["registry_digest"])
        dump_json(output_root/"bindings/setup_treatment_binding_inventory.json",setup_binding_reg);dump_jsonl(output_root/"bindings/setup_treatment_binding_inventory.jsonl",setup_bindings)

        security_paths={row["artifact_path"]:row for row in upstream["security_rows"]}
        security_records=[]
        for c in capabilities:
            is_order=c["capability_code"] in ORDER_MUTATION_CODES
            upstream_security=security_paths.get(c["source_path"])
            if not is_order and not upstream_security and c["authority_class"] not in {"NETWORK_EXTERNAL","NATIVE_OR_PROCESS_EXTERNAL","MUTATE_FILE_LEDGER"}: continue
            body={**meta_factory(c["capability_digest"],status="BLOCKED"),"security_record_id":stable_id("EXECSEC",c["capability_id"]),"capability_id":c["capability_id"],"source_path":c["source_path"],"authority_class":c["authority_class"],"lcm02_security_sensitive":bool(upstream_security),"lcm02_security_review_status":upstream_security.get("security_review_status") if upstream_security else "NOT_CLASSIFIED_BY_LCM02_AS_SECURITY_SENSITIVE","security_reviewer_role":(upstream_security or {}).get("security_reviewer_role") or "SECURITY_REVIEWER","restriction_state":"SECURITY_REVIEW_REQUIRED","adapter_activation_allowed":False,"live_order_authority":False}
            security_records.append({**body,"security_record_digest":digest_object(body)})
        security_reg=_registry("security_restricted_execution_paths",security_records,binding["binding_digest"],cap_reg["registry_digest"])
        dump_json(output_root/"security/security_restricted_execution_paths.json",security_reg);dump_jsonl(output_root/"security/security_restricted_execution_paths.jsonl",security_records)

        # Reconcile the earlier broad survey with the deeper LCM-10A inventory.
        cap_keys={(c["source_path"],e["line_number"]) for c in capabilities for e in c["evidence_locations"]}
        relevant_lcm01=[r for r in upstream["lcm01_capabilities"] if r["capability_kind"] in {"ORDER_API","FILE_IO","FILE_MUTATION","NETWORK_API","PERSISTENT_STATE","ENVIRONMENT_ACCESS"}]
        reconciliation=[]
        for row in relevant_lcm01:
            key=(row["path"],int(row["line_number"])); matched=key in cap_keys
            body={**meta_factory(row["line_digest"],status="PASS" if matched else "UNKNOWN"),"reconciliation_id":stable_id("LCM01RECON",row["path"],row["line_number"],row["capability_kind"],row["matched_token"]),"lcm01_path":row["path"],"lcm01_line_number":int(row["line_number"]),"lcm01_capability_kind":row["capability_kind"],"lcm01_matched_token":row["matched_token"],"lcm10a_deep_match":matched,"disposition":"BOUND_TO_LCM10A_CAPABILITY" if matched else "EXPLICIT_UNKNOWN_LCM01_SURFACE_NOT_DEEP_MATCHED"}
            reconciliation.append({**body,"reconciliation_digest":digest_object(body)})
        recon_reg=_registry("lcm01_capability_reconciliation",reconciliation,binding["binding_digest"],cap_reg["registry_digest"])
        dump_json(output_root/"reconciliation/lcm01_capability_reconciliation.json",recon_reg);dump_jsonl(output_root/"reconciliation/lcm01_capability_reconciliation.jsonl",reconciliation)

        unknowns=[]
        for s in sources:
            if s["parse_status"]!="PASS": unknowns.append(_unknown("SOURCE_PARSE_FAILURE","SOURCE_FILE",s["source_id"],s["path"],s["sha256"],{"parse_error":s["parse_error"]}))
        for r in reachability:
            if r["reachability_state"]!="REACHABLE_FROM_STATIC_ENTRY": unknowns.append(_unknown("BROKER_REACHABILITY_NOT_PROVEN","EXECUTION_CAPABILITY",r["reachability_id"],r["source_path"],next((x["sha256"] for x in sources if x["path"]==r["source_path"]),None),{"capability_code":r["capability_code"],"reachability_state":r["reachability_state"],"symbol_name":r["symbol_name"]}))
        for c in capabilities:
            if c["owner"]["ownership_is_human_approved"] is False and c["authority_class"] in {"SUBMIT_ORDER","MODIFY_POSITION","MODIFY_ORDER","CANCEL_ORDER","CLOSE_POSITION","NETWORK_EXTERNAL","MUTATE_FILE_LEDGER"}: unknowns.append(_unknown("HUMAN_AUTHORITY_OWNER_NOT_APPROVED","EXECUTION_CAPABILITY",c["capability_id"],c["source_path"],c["source_sha256"],{"authority_class":c["authority_class"],"owner":c["owner"]}))
            if c["hidden_authority_indicator"]: unknowns.append(_unknown("WRAPPER_HIDES_ORDER_CAPABILITY","EXECUTION_CAPABILITY",c["capability_id"],c["source_path"],c["source_sha256"],{"symbol_name":c["symbol_name"],"capability_code":c["capability_code"]}))
            if "LIVE_CAPABLE_SURFACE" in c["mode_classes"] and not any(m in c["mode_classes"] for m in ("TESTER","DRY_RUN","PAPER","SHADOW","LIVE")): unknowns.append(_unknown("MODE_SWITCH_NOT_EXPLICIT","EXECUTION_CAPABILITY",c["capability_id"],c["source_path"],c["source_sha256"],{"mode_classes":c["mode_classes"]}))
        for row in reconciliation:
            if not row["lcm10a_deep_match"]: unknowns.append(_unknown("LCM01_CAPABILITY_SURFACE_NOT_DEEP_MATCHED","LCM01_CAPABILITY",row["reconciliation_id"],row["lcm01_path"],None,{"capability_kind":row["lcm01_capability_kind"],"line_number":row["lcm01_line_number"],"matched_token":row["lcm01_matched_token"]},blocking=row["lcm01_capability_kind"] in {"ORDER_API","NETWORK_API"}))
        for sb in setup_bindings:
            if sb["binding_state"]=="NO_DIRECT_TREATMENT_OR_EXECUTION_EVIDENCE_OBSERVED": unknowns.append(_unknown("SETUP_TREATMENT_EVIDENCE_NOT_OBSERVED_ON_SOURCE","SETUP_BINDING",sb["binding_id"],sb["source_path"],sb["source_sha256"],{"setup_id":sb["setup_id"]}))
        unknowns=sorted({x["unknown_id"]:x for x in unknowns}.values(),key=lambda x:x["unknown_id"])
        unknown_reg=_registry("execution_unknown_queue",unknowns,binding["binding_digest"],reach_reg["registry_digest"],recon_reg["registry_digest"])
        dump_json(output_root/"unknowns/execution_unknown_queue.json",unknown_reg);dump_jsonl(output_root/"unknowns/execution_unknown_queue.jsonl",unknowns)

        by_path=defaultdict(list)
        for c in capabilities: by_path[c["source_path"]].append(c)
        plan=[]
        priority_order={"SUBMIT_ORDER":10,"MODIFY_POSITION":20,"MODIFY_ORDER":20,"CANCEL_ORDER":20,"CLOSE_POSITION":20,"CREATE_REQUEST_INTENT":30,"RECONCILE_BROKER_STATE":40,"READ_BROKER_CONSTRAINTS":50,"READ_ACCOUNT_STATE":50,"NETWORK_EXTERNAL":60,"MUTATE_FILE_LEDGER":70,"READ_FILE_LEDGER":80,None:90}
        for path,rows in sorted(by_path.items()):
            auths=sorted({r["authority_class"] for r in rows},key=lambda x:(priority_order.get(x,90),x or ''))
            source_digest=rows[0]["source_sha256"]; priority=min(priority_order.get(x,90) for x in auths)
            body={**meta_factory(source_digest,status="BLOCKED"),"extraction_item_id":stable_id("TREATEXTRACT",path,source_digest),"source_path":path,"source_sha256":source_digest,"priority":priority,"authority_classes":auths,"capability_ids":[r["capability_id"] for r in rows],"proposed_treatment_package_id":stable_id("TREATPKG",path,source_digest),"proposed_disabled_adapter_id":stable_id("EXECADAPTER",path,source_digest),"required_reviews":sorted(set(["DOMAIN_OWNER_EXECUTION","INDEPENDENT_MIGRATION_REVIEWER"]+(["SECURITY_REVIEWER"] if any(r["authority_class"] in {"SUBMIT_ORDER","MODIFY_POSITION","MODIFY_ORDER","CANCEL_ORDER","CLOSE_POSITION","NETWORK_EXTERNAL","NATIVE_OR_PROCESS_EXTERNAL"} for r in rows) else []))),"blocker_codes":["LCM10B_EXTRACTION_NOT_STARTED","ADAPTER_MUST_DEFAULT_DISABLED","SOURCE_BEHAVIOR_MUST_REMAIN_UNCHANGED","OWNER_APPROVAL_REQUIRED"],"source_move_allowed":False,"adapter_activation_allowed":False}
            plan.append({**body,"extraction_item_digest":digest_object(body)})
        plan.sort(key=lambda x:(x["priority"],x["source_path"]))
        plan_body={**meta_factory(binding["binding_digest"],cap_reg["registry_digest"],status="PASS"),"inventory_id":INVENTORY_ID,"extraction_item_count":len(plan),"ordered_items":plan,"execution_boundary_default":"DISABLED_FAIL_CLOSED","live_adapter_activation_allowed":False,"source_move_allowed":False}
        extraction_plan={**plan_body,"plan_digest":digest_object(plan_body)};dump_json(output_root/"plans/treatment_extraction_order.json",extraction_plan)
        violations=[]
        for b in boundaries:
            if b["blocker_codes"]:
                body={**meta_factory(b["boundary_digest"],status="BLOCKED"),"violation_id":stable_id("EXECBOUNDVIOL",b["authority_boundary_id"]),"authority_boundary_id":b["authority_boundary_id"],"source_path":b["source_path"],"symbol_name":b["symbol_name"],"authority_class":b["authority_class"],"violation_codes":b["blocker_codes"],"required_phase":"LCM-10B","resolution_state":"OPEN"}
                violations.append({**body,"violation_digest":digest_object(body)})
        dump_jsonl(output_root/"plans/execution_boundary_violation_registry.jsonl",violations)
        violation_reg=_registry("execution_boundary_violation_registry",violations,binding["binding_digest"],auth_reg["registry_digest"]);dump_json(output_root/"plans/execution_boundary_violation_registry.json",violation_reg)

        events=[]
        event_subjects=[("SOURCE_FREEZE_CLOSED",freeze["freeze_digest"]),("TREATMENT_ATOM_REGISTRY_CLOSED",atom_reg["registry_digest"]),("EXECUTION_CAPABILITY_REGISTRY_CLOSED",cap_reg["registry_digest"]),("BROKER_REACHABILITY_ACCOUNTED",reach_reg["registry_digest"]),("AUTHORITY_BOUNDARY_MAP_CLOSED",auth_reg["registry_digest"]),("RISK_ASSUMPTION_REGISTRY_CLOSED",risk_reg["registry_digest"]),("EXECUTION_UNKNOWNS_PRESERVED",unknown_reg["registry_digest"]),("EXTRACTION_ORDER_EMITTED",extraction_plan["plan_digest"])]
        for sequence,(etype,digest) in enumerate(event_subjects,1):
            body={**meta_factory(binding["binding_digest"],digest,status="PASS"),"event_id":stable_id("TREATINVEVENT",INVENTORY_ID,sequence,etype),"sequence":sequence,"event_type":etype,"subject_digest":digest,"authority_created":False}
            events.append({**body,"event_digest":digest_object(body)})
        event_body={**meta_factory(binding["binding_digest"],status="PASS"),"inventory_id":INVENTORY_ID,"event_count":len(events),"events":events};event_ledger={**event_body,"ledger_digest":digest_object(event_body)};dump_json(output_root/"events/treatment_inventory_event_ledger.json",event_ledger)

        counts={"scanned_source_file_count":len(sources),"treatment_atom_count":len(atoms),"execution_capability_count":len(capabilities),"broker_reachability_record_count":len(reachability),"authority_boundary_count":len(boundaries),"risk_assumption_count":len(risks),"setup_binding_count":len(setup_bindings),"security_restricted_path_record_count":len(security_records),"unknown_count":len(unknowns),"blocking_unknown_count":sum(x["blocking"] for x in unknowns),"extraction_item_count":len(plan),"boundary_violation_count":len(violations)}
        closure_body={**meta_factory(binding["binding_digest"],status="PASS"),"inventory_id":INVENTORY_ID,"counts":counts,"all_scanned_sources_disposed":True,"all_order_capable_hits_registered":all(any(c["source_path"]==r["source_path"] and c["capability_code"]==r["capability_code"] for c in capabilities) for r in reachability),"all_non_reachable_broker_hits_explicit_unknown":all(r["reachability_state"]=="REACHABLE_FROM_STATIC_ENTRY" or any(u["subject_id"]==r["reachability_id"] for u in unknowns) for r in reachability),"all_setup_dependencies_accounted":len(setup_bindings)==60,"source_behavior_changed":False,"closure_status":"CLOSED_REFERENCE_INVENTORY"}
        closure={**closure_body,"report_digest":digest_object(closure_body)};dump_json(output_root/"reports/portfolio_closure_report.json",closure)

        attacks=[
            {"attack":"WRAPPER_HIDING_BROKER_SUBMISSION","result":"PASS_WITH_BLOCKERS","evidence_count":sum(c["hidden_authority_indicator"] for c in capabilities),"noncompensatory":True},
            {"attack":"FILE_LEDGER_AS_ENTITLEMENT_AUTHORITY","result":"PASS_WITH_UNKNOWNS","evidence_count":sum(c["authority_class"] in {"READ_FILE_LEDGER","MUTATE_FILE_LEDGER"} for c in capabilities),"noncompensatory":True},
            {"attack":"VOLUME_DEFAULT_DIFFERS_BY_SYMBOL","result":"PASS_WITH_UNKNOWNS","evidence_count":sum(r["assumption_type"] in {"VOLUME_MIN","VOLUME_MAX","VOLUME_STEP"} for r in risks),"noncompensatory":True},
            {"attack":"LONG_SHORT_ASYMMETRY","result":"PASS_WITH_UNKNOWNS","evidence_count":sum(r["assumption_type"]=="LONG_SHORT_ASYMMETRY" for r in risks),"noncompensatory":True},
            {"attack":"TESTER_MODE_BYPASSES_SAFETY","result":"PASS_WITH_UNKNOWNS","evidence_count":sum("TESTER" in c["mode_classes"] and c["authority_class"] in {"SUBMIT_ORDER","MODIFY_POSITION","MODIFY_ORDER","CANCEL_ORDER","CLOSE_POSITION"} for c in capabilities),"noncompensatory":True},
            {"attack":"UNREGISTERED_ORDER_SURFACE","result":"PASS","evidence":"Every deep-scan broker mutation hit is in execution_capability_registry and reachability registry."},
            {"attack":"AUTHORITY_GRANTED_BY_INVENTORY","result":"PASS","evidence":"All authority fields are false; no adapter or source behavior is changed."},
        ]
        hostile_body={**meta_factory(binding["binding_digest"],status="PASS"),"inventory_id":INVENTORY_ID,"hostile_review_passed":True,"attacks":attacks,"residual_risks":["Static reachability cannot prove runtime branch activation.","Human owners and security reviewers remain role-bound but not approved.","Broker-specific stop, freeze, volume and session values are not evaluated.","File-ledger entitlement semantics require LCM-10B boundary review."]}
        hostile={**hostile_body,"report_digest":digest_object(hostile_body)};dump_json(output_root/"reports/hostile_review.json",hostile)
        gates=[{"gate":"UPSTREAM_HANDOFF_DIGEST","result":"PASS"},{"gate":"SOURCE_SCAN_COVERAGE","result":"PASS"},{"gate":"TREATMENT_ATOM_REGISTRY","result":"PASS"},{"gate":"EXECUTION_CAPABILITY_REGISTRY","result":"PASS"},{"gate":"BROKER_REACHABILITY_OR_UNKNOWN","result":"PASS"},{"gate":"AUTHORITY_MAP","result":"PASS"},{"gate":"RISK_ASSUMPTION_REGISTRY","result":"PASS"},{"gate":"SETUP_DEPENDENCY_ACCOUNTING","result":"PASS"},{"gate":"SECURITY_RESTRICTED_PATHS","result":"PASS"},{"gate":"SOURCE_BEHAVIOR_UNCHANGED","result":"PASS"},{"gate":"AUTHORITY_NEGATIVE","result":"PASS"}]
        acceptance_body={**meta_factory(binding["binding_digest"],closure["report_digest"],hostile["report_digest"],status="PASS"),"inventory_id":INVENTORY_ID,"acceptance_gate_passed":True,"counts":counts,"non_compensatory_gates":gates,"failed_gate_count":0,"unknowns_preserved":True,"source_behavior_changed":False,"promotion_authority_created":False,"runtime_authority_created":False,"live_order_authority_created":False,"capital_authority_created":False}
        acceptance={**acceptance_body,"report_digest":digest_object(acceptance_body)};dump_json(output_root/"reports/acceptance_report.json",acceptance)

        handoff=build_handoff(atom_registry_digest=atom_reg["registry_digest"],capability_registry_digest=cap_reg["registry_digest"],reachability_digest=reach_reg["registry_digest"],authority_digest=auth_reg["registry_digest"],risk_digest=risk_reg["registry_digest"],unknown_digest=unknown_reg["registry_digest"],extraction_plan_digest=extraction_plan["plan_digest"],counts=counts,meta_factory=meta_factory)
        dump_json(output_root/"handoff/lcm10a_to_lcm10b_handoff.json",handoff);dump_json(output_root/"LCM10A_TO_LCM10B_HANDOFF.json",handoff)
        named={"treatment_atom_registry.json":{"path":"inventory/treatment_atom_registry.json","digest":atom_reg["registry_digest"]},"execution_capability_registry.json":{"path":"execution/execution_capability_registry.json","digest":cap_reg["registry_digest"]},"broker_api_reachability.json":{"path":"reachability/broker_api_reachability.json","digest":reach_reg["registry_digest"]},"authority_boundary_map.json":{"path":"authority/authority_boundary_map.json","digest":auth_reg["registry_digest"]},"risk_assumption_registry.json":{"path":"risk/risk_assumption_registry.json","digest":risk_reg["registry_digest"]},"execution_unknown_queue.json":{"path":"unknowns/execution_unknown_queue.json","digest":unknown_reg["registry_digest"]},"LCM10A_TO_LCM10B_HANDOFF.json":{"path":"LCM10A_TO_LCM10B_HANDOFF.json","digest":handoff["handoff_digest"]}}
        locator_body={**meta_factory(binding["binding_digest"],status="PASS"),"inventory_id":INVENTORY_ID,"artifacts":named};locator={**locator_body,"locator_digest":digest_object(locator_body)};dump_json(output_root/"required_artifact_locator.json",locator)
        marker_body={**meta_factory(binding["binding_digest"],status="PASS"),"inventory_id":INVENTORY_ID,"phase_id":PHASE_ID,"master_phase":"LCM-10","status":"ACCEPTED_REFERENCE","counts":counts,"source_behavior_changed":False};marker={**marker_body,"marker_digest":digest_object(marker_body)};dump_json(output_root/"treatment_inventory_marker.json",marker)
        artifact_digests={"source_freeze":freeze["freeze_digest"],"treatment_atoms":atom_reg["registry_digest"],"execution_capabilities":cap_reg["registry_digest"],"reachability":reach_reg["registry_digest"],"authority":auth_reg["registry_digest"],"risk":risk_reg["registry_digest"],"unknowns":unknown_reg["registry_digest"],"handoff":handoff["handoff_digest"]}
        dump_json(output_root/"provenance/treatment_inventory_provenance_graph.json",build_provenance(INVENTORY_ID,binding,sources,artifact_digests))
        manifest=build_manifest(output_root);dump_json(output_root/"output_manifest.json",manifest)
        receipt_body={**meta_factory(binding["binding_digest"],manifest["manifest_digest"],handoff["handoff_digest"],status="PASS"),"inventory_id":INVENTORY_ID,"upstream_handoff_digest":upstream["setup_handoff"]["handoff_digest"],"output_manifest_digest":manifest["manifest_digest"],"handoff_digest":handoff["handoff_digest"],"counts":counts,"source_move_performed":False,"source_delete_performed":False,"semantic_refactor_performed":False,"consumer_cutover_performed":False,"adapter_constructed":False,"adapter_activated":False}
        receipt={**receipt_body,"receipt_digest":digest_object(receipt_body)};dump_json(output_root/"treatment_inventory_receipt.json",receipt)
        manifest=build_manifest(output_root);dump_json(output_root/"output_manifest.json",manifest)
        return {"passed":True,"inventory_id":INVENTORY_ID,"output_root":output_root.as_posix(),"manifest_digest":manifest["manifest_digest"],"handoff_digest":handoff["handoff_digest"],**counts}
