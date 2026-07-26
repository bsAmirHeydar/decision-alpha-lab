from __future__ import annotations
import shutil, tempfile
from pathlib import Path
from typing import Any
from .approval_boundary import build_approval_bundle, build_dissent_bundle, build_revocation_bundle
from .artifact_manifest import build_output_manifest
from .authority import verify_authority_permit
from .canonical import stable_id, with_digest
from .decision_engine import build_decisions
from .event_ledger import build_event_ledger
from .handoff_input import load_acl09_bundle
from .io import atomic_publish, dump_json
from .obsidian_projection import project
from .policies import CLAIM_CEILING, SERVICE_VERSION
from .prerequisite_evaluator import build_matrix
from .promotion_policy import validate_promotion_policy
from .provenance import build_provenance
from .runtime_manifest import build_runtime_candidate_manifest
from .state_registry import state_registry_snapshot, transition_registry_snapshot, prerequisite_registry_snapshot, validate_registries
from .subject_projection import project_subjects

class ACL10PromotionStateService:
    def build(self, acl09_root:Path, permit:dict[str,Any], promotion_policy:dict[str,Any], destination:Path, evaluated_at:str) -> dict[str,Any]:
        bundle=load_acl09_bundle(acl09_root); policy=validate_promotion_policy(promotion_policy); authority=verify_authority_permit(permit,bundle['binding'])
        states=state_registry_snapshot(); transitions=transition_registry_snapshot(); prerequisites=prerequisite_registry_snapshot(); validate_registries(states,transitions,prerequisites)
        subject_bundle=project_subjects(bundle); matrix=build_matrix(subject_bundle,bundle,policy)
        decision_bundle,attempt_bundle,decisions,attempts=build_decisions(subject_bundle,matrix,policy,evaluated_at)
        approval_bundle=build_approval_bundle(decision_bundle,policy); dissent_bundle=build_dissent_bundle(); revocation_bundle=build_revocation_bundle(); runtime_manifest=build_runtime_candidate_manifest(decision_bundle)
        promotion_run_id=stable_id('PROMRUN',bundle['memory_run']['memory_run_id'],policy['policy_digest'],decision_bundle['decision_bundle_digest'],evaluated_at,length=32)
        run=with_digest({'schema_version':'1.0.0','promotion_run_id':promotion_run_id,'memory_run_id':bundle['memory_run']['memory_run_id'],'report_id':bundle['handoff']['report_id'],'validation_id':bundle['handoff']['validation_id'],'run_id':bundle['handoff']['run_id'],'batch_id':bundle['handoff']['batch_id'],'evaluated_at':evaluated_at,'state':'COMPLETED_NON_PROMOTIONAL','claim_ceiling':CLAIM_CEILING,'service_version':SERVICE_VERSION,'input_binding_digest':bundle['binding']['binding_digest'],'promotion_policy_digest':policy['policy_digest'],'subject_bundle_digest':subject_bundle['subject_bundle_digest'],'prerequisite_matrix_digest':matrix['matrix_digest'],'decision_bundle_digest':decision_bundle['decision_bundle_digest'],'runtime_candidate_manifest_digest':runtime_manifest['runtime_candidate_manifest_digest'],'promotion_executed':False,'runtime_generation_allowed':False,'live_order_submission_allowed':False,'capital_activation_allowed':False},'promotion_run_digest')
        events=build_event_ledger(promotion_run_id,[
            ('ACL09_PACKAGE_ACCEPTED',{'binding_digest':bundle['binding']['binding_digest']}),
            ('PROMOTION_POLICY_BOUND',{'promotion_policy_digest':policy['policy_digest']}),
            ('PROMOTION_REGISTRIES_BOUND',{'state_registry_digest':states['registry_digest'],'transition_registry_digest':transitions['registry_digest'],'prerequisite_registry_digest':prerequisites['registry_digest']}),
            ('PROMOTION_SUBJECTS_PROJECTED',{'subject_bundle_digest':subject_bundle['subject_bundle_digest']}),
            ('PROMOTION_PREREQUISITES_EVALUATED',{'prerequisite_matrix_digest':matrix['matrix_digest'],'eligible_count':matrix['eligible_count']}),
            ('PROMOTION_STATE_DECISIONS_ISSUED',{'decision_bundle_digest':decision_bundle['decision_bundle_digest']}),
            ('APPROVAL_BOUNDARY_ENFORCED',{'approval_bundle_digest':approval_bundle['approval_bundle_digest']}),
            ('RUNTIME_CANDIDATE_MANIFEST_FROZEN',{'runtime_candidate_manifest_digest':runtime_manifest['runtime_candidate_manifest_digest']}),
            ('ACL11_HANDOFF_PREPARED',{'runtime_candidate_count':runtime_manifest['runtime_candidate_count']}),
        ],evaluated_at)
        provenance=build_provenance(promotion_run_id,bundle['binding'],policy,subject_bundle,matrix,decision_bundle,runtime_manifest,events)
        handoff=with_digest({'schema_version':'1.0.0','handoff_type':'ACL10_TO_ACL11','promotion_run_id':promotion_run_id,'promotion_run_digest':run['promotion_run_digest'],'memory_run_id':bundle['memory_run']['memory_run_id'],'memory_run_digest':bundle['memory_run']['memory_run_digest'],'decision_bundle_digest':decision_bundle['decision_bundle_digest'],'runtime_candidate_manifest_digest':runtime_manifest['runtime_candidate_manifest_digest'],'event_ledger_digest':events['ledger_digest'],'provenance_graph_digest':provenance['graph_digest'],'promotion_review_eligible_count':decision_bundle['promotion_review_eligible_count'],'runtime_candidate_count':runtime_manifest['runtime_candidate_count'],'required_acl11_actions':['VERIFY_PROMOTION_STATE_PACKAGE','ASSESS_RUNTIME_PARITY_PREREQUISITES','ISSUE_NON_EXECUTABLE_RUNTIME_CUSTODY_DECISION'],'forbidden_acl11_actions':['GENERATE_RUNTIME_FOR_INELIGIBLE_SUBJECT','MUTATE_PROMOTION_DECISIONS','BYPASS_RUNTIME_PARITY_GATES','AUTHORIZE_LIVE_ORDER','ACTIVATE_CAPITAL'],'promotion_execution_allowed':False,'runtime_generation_allowed':False,'live_order_submission_allowed':False,'capital_activation_allowed':False},'handoff_digest')
        staging=Path(tempfile.mkdtemp(prefix='.acl10-staging-',dir=str(destination.parent)))
        try:
            (staging/'.acl10_generated_root').write_text('ACL-10 generated root; do not hand edit.\n', encoding='utf-8', newline='\n')
            for rel,obj in [
              ('binding/acl09_binding.json',bundle['binding']),('authority/authority_report.json',authority),('policy/promotion_policy_snapshot.json',policy),
              ('registry/state_registry_snapshot.json',states),('registry/transition_registry_snapshot.json',transitions),('registry/prerequisite_registry_snapshot.json',prerequisites),
              ('subjects/source_subject_bundle.json',subject_bundle),('evaluations/prerequisite_matrix.json',matrix),('decisions/promotion_decision_bundle.json',decision_bundle),
              ('transitions/transition_attempt_bundle.json',attempt_bundle),('approval/approval_request_bundle.json',approval_bundle),('approval/dissent_bundle.json',dissent_bundle),
              ('control/revocation_bundle.json',revocation_bundle),('runtime/runtime_candidate_manifest.json',runtime_manifest),('events/promotion_event_ledger.json',events),
              ('lineage/promotion_provenance_graph.json',provenance),('run/promotion_run.json',run),('handoff/acl11_handoff.json',handoff)]: dump_json(staging/rel,obj)
            for subject in subject_bundle['subjects']: dump_json(staging/'subjects/records'/f"{subject['subject_id']}.json",subject)
            for evaluation in matrix['evaluations']: dump_json(staging/'evaluations/records'/f"{evaluation['evaluation_id']}.json",evaluation)
            for decision in decisions: dump_json(staging/'decisions/records'/f"{decision['state_decision_id']}.json",decision)
            for attempt in attempts: dump_json(staging/'transitions/attempts'/f"{attempt['transition_attempt_id']}.json",attempt)
            state_report=with_digest({'schema_version':'1.0.0','promotion_run_id':promotion_run_id,'state_counts':decision_bundle['state_counts'],'promotion_review_eligible_count':decision_bundle['promotion_review_eligible_count'],'promotion_executed_count':0},'report_digest')
            eligibility_report=with_digest({'schema_version':'1.0.0','promotion_run_id':promotion_run_id,'source_reporting_eligible_candidate_count':bundle['handoff']['reporting_eligible_candidate_count'],'evaluated_subject_count':decision_bundle['decision_count'],'promotion_review_eligible_count':decision_bundle['promotion_review_eligible_count'],'runtime_candidate_count':runtime_manifest['runtime_candidate_count'],'passed':decision_bundle['promotion_review_eligible_count']==0 and runtime_manifest['runtime_candidate_count']==0},'report_digest')
            integrity_report=with_digest({'schema_version':'1.0.0','promotion_run_id':promotion_run_id,'acl09_bundle_verified':True,'source_memory_mutated':False,'source_decisions_mutated':False,'subject_count':subject_bundle['subject_count'],'passed':True},'integrity_report_digest')
            security_report=with_digest({'schema_version':'1.0.0','promotion_run_id':promotion_run_id,'network_access_allowed':False,'secret_access_allowed':False,'research_execution_allowed':False,'promotion_execution_allowed':False,'runtime_generation_allowed':False,'live_order_submission_allowed':False,'capital_activation_allowed':False,'self_approval_allowed':False,'passed':True},'security_report_digest')
            dump_json(staging/'reports/state_distribution_report.json',state_report); dump_json(staging/'reports/promotion_eligibility_report.json',eligibility_report); dump_json(staging/'reports/integrity_report.json',integrity_report); dump_json(staging/'security/security_boundary_report.json',security_report)
            projection=project(staging,run,decision_bundle,matrix,runtime_manifest); dump_json(staging/'docs/history/obsidian/base_projection_manifest.json',projection)
            manifest=build_output_manifest(staging,promotion_run_id); dump_json(staging/'output_manifest.json',manifest)
            receipt=with_digest({'schema_version':'1.0.0','promotion_run_id':promotion_run_id,'memory_run_id':bundle['memory_run']['memory_run_id'],'promotion_run_digest':run['promotion_run_digest'],'decision_bundle_digest':decision_bundle['decision_bundle_digest'],'runtime_candidate_manifest_digest':runtime_manifest['runtime_candidate_manifest_digest'],'event_ledger_digest':events['ledger_digest'],'acl11_handoff_digest':handoff['handoff_digest'],'output_manifest_digest':manifest['manifest_digest'],'service_version':SERVICE_VERSION,'claim_ceiling':CLAIM_CEILING,'promotion_execution_allowed':False,'runtime_generation_allowed':False,'live_order_submission_allowed':False,'capital_activation_allowed':False},'receipt_digest'); dump_json(staging/'promotion_receipt.json',receipt)
            atomic_publish(staging,destination)
            return {'passed':True,'promotion_run_id':promotion_run_id,'subject_count':subject_bundle['subject_count'],'promotion_review_eligible_count':decision_bundle['promotion_review_eligible_count'],'runtime_candidate_count':runtime_manifest['runtime_candidate_count'],'artifact_count':manifest['artifact_count'],'handoff_digest':handoff['handoff_digest']}
        except Exception:
            if staging.exists(): shutil.rmtree(staging,ignore_errors=True)
            raise
