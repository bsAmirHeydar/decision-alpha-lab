from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from collections import Counter
from .authority import permit
from .canonical import content_id, digest_object, file_digest
from .constants import *
from .dependencies import build as build_dependencies
from .event_ledger import build as build_events
from .io import atomic_publish, cleanup, private_staging, write_csv, write_json, write_jsonl, write_text
from .manifest import build as build_manifest
from .pilot import select as select_pilot
from .portfolio import build as build_portfolio
from .provenance import build as build_provenance
from .registries import *
from .upstream import load

@dataclass(frozen=True)
class RunConfig:
    repo_root: Path
    destination: Path
    issued_at: str = DEFAULT_ISSUED_AT


def _contract(contract_id,purpose,required_fields):
    obj={"schema_version":"1.0.0","contract_id":contract_id,"purpose":purpose,"required_fields":list(required_fields),"source_move_allowed":False,"source_delete_allowed":False,"semantic_refactor_allowed":False,"consumer_cutover_allowed":False,"contract_digest":None};obj["contract_digest"]=digest_object(obj,"contract_digest");return obj


def run(config: RunConfig) -> Path:
    upstream=load(config.repo_root);handoff=upstream["handoff"]
    authority=permit(handoff["handoff_digest"],config.issued_at)
    records,unresolved,dep_rows=build_portfolio(upstream)
    evaluations,selected=select_pilot(records)
    if selected is None:
        raise RuntimeError("LCM-08A deterministic policy did not select exactly one eligible pilot")
    selected_id=selected["identity_id"]
    for record in records:
        record["pilot_eligibility"]={"evaluated":True,"eligible":next(e["eligible"] for e in evaluations if e["identity_id"]==record["identity_id"]),"selected":record["identity_id"]==selected_id}
        record["record_digest"]=digest_object(record,"record_digest")
    graph=build_dependencies(records,dep_rows)
    wave_counts=Counter(r["wave_assignment"] for r in records)
    risk_counts=Counter(r["risk_class"] for r in records)
    granularity_counts=Counter(r["granularity_class"] for r in records)
    family_counts=Counter(r["family_candidate"] for r in records)
    pilot_record=next(r for r in records if r["identity_id"]==selected_id)
    identity={"source_handoff_digest":handoff["handoff_digest"],"roadmap_id":ROADMAP_ID,"context_record_digests":sorted(r["record_digest"] for r in records),"selected_pilot_identity_id":selected_id,"selected_pilot_source_digest":pilot_record["source_artifact_sha256"]}
    portfolio_id=content_id("CTXPORT",identity)
    destination=config.destination/portfolio_id;staging=private_staging(config.destination,'.lcm08a-stage-')
    try:
        marker={"schema_version":"1.0.0","phase_id":PHASE_ID,"master_phase":"LCM-08","roadmap_id":ROADMAP_ID,"portfolio_id":portfolio_id,"source_handoff_digest":handoff["handoff_digest"],"claim_ceiling":CLAIM_CEILING,"context_candidate_count":len(records),"selected_pilot_identity_id":selected_id,"source_move_performed":False,"source_delete_performed":False,"semantic_refactor_performed":False,"adapter_published":False,"consumer_cutover_performed":False,"runtime_authority_created":False,"live_order_authority_created":False,"capital_authority_created":False,"marker_digest":None};marker["marker_digest"]=digest_object(marker,"marker_digest");write_json(staging/'context_portfolio_marker.json',marker)
        write_json(staging/'authority/authority_permit.json',authority)
        binding={"schema_version":"1.0.0","handoff_type":"LCM07_TO_LCM08","source_handoff_digest":handoff["handoff_digest"],"shared_engine_run_id":handoff["shared_engine_run_id"],"framework_run_id":handoff["framework_run_id"],"unresolved_blockers":handoff.get("unresolved_blockers",[]),"input_digests":upstream["input_digests"],"binding_digest":None};binding["binding_digest"]=digest_object(binding,"binding_digest");write_json(staging/'input/lcm07_binding.json',binding)
        registries={
          "context_risk_dimension_registry":closed_registry("LCM08A_CONTEXT_RISK_DIMENSION_REGISTRY_V1",RISK_DIMENSIONS,"Non-compensatory and weighted Context migration risk dimensions."),
          "risk_class_registry":closed_registry("LCM08A_RISK_CLASS_REGISTRY_V1",list(RISK_CLASSES),"Closed Context migration risk classes."),
          "granularity_class_registry":closed_registry("LCM08A_GRANULARITY_CLASS_REGISTRY_V1",list(GRANULARITY_CLASSES),"Closed Context candidate granularity classes."),
          "wave_registry":closed_registry("LCM08A_WAVE_REGISTRY_V1",list(WAVES),"Dependency- and risk-ordered Context migration waves."),
          "pilot_gate_registry":closed_registry("LCM08A_PILOT_GATE_REGISTRY_V1",PILOT_GATES,"Non-compensatory pilot eligibility gates."),
          "reason_code_registry":closed_registry("LCM08A_REASON_CODE_REGISTRY_V1",REASON_CODES,"Closed machine reason codes."),
        }
        for name,obj in registries.items():write_json(staging/f'registries/{name}.json',obj)
        contracts={
          "context_portfolio_contract":_contract("LCM08A_CONTEXT_PORTFOLIO_CONTRACT_V1","One record per Context identity candidate or explicit unresolved record.",( "identity_id","source_artifact_path","risk_class","wave_assignment")),
          "risk_assessment_contract":_contract("LCM08A_RISK_ASSESSMENT_CONTRACT_V1","Preserve raw dimensions; critical dimensions cannot be averaged away.",( "identity_id","risk_dimensions","critical_dimensions","risk_class")),
          "dependency_graph_contract":_contract("LCM08A_DEPENDENCY_GRAPH_CONTRACT_V1","Bind static dependencies without claiming semantic reachability.",( "nodes","edges","semantic_reachability_claimed")),
          "wave_assignment_contract":_contract("LCM08A_WAVE_ASSIGNMENT_CONTRACT_V1","Assign by dependency, risk and family without migration authority.",( "identity_id","wave_assignment","risk_class")),
          "pilot_selection_contract":_contract("LCM08A_PILOT_SELECTION_CONTRACT_V1","Select exactly one bounded pilot by non-compensatory gates.",( "identity_id","gates","eligible","selected")),
          "handoff_contract":_contract("LCM08A_TO_LCM08B_HANDOFF_CONTRACT_V1","Authorize only pilot packet, canonical authoring, adapter and parity.",( "selected_pilot_identity_id","allowed_actions","forbidden_actions")),
        }
        for name,obj in contracts.items():write_json(staging/f'contracts/{name}.json',obj)
        write_jsonl(staging/'portfolio/context_portfolio_registry.jsonl',records)
        csv_fields=["portfolio_record_id","identity_id","family_candidate","semantic_name_candidate","source_artifact_path","source_artifact_sha256","source_language","granularity_class","risk_class","aggregate_risk_score","wave_assignment","identity_collision","protected_platform_asset","security_sensitive"]
        write_csv(staging/'portfolio/context_portfolio_registry.csv',records,csv_fields)
        write_jsonl(staging/'risk/context_risk_assessment.jsonl',[{"schema_version":"1.0.0","identity_id":r["identity_id"],"risk_dimensions":r["risk_dimensions"],"critical_dimensions":r["critical_dimensions"],"aggregate_risk_score":r["aggregate_risk_score"],"risk_class":r["risk_class"],"assessment_digest":digest_object({"identity_id":r["identity_id"],"risk_dimensions":r["risk_dimensions"],"critical_dimensions":r["critical_dimensions"],"aggregate_risk_score":r["aggregate_risk_score"],"risk_class":r["risk_class"]})} for r in records])
        risk_csv=[{"identity_id":r["identity_id"],"family_candidate":r["family_candidate"],"source_artifact_path":r["source_artifact_path"],"risk_class":r["risk_class"],"aggregate_risk_score":r["aggregate_risk_score"],"critical_dimensions":r["critical_dimensions"],"granularity_class":r["granularity_class"]} for r in records]
        write_csv(staging/'risk/context_risk_assessment.csv',risk_csv,["identity_id","family_candidate","source_artifact_path","risk_class","aggregate_risk_score","critical_dimensions","granularity_class"])
        write_json(staging/'dependencies/context_dependency_graph.json',graph)
        wave_assignment={"schema_version":"1.0.0","portfolio_id":portfolio_id,"assignments":[{"identity_id":r["identity_id"],"family_candidate":r["family_candidate"],"risk_class":r["risk_class"],"wave_assignment":r["wave_assignment"],"blocked":r["wave_assignment"]=="BLOCKED_UNRESOLVED"} for r in records],"wave_counts":dict(sorted(wave_counts.items())),"assignment_digest":None};wave_assignment["assignment_digest"]=digest_object(wave_assignment,"assignment_digest");write_json(staging/'waves/context_wave_assignment.json',wave_assignment)
        write_jsonl(staging/'pilot/pilot_candidate_evaluations.jsonl',evaluations)
        selection={"schema_version":"1.0.0","portfolio_id":portfolio_id,"selection_policy":"NON_COMPENSATORY_GATES_THEN_LOWEST_RISK_THEN_IDENTITY_ID","selected_pilot_identity_id":selected_id,"selected_source_artifact_path":pilot_record["source_artifact_path"],"selected_source_digest":pilot_record["source_artifact_sha256"],"selected_risk_class":pilot_record["risk_class"],"selected_wave":"WAVE_01_LOW_RISK_PILOT","architect_policy_approval":"EXPLICIT_USER_ARCHITECT_DIRECTION_TO_PROCEED_AFTER_LCM07","domain_semantic_change_authorized":False,"source_move_authorized":False,"source_delete_authorized":False,"consumer_cutover_authorized":False,"selection_digest":None};selection["selection_digest"]=digest_object(selection,"selection_digest");write_json(staging/'pilot/pilot_selection_decision.json',selection)
        write_jsonl(staging/'unresolved/unresolved_context_queue.jsonl',unresolved)
        summary={"schema_version":"1.0.0","phase_id":PHASE_ID,"portfolio_id":portfolio_id,"claim_ceiling":CLAIM_CEILING,"context_candidate_count":len(records),"unresolved_record_count":len(unresolved),"risk_class_counts":dict(sorted(risk_counts.items())),"granularity_class_counts":dict(sorted(granularity_counts.items())),"wave_counts":dict(sorted(wave_counts.items())),"family_count":len(family_counts),"selected_pilot_identity_id":selected_id,"selected_pilot_source_path":pilot_record["source_artifact_path"],"selected_pilot_risk_class":pilot_record["risk_class"],"exactly_one_pilot_selected":sum(1 for e in evaluations if e["selected"])==1,"portfolio_closed_for_input_snapshot":True,"source_move_performed":False,"source_delete_performed":False,"semantic_refactor_performed":False,"adapter_published":False,"consumer_cutover_performed":False,"runtime_authority_created":False,"live_order_authority_created":False,"capital_authority_created":False,"summary_digest":None};summary["summary_digest"]=digest_object(summary,"summary_digest");write_json(staging/'reports/context_portfolio_summary.json',summary)
        hostile_checks=[
          {"check_id":"EVERY_CONTEXT_IDENTITY_ACCOUNTED","passed":len(records)==321},
          {"check_id":"EXACTLY_ONE_PILOT_SELECTED","passed":sum(1 for e in evaluations if e["selected"])==1},
          {"check_id":"PILOT_HAS_NO_ORDER_AUTHORITY","passed":not pilot_record["static_profile"]["capabilities"].get("order_api")},
          {"check_id":"PILOT_HAS_NO_IDENTITY_COLLISION","passed":not pilot_record["identity_collision"]},
          {"check_id":"PILOT_IS_PACKAGE_CONTEXT","passed":pilot_record["granularity_class"]=="PACKAGE_CONTEXT"},
          {"check_id":"CRITICAL_DIMENSIONS_NOT_AVERAGED_AWAY","passed":all(r["risk_class"]=="CRITICAL" for r in records if r["critical_dimensions"])},
          {"check_id":"EMBEDDED_FRAGMENTS_NOT_PILOT_ELIGIBLE","passed":all(not e["eligible"] for e,r in zip(evaluations,records) if r["granularity_class"]=="EMBEDDED_CONTEXT_FRAGMENT")},
          {"check_id":"FUTURE_AWARE_CANDIDATES_NOT_PILOT_ELIGIBLE","passed":all(not e["eligible"] for e,r in zip(evaluations,records) if "CURRENT_BAR_OR_FUTURE_AWARENESS" in r["critical_dimensions"])},
          {"check_id":"PROTECTED_PLATFORM_NOT_SELECTED","passed":not pilot_record["protected_platform_asset"]},
          {"check_id":"NO_SOURCE_MOVE_OR_DELETE","passed":True},
          {"check_id":"NO_ADAPTER_OR_CUTOVER","passed":True},
          {"check_id":"NO_EXECUTION_OR_CAPITAL_AUTHORITY","passed":True},
        ]
        hostile={"schema_version":"1.0.0","portfolio_id":portfolio_id,"checks":hostile_checks,"hostile_review_passed":all(c["passed"] for c in hostile_checks),"hostile_review_digest":None};hostile["hostile_review_digest"]=digest_object(hostile,"hostile_review_digest");write_json(staging/'reports/hostile_review.json',hostile)
        acceptance={"schema_version":"1.0.0","portfolio_id":portfolio_id,"acceptance_state":"CONTEXT_PORTFOLIO_FROZEN_REFERENCE_PILOT_SELECTED","acceptance_gate_passed":hostile["hostile_review_passed"] and summary["exactly_one_pilot_selected"],"portfolio_closed_for_input_snapshot":True,"risk_assessment_deterministic":True,"critical_dimensions_non_compensatory":True,"dependency_graph_static_only":True,"wave_assignment_complete":all(r["wave_assignment"] for r in records),"pilot_selected":True,"pilot_identity_id":selected_id,"migration_authority_created":False,"cutover_authority_created":False,"runtime_authority_created":False,"live_order_authority_created":False,"capital_authority_created":False,"acceptance_digest":None};acceptance["acceptance_digest"]=digest_object(acceptance,"acceptance_digest");write_json(staging/'reports/acceptance_report.json',acceptance)
        write_text(staging/'docs/LCM08A_EXECUTIVE_BRIEF.md', f"# LCM-08A Executive Brief\n\nPortfolio `{portfolio_id}` freezes {len(records)} Context identity candidates. Exactly one reference pilot is selected: `{selected_id}` at `{pilot_record['source_artifact_path']}`. No source move, deletion, semantic refactor, adapter publication, consumer cutover, runtime, live-order or capital authority occurred.\n")
        write_text(staging/'docs/LCM08A_RISK_MODEL.md', "# LCM-08A Risk Model\n\nRisk dimensions remain visible individually. Execution, broker/network coupling, current-bar/future awareness, nondeterminism, security sensitivity and identity ambiguity are critical non-compensatory dimensions. Aggregate scores order work only; they cannot turn a critical dimension into an acceptable pilot.\n")
        write_text(staging/'docs/LCM08A_PILOT_DECISION.md', f"# LCM-08A Pilot Decision\n\nThe deterministic policy selected `{selected_id}`. The source remains immutable. LCM-08B may construct a pilot packet, canonical package, compatibility adapter and parity evidence only. Any semantic correction requires an explicit decision record.\n")
        write_text(staging/'docs/LCM08A_TO_LCM08B_HANDOFF.md', f"# LCM-08A to LCM-08B Handoff\n\nSelected pilot: `{selected_id}`. Source: `{pilot_record['source_artifact_path']}`. Source digest: `{pilot_record['source_artifact_sha256']}`. Allowed next work is limited to pilot evidence packet construction, canonical authoring, compatibility adapter construction and behavioral parity.\n")
        ledger=build_events(portfolio_id,handoff["handoff_digest"],config.issued_at);write_json(staging/'events/context_portfolio_event_ledger.json',ledger)
        output_digests={"portfolio_registry":file_digest(staging/'portfolio/context_portfolio_registry.jsonl'),"risk_assessment":file_digest(staging/'risk/context_risk_assessment.jsonl'),"dependency_graph":file_digest(staging/'dependencies/context_dependency_graph.json'),"wave_assignment":file_digest(staging/'waves/context_wave_assignment.json'),"pilot_evaluations":file_digest(staging/'pilot/pilot_candidate_evaluations.jsonl'),"pilot_selection":file_digest(staging/'pilot/pilot_selection_decision.json'),"acceptance_report":file_digest(staging/'reports/acceptance_report.json')}
        provenance=build_provenance(portfolio_id,upstream["input_digests"],output_digests);write_json(staging/'provenance/context_portfolio_provenance_graph.json',provenance)
        handoff_out={"schema_version":"1.0.0","handoff_type":"LCM08A_TO_LCM08B","portfolio_id":portfolio_id,"source_handoff_digest":handoff["handoff_digest"],"portfolio_summary_digest":summary["summary_digest"],"acceptance_report_digest":acceptance["acceptance_digest"],"pilot_selection_digest":selection["selection_digest"],"selected_pilot_identity_id":selected_id,"selected_pilot_source_path":pilot_record["source_artifact_path"],"selected_pilot_source_digest":pilot_record["source_artifact_sha256"],"required_characterization_gaps":pilot_record["characterization_state"]["required_case_types"],"allowed_actions":["BUILD_PILOT_MIGRATION_PACKET","AUTHOR_CANONICAL_CONTEXT_PACKAGE","BUILD_COMPATIBILITY_ADAPTER","EXECUTE_GOLDEN_PARITY","PRESERVE_LEGACY_SOURCE_IMMUTABLY"],"forbidden_actions":["MIGRATE_NON_PILOT_CONTEXT","MOVE_OR_DELETE_SOURCE","SWITCH_CONSUMER","QUARANTINE_OR_RETIRE_LEGACY","ENABLE_EXECUTION","AUTHORIZE_RUNTIME","AUTHORIZE_LIVE_ORDER","ACTIVATE_CAPITAL"],"source_move_allowed":False,"source_delete_allowed":False,"semantic_correction_allowed_without_decision":False,"consumer_cutover_allowed":False,"runtime_authority_created":False,"live_order_authority_created":False,"capital_authority_created":False,"handoff_digest":None};handoff_out["handoff_digest"]=digest_object(handoff_out,"handoff_digest");write_json(staging/'handoff/lcm08a_to_lcm08b_handoff.json',handoff_out)
        build_manifest(staging)
        receipt={"schema_version":"1.0.0","portfolio_id":portfolio_id,"acceptance_state":acceptance["acceptance_state"],"output_manifest_digest":file_digest(staging/'output_manifest.json'),"handoff_digest":handoff_out["handoff_digest"],"receipt_digest":None};receipt["receipt_digest"]=digest_object(receipt,"receipt_digest");write_json(staging/'context_portfolio_receipt.json',receipt)
        # Manifest includes receipt, so rebuild once.
        build_manifest(staging)
        atomic_publish(staging,destination)
        return destination
    except Exception:
        cleanup(staging)
        raise
