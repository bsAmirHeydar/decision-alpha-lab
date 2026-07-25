from __future__ import annotations
import csv,json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from .aliases import build_aliases,analyze_collisions
from .authority import build_permit,verify_permit
from .canonical import content_id,digest_object
from .consumers import build_consumer_census
from .event_ledger import build as build_events
from .identity import build_identity_candidates,family_map
from .io import atomic_publish,private_staging,read_csv,read_json,read_jsonl,write_csv,write_json,write_jsonl,write_text
from .locators import build_locators
from .manifest import build as build_manifest
from .reports import summary as build_summary
from .upstream import latest_classification,survey_root,verify_classification
from .versioning import registry as version_registry

@dataclass(frozen=True)
class RunConfig:
    repo_root: Path
    destination: Path
    issued_at: str='2026-07-18T00:00:00Z'

def _registry(registry_id,key,values,extra=None):
    obj={'schema_version':'1.0.0','registry_id':registry_id,'closed':True,key:values};obj.update(extra or {});obj['registry_digest']=digest_object(obj,'registry_digest');return obj

def run_identity(config: RunConfig) -> Path:
    repo=config.repo_root.resolve();classification=latest_classification(repo);up=verify_classification(classification);survey=survey_root(repo,up['survey_id'])
    permit=build_permit(up['handoff']['handoff_digest'],up['classification_id'],config.issued_at);verify_permit(permit,up['handoff']['handoff_digest'])
    records=list(read_jsonl(classification/'artifacts/artifact_classification_records.jsonl'))
    active=[r for r in records if r['activity_status'] in {'ACTIVE_PLATFORM','ACTIVE_RESEARCH','ACTIVE_RUNTIME_CANDIDATE'}]
    identities,ambiguities,identity_by_path=build_identity_candidates(records)
    edges=read_csv(survey/'dependencies/all_dependency_edges.csv')
    aliases=build_aliases(repo,active,identity_by_path,edges);aliases,collisions,alias_index=analyze_collisions(aliases)
    locators=build_locators(identities);consumers=build_consumer_census(edges,identity_by_path);family_rows,amb_by_family=family_map(identities,ambiguities)
    material={'classification_id':up['classification_id'],'source_handoff_digest':up['handoff']['handoff_digest'],'policy_version':'LCM03_IDENTITY_POLICY_V1','identity_digests':[x['identity_digest'] for x in identities],'ambiguity_digests':[x['ambiguity_digest'] for x in ambiguities],'alias_digests':[x['alias_digest'] for x in aliases]}
    run_id=content_id('IDENTITY',material);final=config.destination/run_id;staging=private_staging(config.destination,'.lcm03-staging-')
    try:
        marker={'schema_version':'1.0.0','phase_id':'LCM-03','identity_run_id':run_id,'claim_ceiling':'IDENTITY_AND_LOCATOR_REFERENCE_ONLY','source_move_performed':False,'source_delete_performed':False,'semantic_refactor_performed':False,'marker_digest':None};marker['marker_digest']=digest_object(marker,'marker_digest');write_json(staging/'identity_marker.json',marker)
        binding={'schema_version':'1.0.0','classification_id':up['classification_id'],'survey_id':up['survey_id'],'source_handoff_digest':up['handoff']['handoff_digest'],'source_summary_digest':up['summary']['summary_digest'],'source_output_manifest_digest':up['manifest']['output_manifest_digest'],'binding_digest':None};binding['binding_digest']=digest_object(binding,'binding_digest');write_json(staging/'input/lcm02_binding.json',binding)
        write_json(staging/'authority/authority_permit.json',permit)
        from .registries import IDENTITY_KINDS,ALIAS_TYPES,ALIAS_STATUSES,IDENTITY_STATUSES,LOCATOR_STATUSES,RESOLUTION_STATUSES
        regs={
          'identity_kind_registry.json':_registry('LCM03_IDENTITY_KIND_REGISTRY_V1','identity_kinds',[{'identity_kind':k,'prefix':v[0],'logical_namespace':v[1]} for k,v in IDENTITY_KINDS.items()],{'support_artifact_is_domain_semantic_identity':False}),
          'alias_type_registry.json':_registry('LCM03_ALIAS_TYPE_REGISTRY_V1','alias_types',ALIAS_TYPES,{'undeclared_alias_type_allowed':False}),
          'alias_status_registry.json':_registry('LCM03_ALIAS_STATUS_REGISTRY_V1','alias_statuses',ALIAS_STATUSES,{'ambiguous_alias_resolution_allowed':False}),
          'identity_status_registry.json':_registry('LCM03_IDENTITY_STATUS_REGISTRY_V1','identity_statuses',IDENTITY_STATUSES,{'provisional_is_human_approval':False}),
          'locator_status_registry.json':_registry('LCM03_LOCATOR_STATUS_REGISTRY_V1','locator_statuses',LOCATOR_STATUSES,{'path_scan_fallback_allowed':False}),
          'resolution_status_registry.json':_registry('LCM03_RESOLUTION_STATUS_REGISTRY_V1','resolution_statuses',RESOLUTION_STATUSES,{'unknown_is_pass':False}),
          'version_policy_registry.json':version_registry(),
        }
        for name,obj in regs.items(): write_json(staging/'registries'/name,obj)
        id_fields=['identity_id','identity_kind','identity_prefix','semantic_name_candidate','family_candidate','major_version','semantic_version','identity_status','source_classification_id','source_artifact_path','source_artifact_sha256','source_role','source_activity_status','protected_platform_asset','security_sensitive','owner_resolution_status','semantic_owner_role','code_owner_role','human_semantic_approval_claimed','merge_claimed','path_independent_after_registration','identity_digest']
        write_csv(staging/'identities/canonical_identity_candidates.csv',id_fields,identities);write_jsonl(staging/'identities/canonical_identity_candidates.jsonl',identities)
        family_obj={'schema_version':'1.0.0','identity_run_id':run_id,'family_count':len({x['family_candidate'] for x in identities}), 'rows':family_rows,'ambiguity_counts_by_family':dict(sorted(amb_by_family.items())),'automatic_family_merge_allowed':False,'family_map_digest':None};family_obj['family_map_digest']=digest_object(family_obj,'family_map_digest');write_json(staging/'identities/family_identity_map.json',family_obj);write_csv(staging/'identities/family_identity_map.csv',['family_candidate','identity_kind','identity_candidate_count','protected_platform_count','security_review_blocked_count','human_semantic_approval_complete','automatic_merge_allowed','family_identity_status','family_identity_digest'],family_rows)
        alias_fields=['alias_id','alias_type','alias_value','normalized_alias_value','alias_scope','case_sensitive','identity_id','source_artifact_path','alias_status','resolution_status','evidence_codes','confidence_bps','redirect_materialized','cutover_authorized','alias_digest']
        write_csv(staging/'aliases/legacy_alias_records.csv',alias_fields,aliases);write_jsonl(staging/'aliases/legacy_alias_records.jsonl',aliases)
        idx={'schema_version':'1.0.0','identity_run_id':run_id,'index_key_format':'ALIAS_TYPE|SCOPE|NORMALIZED_VALUE','resolvable_alias_count':len(alias_index),'index':alias_index,'path_scan_fallback_allowed':False,'index_digest':None};idx['index_digest']=digest_object(idx,'index_digest');write_json(staging/'aliases/alias_resolution_index.json',idx)
        write_jsonl(staging/'aliases/ambiguous_alias_queue.jsonl',[{'collision_id':c['collision_id'],'alias_type':c['alias_type'],'alias_scope':c['alias_scope'],'normalized_alias_value':c['normalized_alias_value'],'identity_ids':c['identity_ids'],'source_artifact_paths':c['source_artifact_paths'],'resolution_status':'AMBIGUOUS_BLOCKED','human_resolution_required':True,'source_collision_digest':c['collision_digest']} for c in collisions])
        loc_fields=['identity_id','identity_kind','semantic_version','compatibility_range','logical_uri','current_artifact_path','current_artifact_sha256','materialized_canonical_path','locator_status','canonical_path_materialized','authority_class','runtime_authority','live_order_authority','capital_authority','locator_digest']
        write_csv(staging/'locators/artifact_locator_records.csv',loc_fields,locators);write_jsonl(staging/'locators/artifact_locator_records.jsonl',locators)
        logical={'schema_version':'1.0.0','identity_run_id':run_id,'locators':{x['identity_id']:x['logical_uri'] for x in locators},'materialized_path_count':0,'locator_index_digest':None};logical['locator_index_digest']=digest_object(logical,'locator_index_digest');write_json(staging/'locators/logical_locator_index.json',logical)
        cons_fields=['consumer_record_id','target_identity_id','target_artifact_path','consumer_artifact_path','edge_type','raw_target','line_number','resolution_status','semantic_reachability_claimed','consumer_digest']
        write_csv(staging/'consumers/consumer_census.csv',cons_fields,consumers);write_jsonl(staging/'consumers/consumer_census.jsonl',consumers)
        collision_obj={'schema_version':'1.0.0','identity_run_id':run_id,'collision_count':len(collisions),'collisions':collisions,'automatic_resolution_allowed':False,'collision_report_digest':None};collision_obj['collision_report_digest']=digest_object(collision_obj,'collision_report_digest');write_json(staging/'collisions/alias_collision_report.json',collision_obj)
        object_collisions=[c for c in collisions if c['alias_type']=='OBJECT_PREFIX'];objrep={'schema_version':'1.0.0','identity_run_id':run_id,'object_prefix_collision_count':len(object_collisions),'collisions':object_collisions,'cross_chart_collision_risk_requires_runtime_characterization':True,'report_digest':None};objrep['report_digest']=digest_object(objrep,'report_digest');write_json(staging/'collisions/object_prefix_collision_report.json',objrep)
        casefold=read_json(survey/'path_safety/case_insensitive_path_collisions.json');case_rep={'schema_version':'1.0.0','identity_run_id':run_id,'source_survey_id':up['survey_id'],'collision_count':casefold.get('collision_count',0),'collisions':casefold.get('collisions',[]),'source_report_digest':digest_object(casefold),'report_digest':None};case_rep['report_digest']=digest_object(case_rep,'report_digest');write_json(staging/'collisions/casefold_path_collision_report.json',case_rep)
        write_jsonl(staging/'unresolved/identity_ambiguity_queue.jsonl',ambiguities)
        unresolved={'schema_version':'1.0.0','identity_run_id':run_id,'identity_ambiguity_count':len(ambiguities),'alias_collision_count':len(collisions),'security_review_blocked_identity_count':sum(x['security_sensitive'] for x in identities),'owner_assignment_pending_identity_count':sum(x['owner_resolution_status']!='HUMAN_APPROVED' for x in identities),'human_resolution_required':bool(ambiguities or collisions),'unknown_is_not_pass':True,'unknown_is_not_merge_authority':True,'unresolved_digest':None};unresolved['unresolved_digest']=digest_object(unresolved,'unresolved_digest');write_json(staging/'unresolved/unresolved_summary.json',unresolved)
        summary=build_summary(run_id,up['classification_id'],identities,ambiguities,aliases,collisions,locators,consumers);write_json(staging/'reports/identity_summary.json',summary)
        coverage={'schema_version':'1.0.0','identity_run_id':run_id,'active_candidate_count':len(active),'covered_by_identity_count':len(identities),'covered_by_explicit_ambiguity_count':len(ambiguities),'uncovered_active_candidate_count':len(active)-len(identities)-len(ambiguities),'coverage_complete':len(active)==len(identities)+len(ambiguities),'legacy_path_alias_count':sum(x['alias_type']=='LEGACY_PATH' for x in aliases),'consumer_census_count':len(consumers),'coverage_digest':None};coverage['coverage_digest']=digest_object(coverage,'coverage_digest');write_json(staging/'reports/coverage_report.json',coverage)
        ledger=build_events(run_id,config.issued_at,[('LCM02_PACKAGE_ACCEPTED',{'classification_id':up['classification_id']}),('IDENTITY_POLICY_BOUND',{'version_policy_digest':regs['version_policy_registry.json']['registry_digest']}),('IDENTITY_CANDIDATES_REGISTERED',{'count':len(identities),'ambiguity_count':len(ambiguities)}),('LEGACY_ALIASES_REGISTERED',{'count':len(aliases)}),('COLLISIONS_BLOCKED',{'collision_count':len(collisions)}),('ARTIFACT_LOCATORS_BUILT',{'count':len(locators)}),('CONSUMER_CENSUS_COMPLETED',{'count':len(consumers)}),('LCM04_HANDOFF_PREPARED',{'characterization_execution_allowed':False})]);write_json(staging/'events/identity_event_ledger.json',ledger)
        provenance={'schema_version':'1.0.0','phase_id':'LCM-03','identity_run_id':run_id,'source_classification_id':up['classification_id'],'nodes':[{'node_id':'LCM02_CLASSIFICATION','digest':up['summary']['summary_digest']},{'node_id':'LCM03_IDENTITIES','digest':summary['summary_digest']},{'node_id':'LCM03_ALIASES','digest':idx['index_digest']},{'node_id':'LCM03_COLLISIONS','digest':collision_obj['collision_report_digest']},{'node_id':'LCM03_LOCATORS','digest':logical['locator_index_digest']},{'node_id':'LCM03_EVENTS','digest':ledger['ledger_digest']}],'edges':[{'from':'LCM02_CLASSIFICATION','to':'LCM03_IDENTITIES'},{'from':'LCM03_IDENTITIES','to':'LCM03_ALIASES'},{'from':'LCM03_ALIASES','to':'LCM03_COLLISIONS'},{'from':'LCM03_IDENTITIES','to':'LCM03_LOCATORS'},{'from':'LCM03_LOCATORS','to':'LCM03_EVENTS'}],'source_paths_moved':False,'source_paths_deleted':False,'semantic_behavior_changed':False,'runtime_authority_created':False,'live_order_authority_created':False,'capital_authority_created':False,'graph_digest':None};provenance['graph_digest']=digest_object(provenance,'graph_digest');write_json(staging/'provenance/identity_provenance_graph.json',provenance)
        handoff={'schema_version':'1.0.0','handoff_type':'LCM03_TO_LCM04','identity_run_id':run_id,'classification_id':up['classification_id'],'source_handoff_digest':up['handoff']['handoff_digest'],'identity_summary_digest':summary['summary_digest'],'alias_resolution_index_digest':idx['index_digest'],'locator_index_digest':logical['locator_index_digest'],'unresolved_digest':unresolved['unresolved_digest'],'completed_gates':['ALL_ACTIVE_CANDIDATES_IDENTITY_OR_EXPLICIT_AMBIGUITY','IDENTITY_IDS_UNIQUE','ALIASES_DETERMINISTIC_OR_BLOCKED','UNKNOWN_VERSION_FAILS_CLOSED','CONSUMER_CENSUS_RECORDED','OBJECT_PREFIX_COLLISIONS_REPORTED','NO_SOURCE_MOVE_OR_DELETE'],'allowed_actions':['BUILD_CHARACTERIZATION_PACKETS','REGISTER_GOLDEN_CASES','INSTRUMENT_LEGACY_TRACES','RESOLVE_IDENTITY_AMBIGUITIES','RESOLVE_ALIAS_COLLISIONS','ASSIGN_HUMAN_OWNERS'],'forbidden_actions':['MOVE_SOURCE_FILE','DELETE_SOURCE_FILE','SEMANTIC_REFACTOR','MERGE_LEGACY_IMPLEMENTATIONS','CUTOVER_CONSUMER','QUARANTINE_SOURCE','TREAT_PROVISIONAL_IDENTITY_AS_SEMANTIC_APPROVAL','AUTHORIZE_RUNTIME','AUTHORIZE_LIVE_ORDER','ACTIVATE_CAPITAL'],'unresolved_blockers':['IDENTITY_AMBIGUITIES_PENDING' if ambiguities else None,'ALIAS_COLLISIONS_PENDING' if collisions else None,'HUMAN_OWNER_APPROVALS_PENDING','SECURITY_REVIEWS_PENDING'],'characterization_execution_allowed':False,'human_semantic_approval_claimed':False,'source_move_performed':False,'source_delete_performed':False,'semantic_refactor_performed':False,'handoff_digest':None};handoff['unresolved_blockers']=[x for x in handoff['unresolved_blockers'] if x];handoff['handoff_digest']=digest_object(handoff,'handoff_digest');write_json(staging/'handoff/lcm03_to_lcm04_handoff.json',handoff)
        receipt={'schema_version':'1.0.0','phase_id':'LCM-03','identity_run_id':run_id,'classification_id':up['classification_id'],'claim_ceiling':'IDENTITY_AND_LOCATOR_REFERENCE_ONLY','identity_summary_digest':summary['summary_digest'],'coverage_report_digest':coverage['coverage_digest'],'alias_resolution_index_digest':idx['index_digest'],'locator_index_digest':logical['locator_index_digest'],'event_ledger_digest':ledger['ledger_digest'],'provenance_graph_digest':provenance['graph_digest'],'handoff_digest':handoff['handoff_digest'],'identity_candidate_count':len(identities),'identity_ambiguity_count':len(ambiguities),'alias_record_count':len(aliases),'alias_collision_count':len(collisions),'locator_record_count':len(locators),'consumer_record_count':len(consumers),'source_move_performed':False,'source_delete_performed':False,'semantic_refactor_performed':False,'merge_performed':False,'cutover_performed':False,'human_semantic_approval_claimed':False,'runtime_authority_created':False,'live_order_authority_created':False,'capital_authority_created':False,'receipt_digest':None};receipt['receipt_digest']=digest_object(receipt,'receipt_digest');write_json(staging/'identity_receipt.json',receipt)
        # Human-readable package views.
        write_text(
            staging / "docs/LCM03_EXECUTIVE_BRIEF.md",
            f"""# LCM-03 Executive Brief

Identity run: `{run_id}`

- Active candidates: {len(active)}
- Provisional identity candidates: {len(identities)}
- Explicit identity ambiguities: {len(ambiguities)}
- Alias records: {len(aliases)}
- Alias collisions blocked: {len(collisions)}
- Locator records: {len(locators)}
- Consumer records: {len(consumers)}

No source was moved, deleted, merged, refactored, cut over or granted runtime authority.
""",
        )
        write_text(
            staging / "docs/LCM03_IDENTITY_POLICY.md",
            """# LCM-03 Identity Policy

Canonical IDs are stable after registration. File paths are aliases, not domain truth. A provisional identity is not semantic approval. Materially different variants are never merged without owner-reviewed behavioral equivalence.
""",
        )
        write_text(
            staging / "docs/LCM03_ALIAS_POLICY.md",
            """# LCM-03 Alias Policy

Alias resolution uses a closed type, explicit scope and normalized value. Collisions block resolution. Repository scanning by convention is not an approved fallback.
""",
        )
        write_text(
            staging / "docs/LCM03_LOCATOR_POLICY.md",
            """# LCM-03 Locator Policy

Logical locators bind identity to the current immutable source artifact. Physical canonical target paths are not materialized until LCM-05.
""",
        )
        write_text(
            staging / "docs/LCM03_TO_LCM04_HANDOFF.md",
            """# LCM-03 to LCM-04 Handoff

LCM-04 may build characterization packets and traces only for identity-bound or explicitly reviewed ambiguity records. It may not rewrite legacy semantics.
""",
        )
        manifest=build_manifest(staging,run_id);write_json(staging/'output_manifest.json',manifest)
        atomic_publish(staging,final);return final
    except Exception:
        import shutil;shutil.rmtree(staging,ignore_errors=True);raise
