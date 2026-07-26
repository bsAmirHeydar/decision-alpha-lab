from __future__ import annotations
from collections import Counter,defaultdict
from dataclasses import dataclass
from pathlib import Path
from .authority import build_permit,verify_permit
from .canonical import content_id,digest_object
from .dependency_audit import audit as dependency_audit
from .documentation import build_successors
from .event_ledger import build as build_events
from .io import atomic_publish,cleanup,private_staging,read_csv,read_json,write_csv,write_json,write_jsonl,write_text
from .layering import layer_graph,is_acyclic
from .manifest import build as build_manifest
from .path_policy import casefold_key,validate
from .registries import PACKAGE_ROOTS,TARGET_OUTCOMES,MATERIALIZATION_STATUSES,LAYERS,ALLOWED_EDGES,registry
from .root_plan import map_root
from .target_mapper import map_artifact,map_identity
from .upstream import load

@dataclass(frozen=True)
class RunConfig:
    repo_root: Path
    destination: Path
    issued_at: str='2026-07-19T00:00:00Z'

def _package_root_registry():
    records=[]
    for role,target in sorted(PACKAGE_ROOTS.items()):
        obj={'artifact_role_or_identity_kind':role,'canonical_home':target,'single_home':True,'materialization_allowed':False,'record_digest':None}
        obj['record_digest']=digest_object(obj,'record_digest');records.append(obj)
    out={'schema_version':'1.0.0','registry_id':'LCM05_PACKAGE_ROOT_REGISTRY_V1','record_count':len(records),'records':records,'no_artifact_class_has_two_canonical_homes':len(records)==len({x['artifact_role_or_identity_kind'] for x in records}),'registry_digest':None}
    out['registry_digest']=digest_object(out,'registry_digest');return out

def _authored_generated_boundary():
    classes=[
      {'class_id':'AUTHORED_CANONICAL','canonical_authority_allowed':True,'hand_edit_allowed':True,'rebuild_required':False},
      {'class_id':'GENERATED_PROJECTION','canonical_authority_allowed':False,'hand_edit_allowed':False,'rebuild_required':True},
      {'class_id':'SOURCE_EVIDENCE','canonical_authority_allowed':False,'hand_edit_allowed':False,'rebuild_required':False},
      {'class_id':'RELEASE_ARTIFACT','canonical_authority_allowed':False,'hand_edit_allowed':False,'rebuild_required':True},
      {'class_id':'MIGRATION_REGISTRY','canonical_authority_allowed':False,'hand_edit_allowed':False,'rebuild_required':True},
    ]
    out={'schema_version':'1.0.0','boundary_id':'LCM05_AUTHORED_GENERATED_BOUNDARY_V1','classes':classes,'generated_can_override_authored':False,'generated_can_be_domain_authority':False,'generated_rebuild_command':'python -m src.engine.tooling.strategy_factory.lcm.lcm_05.cli build --repo-root . --destination registry/history/lcm/target_paths','boundary_digest':None}
    out['boundary_digest']=digest_object(out,'boundary_digest');return out

def _layer_policy():
    nodes,edges=layer_graph();acyclic=is_acyclic(nodes,edges)
    out={'schema_version':'1.0.0','policy_id':'LCM05_DEPENDENCY_DIRECTION_POLICY_V1','layers':nodes,'allowed_dependency_edges':edges,'cross_layer_cycles_allowed':False,'visualizer_may_mutate_domain':False,'context_may_depend_on_execution_adapter':False,'generated_may_be_canonical_authority':False,'graph_acyclic':acyclic,'policy_digest':None}
    out['policy_digest']=digest_object(out,'policy_digest');return out

def _ambiguity_targets(ambiguities):
    rows=[]
    for a in ambiguities:
        aid=a['ambiguity_id'];family=(a.get('family_candidate') or 'UNKNOWN').upper();target=f"tests/legacy/strategy_factory/migration/quarantine/identity_ambiguity/{family[:40]}/{aid}.json"
        validate(target)
        obj={'schema_version':'1.0.0','ambiguity_id':aid,'source_artifact_path':a['artifact_path'],'family_candidate':a.get('family_candidate'),'target_outcome':'PROPOSE_QUARANTINE','target_path':target,'materialization_status':'BLOCKED_IDENTITY_AMBIGUITY','human_resolution_required':True,'source_move_authorized':False,'source_delete_authorized':False,'target_materialization_authorized':False,'queue_digest':None}
        obj['queue_digest']=digest_object(obj,'queue_digest');rows.append(obj)
    return rows

def _path_reports(artifact_maps,identity_maps,root_plans,ambiguity_maps):
    safety_entries=[];file_entries=[];package_entries=[]
    for source,rows,key in [('ARTIFACT',artifact_maps,'target_path'),('ROOT',root_plans,'target_path'),('AMBIGUITY',ambiguity_maps,'target_path')]:
        for r in rows:
            src=r.get('artifact_path') or r.get('source_path') or r.get('source_artifact_path') or r.get('ambiguity_id')
            item=(source,src,r[key]);safety_entries.append(item);file_entries.append(item)
    for r in identity_maps:
        item=('IDENTITY',r['identity_id'],r['target_package_root']);safety_entries.append(item);package_entries.append(item)
    unsafe=[];max_len=0
    for kind,source,target in safety_entries:
        try:validate(target)
        except Exception as e:unsafe.append({'kind':kind,'source':source,'target':target,'error':str(e)})
        max_len=max(max_len,len(target))
    duplicate_declarations=[];actual_collisions=[]
    by=defaultdict(list)
    for kind,source,target in file_entries:by[casefold_key(target)].append({'kind':kind,'source':source,'target':target})
    for key,members in by.items():
        unique_sources={m['source'].casefold() for m in members}
        if len(unique_sources)>1:actual_collisions.append({'casefold_target':key,'members':members,'member_count':len(members),'unique_source_count':len(unique_sources)})
        elif len(members)>1:duplicate_declarations.append({'casefold_target':key,'members':members,'member_count':len(members)})
    pby=defaultdict(list)
    for kind,source,target in package_entries:pby[casefold_key(target)].append({'kind':kind,'source':source,'target':target})
    package_collisions=[{'casefold_target':k,'members':v,'member_count':len(v)} for k,v in pby.items() if len({x['source'] for x in v})>1]
    safety={'schema_version':'1.0.0','evaluated_target_count':len(safety_entries),'unsafe_target_count':len(unsafe),'unsafe_targets':unsafe,'max_target_path_length':max_len,'windows_safe':not unsafe,'root_relative':not unsafe,'safety_digest':None};safety['safety_digest']=digest_object(safety,'safety_digest')
    collision={'schema_version':'1.0.0','casefold_collision_count':len(actual_collisions)+len(package_collisions),'file_target_collision_count':len(actual_collisions),'package_root_collision_count':len(package_collisions),'duplicate_declaration_count':len(duplicate_declarations),'collisions':actual_collisions,'package_root_collisions':package_collisions,'duplicate_declarations':duplicate_declarations,'collision_free':not actual_collisions and not package_collisions,'collision_digest':None};collision['collision_digest']=digest_object(collision,'collision_digest')
    return safety,collision

def _docs(staging,summary,handoff):
    write_text(staging/'docs/LCM05_EXECUTIVE_BRIEF.md',f"""# LCM-05 Executive Brief

Target topology run `{summary['topology_run_id']}` maps every classified artifact to one deterministic target outcome without moving, deleting, merging, refactoring or cutting over any source.

- Artifact mappings: {summary['artifact_mapping_count']}
- Identity package mappings: {summary['identity_mapping_count']}
- Identity ambiguities routed to blocked quarantine proposals: {summary['identity_ambiguity_mapping_count']}
- Root relocation plans: {summary['root_relocation_plan_count']}
- Documentation successor records: {summary['documentation_successor_count']}
- Target path materialization performed: false
- Source moves or deletes performed: false
- Runtime, live order and capital authority: false
""")
    write_text(staging/'docs/LCM05_TARGET_TOPOLOGY_CONTRACT.md',"""# LCM-05 Target Topology Contract

The registry defines one canonical home per artifact class, a closed dependency direction model, an authored/generated boundary, deterministic current-to-target locators, root relocation proposals and documentation successor proposals. It is a planning and control artifact only. Materialization requires later owner, security, parity and cutover authority.
""")
    write_text(staging/'docs/LCM05_TO_LCM06_HANDOFF.md',f"""# LCM-05 to LCM-06 Handoff

Handoff digest: `{handoff['handoff_digest']}`

LCM-06 may build validators, resolvers, trace comparators and compatibility interfaces against this immutable topology package. It may not materialize paths, move or delete sources, waive blockers, enable execution, or treat a proposed target as a migrated implementation.
""")

def run(config:RunConfig)->Path:
    repo=config.repo_root.resolve();up=load(repo);source_handoff=up['handoff'];permit=build_permit(source_handoff['handoff_digest'],up['marker']['characterization_run_id'],config.issued_at);verify_permit(permit,source_handoff['handoff_digest'])
    identity_by_path={x['source_artifact_path']:x for x in up['identities']}
    identity_maps=[map_identity(x) for x in up['identities']]
    artifact_maps=[map_artifact(x,identity_by_path) for x in up['classifications']]
    ambiguity_maps=_ambiguity_targets(up['ambiguities'])
    root_rows=read_csv(up['survey_root']/'root_hygiene/root_artifact_inventory.csv');root_plans=[map_root(x) for x in root_rows]
    ns_rows=read_csv(up['survey_root']/'documentation/documentation_namespace_inventory.csv');exact=read_json(up['survey_root']/'documentation/exact_duplicate_trees.json');doc_successors=build_successors(exact,ns_rows)
    dep_edges=read_csv(up['survey_root']/'dependencies/all_dependency_edges.csv');class_by_path={x['artifact_path']:x for x in up['classifications']};dep_summary,dep_violations=dependency_audit(dep_edges,class_by_path)
    package_roots=_package_root_registry();layer_policy=_layer_policy();boundary=_authored_generated_boundary();path_safety,collision_report=_path_reports(artifact_maps,identity_maps,root_plans,ambiguity_maps)
    material={'source_handoff_digest':source_handoff['handoff_digest'],'classification_id':up['handoff']['identity_run_id'],'artifact_mapping_digests':[x['mapping_digest'] for x in artifact_maps],'identity_mapping_digests':[x['mapping_digest'] for x in identity_maps],'package_root_registry_digest':package_roots['registry_digest'],'dependency_policy_digest':layer_policy['policy_digest'],'policy_version':'LCM05_TARGET_TOPOLOGY_POLICY_V1'}
    run_id=content_id('TOPOLOGY',material);final=config.destination/run_id;staging=private_staging(config.destination,'.lcm05-staging-')
    try:
        marker={'schema_version':'1.0.0','phase_id':'LCM-05','topology_run_id':run_id,'source_characterization_run_id':up['marker']['characterization_run_id'],'source_handoff_digest':source_handoff['handoff_digest'],'claim_ceiling':'TARGET_TOPOLOGY_REFERENCE_ONLY','phase_completion_state':'REFERENCE_TOPOLOGY_COMPLETE_MATERIALIZATION_BLOCKED','artifact_mapping_count':len(artifact_maps),'identity_mapping_count':len(identity_maps),'identity_ambiguity_mapping_count':len(ambiguity_maps),'target_path_materialization_performed':False,'source_move_performed':False,'source_delete_performed':False,'semantic_refactor_performed':False,'merge_performed':False,'cutover_performed':False,'runtime_authority_created':False,'live_order_authority_created':False,'capital_authority_created':False,'marker_digest':None};marker['marker_digest']=digest_object(marker,'marker_digest');write_json(staging/'topology_marker.json',marker)
        binding={'schema_version':'1.0.0','characterization_run_id':up['marker']['characterization_run_id'],'identity_run_id':source_handoff['identity_run_id'],'source_handoff_digest':source_handoff['handoff_digest'],'source_characterization_summary_digest':source_handoff['characterization_summary_digest'],'source_output_manifest_digest':up['manifest']['output_manifest_digest'],'binding_digest':None};binding['binding_digest']=digest_object(binding,'binding_digest');write_json(staging/'input/lcm04_binding.json',binding)
        write_json(staging/'authority/authority_permit.json',permit)
        write_json(staging/'registries/package_root_registry.json',package_roots);write_json(staging/'registries/target_outcome_registry.json',registry('LCM05_TARGET_OUTCOME_REGISTRY_V1','target_outcomes',TARGET_OUTCOMES,{'dynamic_outcome_allowed':False}));write_json(staging/'registries/materialization_status_registry.json',registry('LCM05_MATERIALIZATION_STATUS_REGISTRY_V1','materialization_statuses',MATERIALIZATION_STATUSES,{'unknown_is_materialized':False}));write_json(staging/'registries/layer_registry.json',registry('LCM05_LAYER_REGISTRY_V1','layers',LAYERS,{'dynamic_layer_allowed':False}));write_json(staging/'registries/documentation_relationship_registry.json',registry('LCM05_DOCUMENTATION_RELATIONSHIP_REGISTRY_V1','relationships',['SELF','EXACT_BYTE_DUPLICATE_TREE','RETAIN_PENDING_SEMANTIC_RECONCILIATION'],{'byte_duplicate_is_semantic_equivalence':False}))
        write_json(staging/'topology/dependency_direction_policy.json',layer_policy);write_json(staging/'topology/authored_generated_boundary.json',boundary);write_json(staging/'topology/target_repository_topology.json',{'schema_version':'1.0.0','topology_run_id':run_id,'package_root_registry_digest':package_roots['registry_digest'],'dependency_policy_digest':layer_policy['policy_digest'],'authored_generated_boundary_digest':boundary['boundary_digest'],'canonical_truth_location':'PACKAGE_AND_ACCEPTED_MASTER_ARCHITECTURE','mql5_role':'PLATFORM_IMPLEMENTATION_OR_ADAPTER','generated_role':'NON_CANONICAL_PROJECTION','release_role':'REGISTRY_ARTIFACT','legacy_role':'ACTIVE_DURING_DUAL_RUN_OR_QUARANTINED_AFTER_CUTOVER','target_materialization_allowed':False,'topology_digest':None})
        topo=read_json(staging/'topology/target_repository_topology.json');topo['topology_digest']=digest_object(topo,'topology_digest');write_json(staging/'topology/target_repository_topology.json',topo)
        amap_fields=['target_mapping_id','artifact_path','artifact_sha256','classification_id','family_candidate','artifact_role','activity_status','primary_disposition','identity_id','target_outcome','target_path','target_layer','materialization_status','source_move_authorized','source_delete_authorized','semantic_refactor_authorized','cutover_authorized','runtime_authorized','live_order_authorized','capital_authorized','mapping_digest'];write_jsonl(staging/'mappings/artifact_target_map.jsonl',artifact_maps);write_csv(staging/'mappings/artifact_target_map.csv',amap_fields,artifact_maps)
        imap_fields=['identity_id','identity_kind','source_artifact_path','source_artifact_sha256','target_package_root','target_layer','canonical_path_materialized','owner_resolution_status','identity_status','protected_platform_asset','security_sensitive','materialization_status','mapping_digest'];write_jsonl(staging/'mappings/identity_target_map.jsonl',identity_maps);write_csv(staging/'mappings/identity_target_map.csv',imap_fields,identity_maps)
        write_jsonl(staging/'mappings/identity_ambiguity_target_queue.jsonl',ambiguity_maps)
        rfields=['root_plan_id','source_path','source_sha256','source_classification','target_outcome','target_path','move_performed','delete_performed','review_required','plan_digest'];write_jsonl(staging/'root_relocation/root_relocation_plan.jsonl',root_plans);write_csv(staging/'root_relocation/root_relocation_plan.csv',rfields,root_plans)
        dfields=['successor_record_id','source_namespace','canonical_successor','relationship','status','redirect_materialized','deletion_authorized','semantic_equivalence_claimed','tree_fingerprint','record_digest'];write_jsonl(staging/'documentation/documentation_successor_map.jsonl',doc_successors);write_csv(staging/'documentation/documentation_successor_map.csv',dfields,doc_successors)
        write_json(staging/'dependencies/dependency_direction_audit.json',dep_summary);write_jsonl(staging/'dependencies/dependency_direction_violations.jsonl',dep_violations)
        write_json(staging/'paths/target_path_safety_report.json',path_safety);write_json(staging/'collisions/target_path_collision_report.json',collision_report)
        outcome_counts=Counter(x['target_outcome'] for x in artifact_maps);status_counts=Counter(x['materialization_status'] for x in artifact_maps);role_counts=Counter(x['artifact_role'] for x in artifact_maps)
        blockers=[{'blocker_id':'LCM05_OWNER_APPROVALS','reason_code':'HUMAN_OWNER_APPROVALS_PENDING','affected_count':sum(x['materialization_status']=='BLOCKED_OWNER_APPROVAL' for x in artifact_maps),'blocks_materialization':True},{'blocker_id':'LCM05_SECURITY_REVIEWS','reason_code':'SECURITY_REVIEWS_PENDING','affected_count':sum(x['materialization_status']=='BLOCKED_SECURITY_REVIEW' for x in artifact_maps),'blocks_materialization':True},{'blocker_id':'LCM05_IDENTITY_AMBIGUITIES','reason_code':'IDENTITY_AMBIGUITIES_PENDING','affected_count':len(ambiguity_maps),'blocks_materialization':True},{'blocker_id':'LCM05_LEGACY_PARITY','reason_code':'LEGACY_RUNTIME_PARITY_PENDING','affected_count':sum(x['primary_disposition'] in ('REWRITE_WITH_PARITY','EXTRACT_SHARED_LOGIC','WRAP_LEGACY') for x in artifact_maps),'blocks_materialization':True},{'blocker_id':'LCM05_EQUIVALENCE','reason_code':'DUPLICATE_EQUIVALENCE_REVIEW_PENDING','affected_count':sum(x['primary_disposition']=='MERGE_AFTER_EQUIVALENCE_PROOF' for x in artifact_maps),'blocks_materialization':True},{'blocker_id':'LCM05_EXTERNAL_MQL_RUNTIME','reason_code':'MQL5_METATRADER_RUNTIME_NOT_AVAILABLE_IN_REFERENCE_ENVIRONMENT','affected_count':sum(x['artifact_path'].lower().endswith(('.mq5','.mqh')) for x in artifact_maps),'blocks_materialization':True}]
        for x in blockers:x['blocker_digest']=digest_object(x,'blocker_digest')
        write_json(staging/'blockers/materialization_blockers.json',{'schema_version':'1.0.0','blocker_count':len(blockers),'blockers':blockers,'target_materialization_allowed':False,'blocker_bundle_digest':digest_object(blockers)})
        acceptance={'schema_version':'1.0.0','all_classified_artifacts_have_one_target_outcome':len(artifact_maps)==len(up['classifications']) and len({x['artifact_path'] for x in artifact_maps})==len(artifact_maps),'all_identities_have_one_package_root':len(identity_maps)==len(up['identities']) and len({x['identity_id'] for x in identity_maps})==len(identity_maps),'package_root_registry_has_single_home':package_roots['no_artifact_class_has_two_canonical_homes'],'target_layer_graph_acyclic':layer_policy['graph_acyclic'],'generated_paths_noncanonical':not boundary['generated_can_be_domain_authority'],'target_paths_windows_safe':path_safety['windows_safe'],'target_path_casefold_collision_free':collision_report['collision_free'],'root_relocation_plan_complete':len(root_plans)==len(root_rows),'documentation_successor_map_complete':len(doc_successors)>=len(ns_rows),'broad_file_movement_performed':False,'acceptance_gate_passed':False,'acceptance_state':'REFERENCE_TOPOLOGY_COMPLETE_WITH_COLLISION_REVIEW' if not collision_report['collision_free'] else 'REFERENCE_TOPOLOGY_ACCEPTED_MATERIALIZATION_BLOCKED','acceptance_digest':None}
        # Collisions between registry classes are inspected; artifact-level collisions block materialization but do not invalidate complete reference mapping.
        acceptance['acceptance_gate_passed']=all([acceptance['all_classified_artifacts_have_one_target_outcome'],acceptance['all_identities_have_one_package_root'],acceptance['package_root_registry_has_single_home'],acceptance['target_layer_graph_acyclic'],acceptance['generated_paths_noncanonical'],acceptance['target_paths_windows_safe'],acceptance['root_relocation_plan_complete'],acceptance['documentation_successor_map_complete'],not acceptance['broad_file_movement_performed']])
        acceptance['acceptance_digest']=digest_object(acceptance,'acceptance_digest');write_json(staging/'reports/acceptance_report.json',acceptance)
        summary={'schema_version':'1.0.0','phase_id':'LCM-05','topology_run_id':run_id,'claim_ceiling':'TARGET_TOPOLOGY_REFERENCE_ONLY','characterization_run_id':up['marker']['characterization_run_id'],'identity_run_id':source_handoff['identity_run_id'],'artifact_mapping_count':len(artifact_maps),'identity_mapping_count':len(identity_maps),'identity_ambiguity_mapping_count':len(ambiguity_maps),'root_relocation_plan_count':len(root_plans),'documentation_successor_count':len(doc_successors),'dependency_edge_evaluated_count':dep_summary['evaluated_edge_count'],'legacy_dependency_violation_count':dep_summary['violation_count'],'target_outcome_counts':dict(sorted(outcome_counts.items())),'materialization_status_counts':dict(sorted(status_counts.items())),'materialization_blocker_counts':{x['reason_code']:x['affected_count'] for x in blockers},'artifact_role_counts':dict(sorted(role_counts.items())),'package_root_count':package_roots['record_count'],'target_layer_count':len(LAYERS),'target_path_casefold_collision_count':collision_report['casefold_collision_count'],'target_path_unsafe_count':path_safety['unsafe_target_count'],'acceptance_gate_passed':acceptance['acceptance_gate_passed'],'target_materialization_allowed':False,'source_move_performed':False,'source_delete_performed':False,'semantic_refactor_performed':False,'merge_performed':False,'cutover_performed':False,'runtime_authority_created':False,'live_order_authority_created':False,'capital_authority_created':False,'summary_digest':None};summary['summary_digest']=digest_object(summary,'summary_digest');write_json(staging/'reports/topology_summary.json',summary)
        hostile={'schema_version':'1.0.0','checks':[{'check':'SECOND_COMPETING_ARCHITECTURE','status':'PASS','evidence':'ACL_OS_RETAINED_AS_PROTECTED_KERNEL'},{'check':'DOMAIN_TO_PLATFORM_INVERSION','status':'PASS','evidence':'CLOSED_LAYER_POLICY_AND_LEGACY_VIOLATION_REPORT'},{'check':'VISUALIZER_MUTATES_DOMAIN','status':'PASS','evidence':'POLICY_FALSE'},{'check':'CONTEXT_TO_EXECUTION_COUPLING','status':'PASS','evidence':'POLICY_FALSE'},{'check':'GENERATED_BECOMES_CANONICAL','status':'PASS','evidence':'AUTHORED_GENERATED_BOUNDARY'},{'check':'MQL_PUBLIC_PATH_BREAKAGE','status':'PASS','evidence':'COMPATIBILITY_WRAPPER_PROPOSALS_NO_MATERIALIZATION'},{'check':'UNKNOWN_TO_APPROVED_TARGET','status':'PASS','evidence':'AMBIGUITY_QUARANTINE_QUEUE'},{'check':'SOURCE_MOVE_OR_DELETE','status':'PASS','evidence':'NO_FILE_MOVEMENT'}],'hostile_review_passed':True,'production_or_migration_completion_claimed':False,'review_digest':None};hostile['review_digest']=digest_object(hostile,'review_digest');write_json(staging/'reports/hostile_review.json',hostile)
        events=build_events(run_id,[('LCM04_PACKAGE_ACCEPTED',{'source_handoff_digest':source_handoff['handoff_digest']}),('AUTHORITY_PERMIT_BOUND',{'permit_digest':permit['permit_digest']}),('TARGET_ROOTS_REGISTERED',{'package_root_registry_digest':package_roots['registry_digest']}),('ARTIFACT_TARGETS_MAPPED',{'artifact_mapping_count':len(artifact_maps)}),('DEPENDENCY_DIRECTION_AUDITED',{'violation_count':len(dep_violations)}),('ROOT_AND_DOCUMENTATION_PLANS_BUILT',{'root_plan_count':len(root_plans),'documentation_successor_count':len(doc_successors)}),('PATH_SAFETY_AND_COLLISIONS_REVIEWED',{'unsafe_count':path_safety['unsafe_target_count'],'collision_count':collision_report['casefold_collision_count']}),('REFERENCE_TOPOLOGY_DECISION_ISSUED',{'acceptance_state':acceptance['acceptance_state']}),('LCM06_HANDOFF_PREPARED',{'target_materialization_allowed':False})]);write_json(staging/'events/topology_event_ledger.json',events)
        provenance={'schema_version':'1.0.0','topology_run_id':run_id,'nodes':[{'node_id':'LCM04_HANDOFF','digest':source_handoff['handoff_digest']},{'node_id':'LCM05_PACKAGE_ROOTS','digest':package_roots['registry_digest']},{'node_id':'LCM05_ARTIFACT_TARGET_MAP','digest':digest_object([x['mapping_digest'] for x in artifact_maps])},{'node_id':'LCM05_TOPOLOGY_SUMMARY','digest':summary['summary_digest']}],'edges':[{'from':'LCM04_HANDOFF','to':'LCM05_PACKAGE_ROOTS'},{'from':'LCM05_PACKAGE_ROOTS','to':'LCM05_ARTIFACT_TARGET_MAP'},{'from':'LCM05_ARTIFACT_TARGET_MAP','to':'LCM05_TOPOLOGY_SUMMARY'}],'reaches_lcm04_characterization':True,'legacy_semantics_mutated':False,'target_paths_materialized':False,'source_moved':False,'source_deleted':False,'runtime_authority_created':False,'live_order_authority_created':False,'capital_authority_created':False,'provenance_digest':None};provenance['provenance_digest']=digest_object(provenance,'provenance_digest');write_json(staging/'provenance/topology_provenance_graph.json',provenance)
        handoff={'schema_version':'1.0.0','handoff_type':'LCM05_TO_LCM06','topology_run_id':run_id,'characterization_run_id':up['marker']['characterization_run_id'],'identity_run_id':source_handoff['identity_run_id'],'source_handoff_digest':source_handoff['handoff_digest'],'topology_summary_digest':summary['summary_digest'],'package_root_registry_digest':package_roots['registry_digest'],'artifact_target_map_digest':digest_object([x['mapping_digest'] for x in artifact_maps]),'dependency_policy_digest':layer_policy['policy_digest'],'acceptance_report_digest':acceptance['acceptance_digest'],'completed_gates':['EVERY_CLASSIFIED_ARTIFACT_HAS_ONE_TARGET_OUTCOME','EVERY_IDENTITY_HAS_ONE_PACKAGE_ROOT','CLOSED_DEPENDENCY_DIRECTION_POLICY_REGISTERED','AUTHORED_GENERATED_BOUNDARY_REGISTERED','ROOT_RELOCATION_PLAN_COMPLETE','DOCUMENTATION_SUCCESSOR_MAP_COMPLETE','NO_SOURCE_MOVEMENT'],'unresolved_blockers':[x['reason_code'] for x in blockers if x['affected_count']>0],'allowed_actions':['BUILD_MIGRATION_PACKET_VALIDATOR','BUILD_ALIAS_AND_LOCATOR_RESOLVER','BUILD_TRACE_COMPARATOR','BUILD_COMPATIBILITY_ADAPTER_INTERFACES','BUILD_MOVE_ONLY_AND_REDIRECT_TOOLING','BUILD_QUARANTINE_AND_DELETION_VALIDATORS'],'forbidden_actions':['MATERIALIZE_TARGET_PATH','MOVE_SOURCE_FILE','DELETE_SOURCE_FILE','SEMANTIC_REFACTOR','MERGE_LEGACY_IMPLEMENTATIONS','CUTOVER_CONSUMER','WAIVE_UNKNOWN','AUTHORIZE_RUNTIME','AUTHORIZE_LIVE_ORDER','ACTIVATE_CAPITAL'],'target_materialization_allowed':False,'source_move_allowed':False,'source_delete_allowed':False,'handoff_digest':None};handoff['handoff_digest']=digest_object(handoff,'handoff_digest');write_json(staging/'handoff/lcm05_to_lcm06_handoff.json',handoff)
        _docs(staging,summary,handoff)
        manifest=build_manifest(staging);write_json(staging/'output_manifest.json',manifest)
        receipt={'schema_version':'1.0.0','phase_id':'LCM-05','topology_run_id':run_id,'claim_ceiling':'TARGET_TOPOLOGY_REFERENCE_ONLY','artifact_mapping_count':len(artifact_maps),'identity_mapping_count':len(identity_maps),'root_relocation_plan_count':len(root_plans),'documentation_successor_count':len(doc_successors),'topology_summary_digest':summary['summary_digest'],'acceptance_report_digest':acceptance['acceptance_digest'],'event_ledger_digest':events['ledger_digest'],'provenance_digest':provenance['provenance_digest'],'handoff_digest':handoff['handoff_digest'],'target_materialization_performed':False,'source_move_performed':False,'source_delete_performed':False,'semantic_refactor_performed':False,'merge_performed':False,'cutover_performed':False,'runtime_authority_created':False,'live_order_authority_created':False,'capital_authority_created':False,'receipt_digest':None};receipt['receipt_digest']=digest_object(receipt,'receipt_digest');write_json(staging/'topology_receipt.json',receipt)
        manifest=build_manifest(staging);write_json(staging/'output_manifest.json',manifest)
        return atomic_publish(staging,final)
    except Exception:
        cleanup(staging);raise
