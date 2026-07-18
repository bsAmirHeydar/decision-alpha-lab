from __future__ import annotations
import shutil,tempfile
from pathlib import Path
from typing import Any
from .active_planner import build_proposals
from .artifact_manifest import build_output_manifest
from .authority import validate_authority
from .canonical import digest_object,stable_id,with_digest
from .duplicate_detector import detect
from .event_ledger import build_event_ledger,verify_event_ledger
from .handoff_input import load_acl08_bundle
from .io import atomic_publish,dump_json
from .memory_policy import validate_memory_policy
from .memory_store import load_prior,decide_admissions,build_index
from .obsidian_projection import summary_md,memory_md,planner_md,duplicate_md
from .planner_policy import validate_planner_policy
from .poison_guard import inspect_records
from .policies import CLAIM_CEILING,SERVICE_VERSION
from .provenance import build_provenance
from .question_registry import registry_snapshot,validate_registry

class ACL09MemoryPlannerService:
    def build(self,acl08_root:Path,permit:dict[str,Any],memory_policy:dict[str,Any],planner_policy:dict[str,Any],destination:Path,processed_at:str,prior_root:Path|None=None)->dict[str,Any]:
        bundle=load_acl08_bundle(acl08_root); authority=validate_authority(permit,bundle['handoff'])
        memory_policy=validate_memory_policy(memory_policy); planner_policy=validate_planner_policy(planner_policy)
        registry=validate_registry(registry_snapshot()); prior=load_prior(prior_root)
        poisoning=inspect_records(bundle['records'],bundle['handoff']['report_id'])
        memory_run_id=stable_id('MEMRUN',bundle['handoff']['report_id'],bundle['handoff']['handoff_digest'],memory_policy['policy_digest'],planner_policy['policy_digest'],prior['parent_memory_index_digest'],processed_at,length=32)
        destination=destination.resolve(); staging=Path(tempfile.mkdtemp(prefix='.acl09_staging_',dir=destination.parent if destination.parent.exists() else None))
        try:
            (staging/'.acl09_generated_root').write_text('ACL-09 GENERATED ROOT — DO NOT HAND EDIT\n',encoding='utf-8')
            binding=with_digest({'schema_version':'1.0.0','memory_run_id':memory_run_id,'report_id':bundle['handoff']['report_id'],'validation_id':bundle['handoff']['validation_id'],'run_id':bundle['handoff']['run_id'],'batch_id':bundle['handoff']['batch_id'],'acl08_handoff_digest':bundle['handoff']['handoff_digest'],'acl08_report_run_digest':bundle['run']['report_run_digest'],'acl08_batch_report_digest':bundle['batch']['batch_report_digest'],'acl08_experience_bundle_digest':bundle['experience']['experience_bundle_digest'],'acl08_input_bundle_digest':bundle['bundle_digest'],'source_decisions_mutated':False},'binding_digest')
            dump_json(staging/'binding/acl08_binding.json',binding); dump_json(staging/'authority/authority_report.json',authority)
            dump_json(staging/'policy/memory_policy_snapshot.json',memory_policy); dump_json(staging/'policy/planner_policy_snapshot.json',planner_policy); dump_json(staging/'policy/research_question_registry_snapshot.json',registry)
            dump_json(staging/'security/memory_poisoning_report.json',poisoning)
            equiv=detect(bundle['records'],memory_policy['near_duplicate_threshold_bps'],prior['memory_fingerprints']); dump_json(staging/'duplicates/equivalence_report.json',equiv)
            for cluster in equiv['clusters']: dump_json(staging/f"duplicates/clusters/{cluster['cluster_id']}.json",cluster)
            for pair in equiv['near_equivalences']: dump_json(staging/f"duplicates/near_equivalences/{pair['pair_id']}.json",pair)
            decisions,entries,aliases,quarantines=decide_admissions(bundle['records'],equiv,bundle['handoff']['report_id'],prior)
            for x in decisions: dump_json(staging/f"memory/admission_decisions/{x['admission_decision_id']}.json",x)
            for x in entries: dump_json(staging/f"memory/entries/{x['memory_entry_id']}.json",x)
            for x in aliases: dump_json(staging/f"memory/aliases/{x['alias_id']}.json",x)
            for x in quarantines: dump_json(staging/f"memory/quarantine/{x['quarantine_id']}.json",x)
            index=build_index(memory_run_id,bundle['handoff']['report_id'],entries,aliases,quarantines,decisions,prior['parent_memory_index_digest']); dump_json(staging/'memory/memory_index.json',index)
            admission_bundle=with_digest({'schema_version':'1.0.0','memory_run_id':memory_run_id,'report_id':bundle['handoff']['report_id'],'decision_count':len(decisions),'status_counts':{s:sum(x['admission_status']==s for x in decisions) for s in sorted({x['admission_status'] for x in decisions})},'admission_decisions':[{'admission_decision_id':x['admission_decision_id'],'admission_decision_digest':x['admission_decision_digest'],'experience_id':x['experience_id'],'admission_status':x['admission_status']} for x in decisions],'source_semantics_mutated':False},'admission_bundle_digest'); dump_json(staging/'memory/admission_bundle.json',admission_bundle)
            proposals,portfolio,budget=build_proposals(memory_run_id,entries,registry,planner_policy,prior['proposal_fingerprints'])
            for x in proposals: dump_json(staging/f"planner/proposals/{x['proposal_id']}.json",x)
            dump_json(staging/'planner/plan_portfolio.json',portfolio); dump_json(staging/'planner/budget_report.json',budget)
            suppression=with_digest({'schema_version':'1.0.0','memory_run_id':memory_run_id,'prior_memory_present':prior_root is not None,'suppressed_proposal_count':portfolio['suppressed_count'],'research_duplicate_execution_prevented':portfolio['suppressed_count']>0,'automatic_execution_allowed':False},'suppression_report_digest'); dump_json(staging/'planner/duplicate_suppression_report.json',suppression)
            events=build_event_ledger(memory_run_id,[
              ('ACL08_PACKAGE_ACCEPTED',{'acl08_handoff_digest':bundle['handoff']['handoff_digest']}),
              ('MEMORY_AND_PLANNER_POLICIES_BOUND',{'memory_policy_digest':memory_policy['policy_digest'],'planner_policy_digest':planner_policy['policy_digest']}),
              ('MEMORY_POISONING_GUARD_PASSED',{'poisoning_report_digest':poisoning['poisoning_report_digest']}),
              ('DUPLICATE_EQUIVALENCE_CLASSIFIED',{'equivalence_report_digest':equiv['equivalence_report_digest']}),
              ('MEMORY_ADMISSION_DECISIONS_ISSUED',{'admission_bundle_digest':admission_bundle['admission_bundle_digest']}),
              ('GOVERNED_MEMORY_INDEX_PUBLISHED',{'memory_index_digest':index['memory_index_digest']}),
              ('BOUNDED_RESEARCH_PROPOSALS_COMPILED',{'portfolio_digest':portfolio['portfolio_digest']}),
              ('PLANNER_BUDGET_ENFORCED',{'budget_report_digest':budget['budget_report_digest']}),
              ('ACL10_HANDOFF_PREPARED',{'selected_proposal_count':portfolio['selected_count']}),
            ],processed_at); assert verify_event_ledger(events); dump_json(staging/'events/memory_event_ledger.json',events)
            provenance=build_provenance(memory_run_id,bundle,memory_policy,planner_policy,equiv,index,portfolio,events); dump_json(staging/'lineage/memory_provenance_graph.json',provenance)
            security=with_digest({'schema_version':'1.0.0','memory_run_id':memory_run_id,'network_access_allowed':False,'secret_access_allowed':False,'research_execution_allowed':False,'automatic_scheduling_allowed':False,'promotion_allowed':False,'live_order_submission_allowed':False,'capital_activation_allowed':False,'doctrine_amendment_allowed':False,'diagnostic_memory_selectable':False,'passed':True},'security_report_digest'); dump_json(staging/'security/security_boundary_report.json',security)
            integrity=with_digest({'schema_version':'1.0.0','memory_run_id':memory_run_id,'acl08_bundle_verified':True,'experience_records_verified':len(bundle['records']),'source_decisions_mutated':False,'duplicate_fingerprints_preserved':True,'memory_history_rewritten':False,'passed':True},'integrity_report_digest'); dump_json(staging/'reports/integrity_report.json',integrity)
            run=with_digest({'schema_version':'1.0.0','memory_run_id':memory_run_id,'report_id':bundle['handoff']['report_id'],'validation_id':bundle['handoff']['validation_id'],'run_id':bundle['handoff']['run_id'],'batch_id':bundle['handoff']['batch_id'],'state':'COMPLETED_NON_PROMOTIONAL','processed_at':processed_at,'service_version':SERVICE_VERSION,'claim_ceiling':CLAIM_CEILING,'input_binding_digest':binding['binding_digest'],'memory_policy_digest':memory_policy['policy_digest'],'planner_policy_digest':planner_policy['policy_digest'],'equivalence_report_digest':equiv['equivalence_report_digest'],'memory_index_digest':index['memory_index_digest'],'admission_bundle_digest':admission_bundle['admission_bundle_digest'],'portfolio_digest':portfolio['portfolio_digest'],'budget_report_digest':budget['budget_report_digest'],'source_decisions_mutated':False,'research_execution_allowed':False,'promotion_allowed':False,'live_order_submission_allowed':False,'capital_activation_allowed':False},'memory_run_digest'); dump_json(staging/'run/memory_run.json',run)
            (staging/'docs/ACL09_MEMORY_AND_PLANNER_SUMMARY.md').parent.mkdir(parents=True,exist_ok=True)
            (staging/'docs/ACL09_MEMORY_AND_PLANNER_SUMMARY.md').write_text(summary_md(run,index,portfolio,equiv),encoding='utf-8')
            (staging/'docs/GOVERNED_MEMORY_INDEX.md').write_text(memory_md(index),encoding='utf-8')
            (staging/'docs/BOUNDED_RESEARCH_PLAN.md').write_text(planner_md(portfolio),encoding='utf-8')
            (staging/'docs/DUPLICATE_AND_EQUIVALENCE.md').write_text(duplicate_md(equiv),encoding='utf-8')
            handoff=with_digest({'schema_version':'1.0.0','handoff_type':'ACL09_TO_ACL10','memory_run_id':memory_run_id,'report_id':bundle['handoff']['report_id'],'validation_id':bundle['handoff']['validation_id'],'run_id':bundle['handoff']['run_id'],'batch_id':bundle['handoff']['batch_id'],'memory_run_digest':run['memory_run_digest'],'memory_index_digest':index['memory_index_digest'],'admission_bundle_digest':admission_bundle['admission_bundle_digest'],'equivalence_report_digest':equiv['equivalence_report_digest'],'plan_portfolio_digest':portfolio['portfolio_digest'],'event_ledger_digest':events['ledger_digest'],'provenance_graph_digest':provenance['graph_digest'],'claim_ceiling':CLAIM_CEILING,'required_acl10_actions':['VERIFY_MEMORY_AND_PLANNER_PACKAGE','EVALUATE_PROMOTION_PREREQUISITES','ISSUE_NON_PROMOTIONAL_STATE_DECISION'],'forbidden_acl10_actions':['EXECUTE_RESEARCH_PLAN','MUTATE_MEMORY_HISTORY','PROMOTE_WITHOUT_VALIDATED_EVIDENCE','AUTHORIZE_EXECUTION','ACTIVATE_CAPITAL'],'reporting_eligible_candidate_count':bundle['batch'].get('reporting_eligible_count',0),'research_execution_allowed':False,'promotion_allowed':False,'live_order_submission_allowed':False,'capital_activation_allowed':False},'handoff_digest'); dump_json(staging/'handoff/acl10_handoff.json',handoff)
            manifest=build_output_manifest(staging,memory_run_id); dump_json(staging/'output_manifest.json',manifest)
            receipt=with_digest({'schema_version':'1.0.0','memory_run_id':memory_run_id,'report_id':bundle['handoff']['report_id'],'memory_run_digest':run['memory_run_digest'],'memory_index_digest':index['memory_index_digest'],'plan_portfolio_digest':portfolio['portfolio_digest'],'event_ledger_digest':events['ledger_digest'],'acl10_handoff_digest':handoff['handoff_digest'],'output_manifest_digest':manifest['manifest_digest'],'service_version':SERVICE_VERSION,'claim_ceiling':CLAIM_CEILING,'research_execution_allowed':False,'live_order_submission_allowed':False,'capital_activation_allowed':False},'receipt_digest'); dump_json(staging/'memory_receipt.json',receipt)
            atomic_publish(staging,destination)
            return {'passed':True,'memory_run_id':memory_run_id,'report_id':bundle['handoff']['report_id'],'new_memory_entry_count':index['entry_count'],'alias_count':index['alias_count'],'quarantine_count':index['quarantine_count'],'selected_proposal_count':portfolio['selected_count'],'artifact_count':manifest['artifact_count'],'handoff_digest':handoff['handoff_digest']}
        except Exception:
            if staging.exists(): shutil.rmtree(staging,ignore_errors=True)
            raise
