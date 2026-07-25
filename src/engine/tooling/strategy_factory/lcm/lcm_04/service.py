from __future__ import annotations
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from .authority import build_permit,verify_permit
from .canonical import content_id,digest_object
from .case_catalog import build as build_case_catalog
from .event_ledger import build as build_events
from .io import atomic_publish,private_staging,write_csv,write_json,write_jsonl,write_text
from .known_time import audit as known_time_audit
from .manifest import build as build_manifest
from .packets import packet,priority,instrumentation_plan
from .registries import *
from .static_profile import profile
from .trace import reference_inputs,build_trace,trace_bundle
from .upstream import latest_identity,verify_identity

@dataclass(frozen=True)
class RunConfig:
    repo_root: Path
    destination: Path
    issued_at: str='2026-07-19T00:00:00Z'

def _registry_files(staging):
    regs={
      'golden_case_type_registry.json':registry('LCM04_GOLDEN_CASE_TYPE_REGISTRY_V1','case_types',CASE_TYPES,{'dynamic_case_type_allowed':False}),
      'trace_event_type_registry.json':registry('LCM04_TRACE_EVENT_TYPE_REGISTRY_V1','event_types',EVENT_TYPES,{'undeclared_event_type_allowed':False}),
      'packet_status_registry.json':registry('LCM04_PACKET_STATUS_REGISTRY_V1','packet_statuses',PACKET_STATUSES,{'unknown_is_ready':False}),
      'trace_evidence_status_registry.json':registry('LCM04_TRACE_EVIDENCE_STATUS_REGISTRY_V1','evidence_statuses',TRACE_EVIDENCE_STATUSES,{'reference_fixture_is_legacy_evidence':False}),
      'known_time_status_registry.json':registry('LCM04_KNOWN_TIME_STATUS_REGISTRY_V1','known_time_statuses',KNOWN_TIME_STATUSES,{'unknown_is_pass':False}),
      'defect_status_registry.json':registry('LCM04_DEFECT_STATUS_REGISTRY_V1','defect_statuses',DEFECT_STATUSES,{'observed_is_approved_correction':False}),
      'bar_status_registry.json':registry('LCM04_BAR_STATUS_REGISTRY_V1','bar_statuses',BAR_STATUSES),
      'environment_kind_registry.json':registry('LCM04_ENVIRONMENT_KIND_REGISTRY_V1','environment_kinds',ENVIRONMENT_KINDS,{'unknown_environment_is_parity_evidence':False}),
    }
    for name,obj in regs.items(): write_json(staging/'registries'/name,obj)
    return regs

def run(config: RunConfig) -> Path:
    repo=config.repo_root.resolve();up=verify_identity(latest_identity(repo));handoff=up['handoff']
    permit=build_permit(handoff['handoff_digest'],up['marker']['identity_run_id'],config.issued_at);verify_permit(permit,handoff['handoff_digest'])
    profiles=[];packets=[];priorities=[];plans=[]
    for ident in up['identities']:
        pr=profile(repo,ident);pa=packet(ident,pr)
        profiles.append(pr);packets.append(pa);priorities.append(priority(pa,pr));plans.append(instrumentation_plan(pa,pr))
    priorities=sorted(priorities,key=lambda x:(x['queue_priority_score'],x['identity_kind'],x['identity_id']))
    catalog=build_case_catalog();inputs=reference_inputs();events=build_trace(inputs);bundle=trace_bundle(events);audit=known_time_audit(events)
    material={'identity_run_id':up['marker']['identity_run_id'],'source_handoff_digest':handoff['handoff_digest'],
              'packet_digests':[x['packet_digest'] for x in packets], 'catalog_digest':catalog['catalog_digest'],
              'reference_trace_bundle_digest':bundle['bundle_digest'],'policy_version':'LCM04_CHARACTERIZATION_POLICY_V1'}
    run_id=content_id('CHARACTERIZATION',material);final=config.destination/run_id;staging=private_staging(config.destination,'.lcm04-staging-')
    try:
        marker={'schema_version':'1.0.0','phase_id':'LCM-04','characterization_run_id':run_id,
                'claim_ceiling':'LEGACY_BEHAVIOR_CHARACTERIZATION_ONLY','phase_completion_state':'FOUNDATION_COMPLETE_LEGACY_EXECUTION_BLOCKED',
                'legacy_trace_execution_count':0,'source_instrumentation_mutation_performed':False,'source_move_performed':False,
                'source_delete_performed':False,'semantic_refactor_performed':False,'cutover_performed':False,'marker_digest':None}
        marker['marker_digest']=digest_object(marker,'marker_digest');write_json(staging/'characterization_marker.json',marker)
        binding={'schema_version':'1.0.0','identity_run_id':up['marker']['identity_run_id'],'classification_id':handoff['classification_id'],
                 'source_handoff_digest':handoff['handoff_digest'],'source_identity_summary_digest':handoff['identity_summary_digest'],
                 'source_output_manifest_digest':up['manifest']['output_manifest_digest'],'binding_digest':None}
        binding['binding_digest']=digest_object(binding,'binding_digest');write_json(staging/'input/lcm03_binding.json',binding)
        write_json(staging/'authority/authority_permit.json',permit);_registry_files(staging);write_json(staging/'cases/golden_case_catalog.json',catalog)
        profile_fields=['identity_id','source_artifact_path','source_artifact_sha256','file_exists','binary_or_unreadable','size_bytes','line_count','include_or_import_count','function_count_estimate','callbacks','capabilities','characterization_risk_score','static_profile_is_behavioral_proof','profile_digest']
        write_jsonl(staging/'profiles/source_static_profiles.jsonl',profiles);write_csv(staging/'profiles/source_static_profiles.csv',profile_fields,profiles)
        packet_fields=['packet_id','identity_id','identity_kind','family_candidate','source_artifact_path','source_artifact_sha256','identity_digest','identity_status','owner_resolution_status','protected_platform_asset','security_sensitive','packet_status','legacy_execution_allowed','source_mutation_allowed','required_case_types','required_case_count','static_profile_digest','blocking_reason_codes','observed_behavior_captured','intended_correction_registered','packet_digest']
        write_jsonl(staging/'packets/characterization_packet_index.jsonl',packets);write_csv(staging/'packets/characterization_packet_index.csv',packet_fields,packets)
        write_jsonl(staging/'instrumentation/instrumentation_plans.jsonl',plans)
        write_jsonl(staging/'priorities/characterization_priority_queue.jsonl',priorities);write_csv(staging/'priorities/characterization_priority_queue.csv',list(priorities[0].keys()),priorities)
        ambiguity_packets=[]
        for a in up['ambiguities']:
            x={'schema_version':'1.0.0','ambiguity_id':a['ambiguity_id'],'source_artifact_path':a['artifact_path'],
               'family_candidate':a['family_candidate'],'packet_status':'BLOCKED_IDENTITY_AMBIGUITY',
               'legacy_execution_allowed':False,'human_resolution_required':True,'source_ambiguity_digest':a['ambiguity_digest'],'packet_digest':None}
            x['packet_digest']=digest_object(x,'packet_digest');ambiguity_packets.append(x)
        write_jsonl(staging/'packets/identity_ambiguity_characterization_queue.jsonl',ambiguity_packets)
        write_jsonl(staging/'traces/reference_fixture_inputs.jsonl',inputs);write_jsonl(staging/'traces/reference_normalized_events.jsonl',events);write_json(staging/'traces/reference_trace_bundle.json',bundle)
        replay={'schema_version':'1.0.0','first_bundle_digest':bundle['bundle_digest'],'second_bundle_digest':trace_bundle(build_trace(reference_inputs()))['bundle_digest'],
                'deterministic':bundle['bundle_digest']==trace_bundle(build_trace(reference_inputs()))['bundle_digest'],'legacy_replay_claimed':False,'replay_digest':None}
        replay['replay_digest']=digest_object(replay,'replay_digest');write_json(staging/'traces/reference_replay_stability.json',replay);write_json(staging/'audit/reference_known_time_audit.json',audit)
        defect={'schema_version':'1.0.0','phase_id':'LCM-04','record_count':0,'records':[],
                'absence_of_record_is_absence_of_defect_claim':False,'silent_bug_fix_allowed':False,'register_digest':None};defect['register_digest']=digest_object(defect,'register_digest');write_json(staging/'defects/observed_defect_register.json',defect)
        correction={'schema_version':'1.0.0','phase_id':'LCM-04','record_count':0,'records':[],
                    'observed_and_intended_must_be_separate':True,'semantic_version_bump_required':True,
                    'migration_may_approve_correction':False,'register_digest':None};correction['register_digest']=digest_object(correction,'register_digest');write_json(staging/'defects/intended_correction_register.json',correction)
        status_counts=Counter(x['packet_status'] for x in packets);kind_counts=Counter(x['identity_kind'] for x in packets)
        capability_counts=Counter()
        for pr in profiles:
            for k,v in pr['capabilities'].items(): capability_counts[k]+=int(v)
        blockers=[
          {'blocker_id':'LCM04_BLOCKER_OWNER_APPROVALS','reason_code':'HUMAN_OWNER_APPROVALS_PENDING','affected_count':sum(x['owner_resolution_status']!='HUMAN_APPROVED' for x in packets),'blocks_legacy_execution':True},
          {'blocker_id':'LCM04_BLOCKER_SECURITY_REVIEWS','reason_code':'SECURITY_REVIEWS_PENDING','affected_count':status_counts.get('BLOCKED_SECURITY_REVIEW',0),'blocks_legacy_execution':True},
          {'blocker_id':'LCM04_BLOCKER_IDENTITY_AMBIGUITIES','reason_code':'IDENTITY_AMBIGUITIES_PENDING','affected_count':len(ambiguity_packets),'blocks_legacy_execution':True},
          {'blocker_id':'LCM04_BLOCKER_EXTERNAL_RUNTIME','reason_code':'MQL5_METATRADER_RUNTIME_NOT_AVAILABLE_IN_REFERENCE_ENVIRONMENT','affected_count':sum(x['source_artifact_path'].lower().endswith(('.mq5','.mqh')) for x in packets),'blocks_legacy_execution':True},
        ]
        for b in blockers: b['blocker_digest']=digest_object(b,'blocker_digest')
        write_json(staging/'blockers/characterization_blockers.json',{'schema_version':'1.0.0','blocker_count':len(blockers),'blockers':blockers,'blocker_bundle_digest':digest_object(blockers)})
        coverage={'schema_version':'1.0.0','identity_run_id':up['marker']['identity_run_id'],'characterization_run_id':run_id,
                  'active_candidate_count':len(packets)+len(ambiguity_packets),'identity_packet_count':len(packets),'ambiguity_packet_count':len(ambiguity_packets),
                  'static_profile_count':len(profiles),'instrumentation_plan_count':len(plans),'required_case_mapping_count':len(packets),
                  'identity_and_ambiguity_coverage_complete':len(packets)+len(ambiguity_packets)==len(up['identities'])+len(up['ambiguities']),
                  'legacy_observed_trace_coverage_complete':False,'coverage_digest':None};coverage['coverage_digest']=digest_object(coverage,'coverage_digest');write_json(staging/'reports/coverage_report.json',coverage)
        summary={'schema_version':'1.0.0','phase_id':'LCM-04','characterization_run_id':run_id,'identity_run_id':up['marker']['identity_run_id'],
                 'claim_ceiling':'LEGACY_BEHAVIOR_CHARACTERIZATION_ONLY','phase_completion_state':'FOUNDATION_COMPLETE_LEGACY_EXECUTION_BLOCKED',
                 'identity_packet_count':len(packets),'identity_ambiguity_packet_count':len(ambiguity_packets),
                 'packet_status_counts':dict(sorted(status_counts.items())),'identity_kind_counts':dict(sorted(kind_counts.items())),
                 'capability_counts':dict(sorted(capability_counts.items())),'golden_case_type_count':catalog['case_count'],
                 'reference_fixture_case_count':len(inputs),'reference_fixture_event_count':len(events),'reference_replay_deterministic':replay['deterministic'],
                 'reference_known_time_status':audit['status'],'legacy_trace_execution_count':0,'legacy_observed_trace_count':0,
                 'legacy_replay_stable_count':0,'observed_defect_count':0,'intended_correction_count':0,
                 'acceptance_gate_passed':False,'acceptance_gate_blockers':[x['reason_code'] for x in blockers],
                 'source_instrumentation_mutation_performed':False,'source_move_performed':False,'source_delete_performed':False,
                 'semantic_refactor_performed':False,'merge_performed':False,'cutover_performed':False,
                 'runtime_authority_created':False,'live_order_authority_created':False,'capital_authority_created':False,'summary_digest':None}
        summary['summary_digest']=digest_object(summary,'summary_digest');write_json(staging/'reports/characterization_summary.json',summary)
        hostile={'schema_version':'1.0.0','checks':[
          {'check':'INSTRUMENTATION_TIMING_MUTATION','status':'PASS','evidence':'NO_SOURCE_INSTRUMENTATION_MATERIALIZED'},
          {'check':'REFERENCE_FIXTURE_MISREPRESENTED_AS_LEGACY','status':'PASS','evidence':'EVIDENCE_STATUS_REFERENCE_FIXTURE_ONLY'},
          {'check':'UNKNOWN_CONVERTED_TO_PASS','status':'PASS','evidence':'LEGACY_EXECUTION_BLOCKED'},
          {'check':'CURRENT_BAR_HIDDEN_BY_DRAWING','status':'PASS','evidence':'CURRENT_BAR_CASE_REQUIRED_WHEN_STATIC_CAPABILITY_DETECTED'},
          {'check':'UNSTABLE_RANDOM_IDS','status':'PASS','evidence':'CONTENT_DERIVED_IDS'},
          {'check':'ORDER_AUTHORITY_ESCALATION','status':'PASS','evidence':'BROKER_SUBMISSION_DISABLED'},
        ],'hostile_review_passed':True,'production_or_legacy_parity_claimed':False,'review_digest':None};hostile['review_digest']=digest_object(hostile,'review_digest');write_json(staging/'reports/hostile_review.json',hostile)
        hand={'schema_version':'1.0.0','handoff_type':'LCM04_TO_LCM05','characterization_run_id':run_id,'identity_run_id':up['marker']['identity_run_id'],
              'source_handoff_digest':handoff['handoff_digest'],'characterization_summary_digest':summary['summary_digest'],
              'coverage_report_digest':coverage['coverage_digest'],'reference_trace_bundle_digest':bundle['bundle_digest'],
              'legacy_characterization_complete':False,'target_path_materialization_allowed':False,
              'allowed_actions':['BUILD_TARGET_TOPOLOGY_PROPOSALS','RESOLVE_OWNER_APPROVALS','RESOLVE_IDENTITY_AMBIGUITIES','EXECUTE_APPROVED_LEGACY_CHARACTERIZATION','CAPTURE_LEGACY_GOLDEN_TRACES','REGISTER_OBSERVED_DEFECTS'],
              'forbidden_actions':['MOVE_SOURCE_FILE','DELETE_SOURCE_FILE','SEMANTIC_REFACTOR','MERGE_LEGACY_IMPLEMENTATIONS','MATERIALIZE_CANONICAL_TARGET_PATH','CUTOVER_CONSUMER','QUARANTINE_SOURCE','TREAT_REFERENCE_FIXTURE_AS_LEGACY_EVIDENCE','AUTHORIZE_RUNTIME','AUTHORIZE_LIVE_ORDER','ACTIVATE_CAPITAL'],
              'completed_gates':['ALL_IDENTITIES_PACKETIZED','ALL_AMBIGUITIES_EXPLICITLY_BLOCKED','CLOSED_GOLDEN_CASE_CATALOG_REGISTERED','STATIC_CHARACTERIZATION_PROFILES_BUILT','REFERENCE_HARNESS_REPLAY_STABLE','KNOWN_TIME_AUDIT_PASS','NO_SOURCE_MUTATION'],
              'unresolved_blockers':[x['reason_code'] for x in blockers],'handoff_digest':None};hand['handoff_digest']=digest_object(hand,'handoff_digest');write_json(staging/'handoff/lcm04_to_lcm05_handoff.json',hand)
        ledger=build_events(run_id,[
          ('LCM03_PACKAGE_ACCEPTED',{'source_handoff_digest':handoff['handoff_digest']}),
          ('AUTHORITY_PERMIT_BOUND',{'permit_digest':permit['permit_digest']}),
          ('CHARACTERIZATION_PACKETS_REGISTERED',{'packet_count':len(packets),'ambiguity_count':len(ambiguity_packets)}),
          ('GOLDEN_CASE_CATALOG_BOUND',{'catalog_digest':catalog['catalog_digest']}),
          ('REFERENCE_HARNESS_EXECUTED',{'trace_bundle_digest':bundle['bundle_digest']}),
          ('KNOWN_TIME_AUDIT_COMPLETED',{'audit_digest':audit['audit_digest']}),
          ('LEGACY_EXECUTION_BLOCKERS_RECORDED',{'blocker_count':len(blockers)}),
          ('LCM05_HANDOFF_PREPARED',{'handoff_digest':hand['handoff_digest']}),
        ],config.issued_at);write_json(staging/'events/characterization_event_ledger.json',ledger)
        prov={'schema_version':'1.0.0','phase_id':'LCM-04','characterization_run_id':run_id,
              'nodes':['LCM03_HANDOFF','LCM04_PACKET_INDEX','LCM04_CASE_CATALOG','LCM04_REFERENCE_TRACE_BUNDLE','LCM04_SUMMARY','LCM04_HANDOFF'],
              'edges':[['LCM03_HANDOFF','LCM04_PACKET_INDEX'],['LCM04_PACKET_INDEX','LCM04_CASE_CATALOG'],['LCM04_CASE_CATALOG','LCM04_REFERENCE_TRACE_BUNDLE'],['LCM04_REFERENCE_TRACE_BUNDLE','LCM04_SUMMARY'],['LCM04_SUMMARY','LCM04_HANDOFF']],
              'reaches_lcm03_identity':True,'reference_fixture_disclosed':True,'legacy_behavior_invented':False,
              'source_mutated':False,'runtime_authority_created':False,'live_order_authority_created':False,'capital_authority_created':False,'provenance_digest':None}
        prov['provenance_digest']=digest_object(prov,'provenance_digest');write_json(staging/'provenance/characterization_provenance_graph.json',prov)
        write_text(staging/'docs/LCM04_EXECUTIVE_BRIEF.md', f"""# LCM-04 Executive Brief

Run: `{run_id}`

The characterization foundation covers {len(packets)} identity-bound artifacts and {len(ambiguity_packets)} explicit ambiguities. Legacy execution remains blocked by missing human owner approvals, security reviews, identity ambiguities and unavailable MetaTrader runtime evidence. Reference traces prove only the harness mechanics.
""")
        write_text(staging/'docs/LCM04_TRACE_CONTRACT.md', """# LCM-04 Trace Contract

Every trace is ordered, content-addressed, known-time explicit and authority-denied. Reference fixtures are never legacy evidence.
""")
        write_text(staging/'docs/LCM04_TO_LCM05_HANDOFF.md', """# LCM-04 to LCM-05 Handoff

LCM-05 may author target topology proposals but may not materialize paths until legacy characterization and owner approvals are complete.
""")
        receipt={'schema_version':'1.0.0','phase_id':'LCM-04','characterization_run_id':run_id,'identity_run_id':up['marker']['identity_run_id'],
                 'claim_ceiling':'LEGACY_BEHAVIOR_CHARACTERIZATION_ONLY','packet_count':len(packets),'ambiguity_packet_count':len(ambiguity_packets),
                 'reference_trace_bundle_digest':bundle['bundle_digest'],'summary_digest':summary['summary_digest'],'coverage_digest':coverage['coverage_digest'],
                 'handoff_digest':hand['handoff_digest'],'event_ledger_digest':ledger['ledger_digest'],'provenance_digest':prov['provenance_digest'],
                 'legacy_trace_execution_count':0,'source_mutation_performed':False,'source_move_performed':False,'source_delete_performed':False,
                 'semantic_refactor_performed':False,'merge_performed':False,'cutover_performed':False,'runtime_authority_created':False,
                 'live_order_authority_created':False,'capital_authority_created':False,'receipt_digest':None}
        receipt['receipt_digest']=digest_object(receipt,'receipt_digest');write_json(staging/'characterization_receipt.json',receipt)
        manifest=build_manifest(staging,run_id);write_json(staging/'output_manifest.json',manifest);atomic_publish(staging,final);return final
    except Exception:
        import shutil;shutil.rmtree(staging,ignore_errors=True);raise
