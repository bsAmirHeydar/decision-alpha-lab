from __future__ import annotations
import csv,json
from collections import Counter,defaultdict
from dataclasses import dataclass
from pathlib import Path
from .authority import build_permit,verify_permit
from .canonical import content_id,digest_object,sha256_file
from .classifier import classify
from .event_ledger import build as build_events
from .io import atomic_publish,private_staging,read_json,write_csv,write_json,write_jsonl,write_text
from .manifest import build as build_manifest
from .ownership import family_roles
from .reports import summarize,family_rows
from .upstream import latest_survey,verify_survey

@dataclass(frozen=True)
class RunConfig:
    repo_root: Path
    destination: Path
    issued_at: str='2026-07-18T00:00:00Z'

def _read_csv(path):
    with path.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
def _load_caps(survey):
    d=defaultdict(set)
    for r in _read_csv(survey/'capabilities/capability_findings.csv'):d[r['path']].add(r['capability_kind'])
    return d
def _load_entry(survey): return {r['path'] for r in _read_csv(survey/'dependencies/entry_points.csv')}
def _load_inbound(survey):
    c=Counter()
    for r in _read_csv(survey/'dependencies/all_dependency_edges.csv'):
        if r['resolution_status']=='RESOLVED_INTERNAL' and r['resolved_path']:c[r['resolved_path']]+=1
    return c
def _load_dup(survey):
    x=read_json(survey/'duplicates/exact_file_duplicate_groups.json'); return {p for g in x.get('groups',[]) for p in g.get('paths',[])}
def _unresolved(records):
    queues=defaultdict(list)
    for r in records:
        base={'classification_id':r['classification_id'],'artifact_path':r['artifact_path'],'family_candidate':r['family_candidate'],'artifact_role':r['artifact_role'],'activity_status':r['activity_status'],'primary_disposition':r['primary_disposition'],'blocking_reasons':r['blocking_reasons'],'source_digest':r['classification_digest']}
        if 'SEMANTIC_ROLE_UNRESOLVED' in r['blocking_reasons']: queues['ambiguous_role'].append({**base,'queue_reason':'SEMANTIC_ROLE_UNRESOLVED'})
        if any('OWNER' in x for x in r['blocking_reasons']): queues['owner'].append({**base,'queue_reason':'HUMAN_OWNER_APPROVAL_PENDING'})
        if r['security_sensitive']: queues['security'].append({**base,'queue_reason':'SECURITY_REVIEW_REQUIRED','authority_surfaces':r['authority_surfaces'],'capability_kinds':r['capability_kinds']})
        if r['duplicate_member']: queues['duplicate'].append({**base,'queue_reason':'DUPLICATE_EQUIVALENCE_REVIEW_REQUIRED'})
        if r['artifact_role']=='GENERATED_PROJECTION': queues['generated_projection'].append({**base,'queue_reason':'GENERATED_PROJECTION_NON_CANONICAL'})
        if r['activity_status']=='UNKNOWN_ACTIVITY': queues['activity'].append({**base,'queue_reason':'ACTIVITY_UNRESOLVED'})
    return queues

def run_classification(config: RunConfig) -> Path:
    repo=config.repo_root.resolve(); survey=latest_survey(repo); upstream=verify_survey(survey)
    permit=build_permit(upstream['handoff']['handoff_digest'],upstream['survey_id'],config.issued_at); verify_permit(permit,upstream['handoff']['handoff_digest'])
    rows=_read_csv(survey/'inventory/artifact_inventory.csv'); caps=_load_caps(survey); entry=_load_entry(survey); inbound=_load_inbound(survey); dup=_load_dup(survey)
    records=[classify(r,caps.get(r['path'],set()),entry,inbound.get(r['path'],0),r['path'] in dup) for r in rows]
    material={'survey_id':upstream['survey_id'],'source_handoff_digest':upstream['handoff']['handoff_digest'],'policy_version':'LCM02_CLASSIFICATION_POLICY_V1','record_digests':[r['classification_digest'] for r in records]}
    cid=content_id('CLASSIFICATION',material); final=config.destination/cid; staging=private_staging(config.destination,'.lcm02-staging-')
    try:
        write_json(staging/'classification_marker.json',{'schema_version':'1.0.0','phase_id':'LCM-02','classification_id':cid,'claim_ceiling':'CLASSIFICATION_AND_OWNERSHIP_REFERENCE_ONLY','source_move_performed':False,'source_delete_performed':False,'semantic_refactor_performed':False,'marker_digest':None})
        marker=read_json(staging/'classification_marker.json'); marker['marker_digest']=digest_object(marker,'marker_digest'); write_json(staging/'classification_marker.json',marker)
        write_json(staging/'input/lcm01_binding.json',{'schema_version':'1.0.0','survey_id':upstream['survey_id'],'source_handoff_digest':upstream['handoff']['handoff_digest'],'source_summary_digest':upstream['summary']['summary_digest'],'source_output_manifest_digest':upstream['manifest']['output_manifest_digest'],'binding_digest':None}); b=read_json(staging/'input/lcm01_binding.json'); b['binding_digest']=digest_object(b,'binding_digest'); write_json(staging/'input/lcm01_binding.json',b)
        write_json(staging/'authority/authority_permit.json',permit)
        families=sorted({r['family_candidate'] for r in records}); ownerreg=family_roles(families); write_json(staging/'owners/owner_role_registry.json',ownerreg)
        role_registry={'schema_version':'1.0.0','registry_id':'LCM02_ARTIFACT_ROLE_REGISTRY_V1','closed':True,'roles':['CONTEXT','SETUP','TREATMENT','VISUALIZER','PLATFORM_ADAPTER','EXECUTION_ADAPTER','SHARED_PRIMITIVE','RESEARCH','DIAGNOSTIC','PLATFORM_KERNEL','GENERATED_PROJECTION','SOURCE_EVIDENCE','RELEASE_METADATA','GOVERNANCE_CONTROL','CONFIGURATION_CONTRACT','TEST_FIXTURE','TEST_CODE','DOCUMENTATION','ARCHIVE','UNKNOWN_ROLE'],'generated_projection_may_be_canonical_doctrine':False}; role_registry['registry_digest']=digest_object(role_registry,'registry_digest')
        disp_registry={'schema_version':'1.0.0','registry_id':'LCM02_PRIMARY_DISPOSITION_REGISTRY_V1','closed':True,'dispositions':['KEEP_CANONICAL','MOVE_WITHOUT_SEMANTIC_CHANGE','WRAP_LEGACY','REWRITE_WITH_PARITY','EXTRACT_SHARED_LOGIC','MERGE_AFTER_EQUIVALENCE_PROOF','ARCHIVE_REFERENCE_ONLY','QUARANTINE_UNCERTAIN','DELETE_AFTER_PROOF','SECURITY_RESTRICTED'],'exactly_one_primary_required':True,'disposition_is_execution_authority':False}; disp_registry['registry_digest']=digest_object(disp_registry,'registry_digest')
        activity_registry={'schema_version':'1.0.0','registry_id':'LCM02_ACTIVITY_STATUS_REGISTRY_V1','closed':True,'statuses':['ACTIVE_PLATFORM','ACTIVE_RUNTIME_CANDIDATE','ACTIVE_RESEARCH','TEST_ONLY','DOCUMENTATION_ONLY','GENERATED','ARCHIVED','RELEASE_HISTORY','CONFIGURATION','UNKNOWN_ACTIVITY'],'unknown_is_delete_authority':False}; activity_registry['registry_digest']=digest_object(activity_registry,'registry_digest')
        surface_registry={'schema_version':'1.0.0','registry_id':'LCM02_AUTHORITY_SURFACE_REGISTRY_V1','closed':True,'surfaces':['ORDER_REQUEST','CAPITAL','BROKER_STATE','FILE_PERSISTENCE','NETWORK_EGRESS','EXTERNAL_MODEL','DYNAMIC_CODE','GLOBAL_STATE','CHART_STATE','TIME_SEMANTICS'],'capability_hit_is_live_authority':False}; surface_registry['registry_digest']=digest_object(surface_registry,'registry_digest')
        for name,obj in [('artifact_role_registry.json',role_registry),('primary_disposition_registry.json',disp_registry),('activity_status_registry.json',activity_registry),('authority_surface_registry.json',surface_registry)]:write_json(staging/'registries'/name,obj)
        fields=['classification_id','artifact_path','artifact_sha256','source_layer_id','family_candidate','family_confidence_bps','artifact_role','role_confidence_bps','role_evidence_codes','activity_status','activity_confidence_bps','activity_evidence_codes','primary_disposition','disposition_evidence_codes','protected_platform_asset','canonical_selection_status','generated_projection_canonical_authority','duplicate_member','capability_kinds','authority_surfaces','security_sensitive','authority_is_risk_indicator_only','live_authority_inferred','semantic_owner_role','code_owner_role','documentation_owner_role','security_reviewer_role','owner_resolution_status','ownership_is_human_approved','ownership_blockers','blocking_reasons','source_move_authorized','source_delete_authorized','semantic_refactor_authorized','merge_authorized','cutover_authorized','runtime_authorized','live_order_authorized','capital_authorized','classification_is_domain_semantic_approval','classification_digest']
        write_csv(staging/'artifacts/artifact_classification_records.csv',fields,records); write_jsonl(staging/'artifacts/artifact_classification_records.jsonl',records)
        summary=summarize(records); summary.update({'schema_version':'1.0.0','phase_id':'LCM-02','classification_id':cid,'survey_id':upstream['survey_id'],'claim_ceiling':'CLASSIFICATION_AND_OWNERSHIP_REFERENCE_ONLY','artifact_count':len(records),'all_artifacts_have_exactly_one_primary_disposition':all(r['primary_disposition'] for r in records),'all_active_candidates_role_bound_or_blocked':all(r['semantic_owner_role'] or r['blocking_reasons'] for r in records if r['activity_status'] in {'ACTIVE_PLATFORM','ACTIVE_RUNTIME_CANDIDATE','ACTIVE_RESEARCH'}),'generated_projection_canonical_count':sum(r['artifact_role']=='GENERATED_PROJECTION' and r['generated_projection_canonical_authority'] for r in records),'platform_kernel_domain_migration_authorized_count':sum(r['protected_platform_asset'] and r['source_move_authorized'] for r in records),'source_move_performed':False,'source_delete_performed':False,'semantic_refactor_performed':False,'human_ownership_approvals_complete':False}); summary['summary_digest']=digest_object(summary,'summary_digest'); write_json(staging/'reports/classification_summary.json',summary)
        famrows=family_rows(records); write_json(staging/'families/family_classification_summary.json',{'schema_version':'1.0.0','classification_id':cid,'families':famrows,'family_count':len(famrows),'human_owner_approval_complete':False,'summary_digest':None}); fobj=read_json(staging/'families/family_classification_summary.json'); fobj['summary_digest']=digest_object(fobj,'summary_digest'); write_json(staging/'families/family_classification_summary.json',fobj)
        write_csv(staging/'families/family_classification_summary.csv',['family','artifact_count','role_counts','disposition_counts','activity_counts','security_sensitive_count','protected_platform_count','unknown_role_count','human_owner_approval_complete'],famrows)
        protected=[r for r in records if r['protected_platform_asset']]; write_csv(staging/'protection/protected_platform_assets.csv',['classification_id','artifact_path','artifact_sha256','family_candidate','artifact_role','primary_disposition','canonical_selection_status','source_move_authorized','source_delete_authorized'],protected)
        preport={'schema_version':'1.0.0','classification_id':cid,'protected_asset_count':len(protected),'domain_migration_authorized_count':sum(r['source_move_authorized'] for r in protected),'delete_authorized_count':sum(r['source_delete_authorized'] for r in protected),'all_protected':all(r['primary_disposition']=='KEEP_CANONICAL' or r['primary_disposition']=='SECURITY_RESTRICTED' for r in protected)}; preport['report_digest']=digest_object(preport,'report_digest'); write_json(staging/'protection/protected_platform_report.json',preport)
        auth=[{'classification_id':r['classification_id'],'artifact_path':r['artifact_path'],'authority_surfaces':r['authority_surfaces'],'capability_kinds':r['capability_kinds'],'security_sensitive':r['security_sensitive'],'primary_disposition':r['primary_disposition'],'security_reviewer_role':r['security_reviewer_role'],'security_review_status':'PENDING_HUMAN_REVIEW' if r['security_sensitive'] else 'NOT_REQUIRED_BY_STATIC_POLICY','risk_indicator_only':True,'live_authority_inferred':False,'runtime_authorized':False,'live_order_authorized':False,'capital_authorized':False,'record_digest':digest_object({'path':r['artifact_path'],'surfaces':r['authority_surfaces'],'caps':r['capability_kinds']})} for r in records if r['authority_surfaces']]
        write_csv(staging/'authority/authority_boundary_records.csv',['classification_id','artifact_path','authority_surfaces','capability_kinds','security_sensitive','primary_disposition','security_reviewer_role','security_review_status','risk_indicator_only','live_authority_inferred','runtime_authorized','live_order_authorized','capital_authorized','record_digest'],auth); write_jsonl(staging/'authority/authority_boundary_records.jsonl',auth)
        sec=[a for a in auth if a['security_sensitive']]; write_csv(staging/'authority/security_sensitive_paths.csv',['classification_id','artifact_path','authority_surfaces','capability_kinds','primary_disposition','security_reviewer_role','security_review_status','record_digest'],sec)
        queues=_unresolved(records)
        for name,items in queues.items():write_jsonl(staging/f'unresolved/{name}_queue.jsonl',items)
        unresolved={'schema_version':'1.0.0','classification_id':cid,'queue_counts':{k:len(v) for k,v in sorted(queues.items())},'unknown_is_not_pass':True,'unknown_is_not_delete_authority':True,'human_resolution_required':True}; unresolved['summary_digest']=digest_object(unresolved,'summary_digest'); write_json(staging/'unresolved/unresolved_summary.json',unresolved)
        dup_report={'schema_version':'1.0.0','classification_id':cid,'exact_duplicate_member_count':sum(r['duplicate_member'] for r in records),'merge_authorized_count':sum(r['duplicate_member'] and r['merge_authorized'] for r in records),'delete_authorized_count':sum(r['duplicate_member'] and r['source_delete_authorized'] for r in records),'equivalence_review_required':True}; dup_report['report_digest']=digest_object(dup_report,'report_digest'); write_json(staging/'duplicates/exact_duplicate_disposition_report.json',dup_report)
        docs={
          'LCM02_EXECUTIVE_BRIEF.md':f'''---
title: "LCM-02 Executive Brief"
status: reference-restricted
classification_id: {cid}
---
# LCM-02 Executive Brief

LCM-02 classified every LCM-01 surveyed artifact into a closed role, activity status and exactly one primary migration disposition. Role binding is governance metadata, not approval of domain semantics. Human ownership assignments remain pending and therefore block destructive action, semantic acceptance and cutover.

No source file was moved, deleted, merged, rewritten or promoted. Generated projections carry no canonical doctrine authority. Security-sensitive artifacts are isolated behind `SECURITY_RESTRICTED` and require an independent security reviewer.
''',
          'LCM02_CLASSIFICATION_METHOD.md':'''---
title: "LCM-02 Classification Method"
status: reference-restricted
---
# Classification Method

Classification uses only LCM-01 evidence: normalized paths, source layer, family candidates, media/language classification, entry-point evidence, resolved inbound dependency edges, exact-byte duplicate membership and static capability findings. It does not infer market truth, behavioral equivalence, production reachability or human ownership from commit authorship.

Precedence is fail-closed: security restrictions override protected-platform disposition; protected assets cannot enter domain migration; generated projections cannot become doctrine; duplicate membership requires later equivalence proof; unknown role or activity is quarantined.
''',
          'LCM02_OWNERSHIP_BOUNDARY.md':'''---
title: "LCM-02 Ownership Boundary"
status: reference-restricted
---
# Ownership Boundary

Each artifact is bound to semantic-owner, code-owner and documentation-owner roles. Security-sensitive artifacts are additionally bound to `SECURITY_REVIEWER`. These are role bindings only. With no approved human assignees in the source evidence, ownership remains `ROLE_BOUND_HUMAN_ASSIGNEE_PENDING`.

Commit authorship, directory names and generated metadata are not accepted as ownership evidence. Missing human approval blocks move, delete, semantic refactor, merge, cutover and runtime authority.
''',
          'LCM02_AUTHORITY_BOUNDARY.md':'''---
title: "LCM-02 Authority Boundary"
status: reference-restricted
---
# Authority Boundary

Static capability hits identify risk surfaces; they do not prove live reachability or authority. Order, capital, broker, persistence, network, dynamic-code, global-state, chart-state and time-semantics surfaces are recorded. All runtime, order and capital authority remains false.
''',
          'LCM02_UNRESOLVED_QUEUES.md':'''---
title: "LCM-02 Unresolved Queues"
status: reference-restricted
---
# Unresolved Queues

Separate queues preserve ambiguous role, unknown activity, pending owner assignment, security review, duplicate equivalence and generated-projection non-canonical status. UNKNOWN is neither PASS nor deletion authority. Queue resolution must create reviewed evidence and may not overwrite the original record.
''',
          'LCM02_TO_LCM03_HANDOFF.md':'''---
title: "LCM-02 to LCM-03 Handoff"
status: reference-restricted
---
# Handoff

LCM-03 may register canonical identities and aliases against these governed classification records. It may not infer missing human approval, change source behavior, move or delete source, merge implementations, perform cutover or create runtime authority.
'''
        }
        for name,text in docs.items():write_text(staging/'docs'/name,text)
        payloads=[('LCM01_SURVEY_ACCEPTED',{'survey_id':upstream['survey_id']}),('CLASSIFICATION_REGISTRIES_BOUND',{'role_count':20,'disposition_count':10,'activity_count':10}),('ARTIFACTS_CLASSIFIED',{'artifact_count':len(records)}),('OWNER_ROLES_BOUND',{'family_count':len(families),'human_approval_complete':False}),('AUTHORITY_SURFACES_ISOLATED',{'security_sensitive_count':len(sec)}),('UNRESOLVED_QUEUES_PUBLISHED',{'queue_counts':unresolved['queue_counts']}),('CLASSIFICATION_PACKAGE_COMPLETED',{'classification_id':cid})]
        ledger=build_events(cid,payloads,config.issued_at); write_json(staging/'events/classification_event_ledger.json',ledger)
        prov={'schema_version':'1.0.0','classification_id':cid,'nodes':[{'id':'LCM01_HANDOFF','digest':upstream['handoff']['handoff_digest']},{'id':'LCM01_SURVEY_SUMMARY','digest':upstream['summary']['summary_digest']},{'id':'LCM02_CLASSIFICATION_SUMMARY','digest':summary['summary_digest']},{'id':'LCM02_OWNER_REGISTRY','digest':ownerreg['registry_digest']},{'id':'LCM02_EVENT_LEDGER','digest':ledger['ledger_digest']}],'edges':[{'from':'LCM01_HANDOFF','to':'LCM02_CLASSIFICATION_SUMMARY'},{'from':'LCM01_SURVEY_SUMMARY','to':'LCM02_CLASSIFICATION_SUMMARY'},{'from':'LCM02_CLASSIFICATION_SUMMARY','to':'LCM02_OWNER_REGISTRY'},{'from':'LCM02_OWNER_REGISTRY','to':'LCM02_EVENT_LEDGER'}],'source_semantics_mutated':False,'source_files_moved':False,'source_files_deleted':False,'generated_projection_promoted':False,'runtime_authority_created':False,'live_order_authority_created':False,'capital_authority_created':False}; prov['graph_digest']=digest_object(prov,'graph_digest'); write_json(staging/'provenance/classification_provenance_graph.json',prov)
        handoff={'schema_version':'1.0.0','handoff_type':'LCM02_TO_LCM03','classification_id':cid,'survey_id':upstream['survey_id'],'source_handoff_digest':upstream['handoff']['handoff_digest'],'classification_summary_digest':summary['summary_digest'],'owner_registry_digest':ownerreg['registry_digest'],'unresolved_summary_digest':unresolved['summary_digest'],'completed_gates':['EVERY_ARTIFACT_HAS_ONE_PRIMARY_DISPOSITION','ACTIVE_CANDIDATES_ROLE_BOUND_OR_BLOCKED','SECURITY_SENSITIVE_PATHS_ISOLATED','GENERATED_PROJECTIONS_NON_CANONICAL','PROTECTED_PLATFORM_ASSETS_BLOCKED_FROM_DOMAIN_MIGRATION','UNKNOWN_PRESERVED_AS_BLOCKING'],'allowed_actions':['REGISTER_CANONICAL_IDENTITIES','REGISTER_LEGACY_ALIASES','PROPOSE_FAMILY_IDENTITY_MAP','RESOLVE_OWNER_ROLE_ASSIGNMENTS','RESOLVE_CLASSIFICATION_UNKNOWNS'],'forbidden_actions':['MOVE_SOURCE_FILE','DELETE_SOURCE_FILE','SEMANTIC_REFACTOR','MERGE_LEGACY_IMPLEMENTATIONS','CUTOVER_CONSUMER','QUARANTINE_SOURCE','AUTHORIZE_RUNTIME','AUTHORIZE_LIVE_ORDER','ACTIVATE_CAPITAL'],'unresolved_blockers':['HUMAN_OWNERSHIP_APPROVALS_PENDING','SECURITY_REVIEWS_PENDING','AMBIGUOUS_ROLE_QUEUE_NONEMPTY','UNKNOWN_ACTIVITY_QUEUE_NONEMPTY','DUPLICATE_EQUIVALENCE_REVIEW_PENDING'],'human_approval_claimed':False,'source_move_performed':False,'source_delete_performed':False,'semantic_refactor_performed':False}; handoff['handoff_digest']=digest_object(handoff,'handoff_digest'); write_json(staging/'handoff/lcm02_to_lcm03_handoff.json',handoff)
        receipt={'schema_version':'1.0.0','phase_id':'LCM-02','classification_id':cid,'survey_id':upstream['survey_id'],'claim_ceiling':'CLASSIFICATION_AND_OWNERSHIP_REFERENCE_ONLY','classification_summary_digest':summary['summary_digest'],'owner_registry_digest':ownerreg['registry_digest'],'unresolved_summary_digest':unresolved['summary_digest'],'event_ledger_digest':ledger['ledger_digest'],'provenance_graph_digest':prov['graph_digest'],'handoff_digest':handoff['handoff_digest'],'artifact_classification_record_count':len(records),'source_move_performed':False,'source_delete_performed':False,'semantic_refactor_performed':False,'merge_performed':False,'cutover_performed':False,'human_approval_claimed':False,'runtime_authority_created':False,'live_order_authority_created':False,'capital_authority_created':False}; receipt['receipt_digest']=digest_object(receipt,'receipt_digest'); write_json(staging/'classification_receipt.json',receipt)
        # The output manifest is written last and includes the immutable receipt. The receipt
        # intentionally does not embed the manifest digest, avoiding a self-referential hash cycle.
        manifest=build_manifest(staging,cid); write_json(staging/'output_manifest.json',manifest)
        atomic_publish(staging,final); return final
    except Exception:
        import shutil; shutil.rmtree(staging,ignore_errors=True); raise
