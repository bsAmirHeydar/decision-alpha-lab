from __future__ import annotations
import shutil,tempfile
from pathlib import Path
from .artifact_manifest import build_output_manifest
from .authority import validate_permit
from .baselines import build_baselines
from .budget import validate_budget,usage_report
from .canonical import stable_id,with_digest
from .completeness import assess_completeness
from .decision import issue_decision
from .discovery import build_catalog
from .events import build_event_ledger
from .evidence import build_evidence
from .handoff import build_handoff
from .handoff_input import load_acl12_bundle
from .input_contract import validate_request
from .io import dump_json,atomic_publish
from .obsidian import project
from .policies import CLAIM_CEILING,SERVICE_VERSION,SECTION_IDS
from .provenance import build_provenance
from .report import build_report
from .security import build_security
from .slice import build_fast_slice
from .support import build_support
from .uncertainty import build_uncertainty
from .value import build_value
class ACL13OneHourAssessmentService:
    def build(self,acl12_root:Path,permit:dict,request:dict,budget_profile:dict,destination:Path,assessed_at:str='2026-07-18T06:00:00Z')->dict:
        bundle=load_acl12_bundle(acl12_root); authority=validate_permit(permit,bundle['binding']); input_validation=validate_request(request); budget_validation=validate_budget(budget_profile,request)
        slice_doc=build_fast_slice(request); completeness=assess_completeness(request,bundle['binding']); support=build_support(slice_doc); baselines=build_baselines(slice_doc,budget_profile['max_random_trials']); catalog=build_catalog(request,slice_doc); value=build_value(slice_doc,support,baselines,catalog); uncertainty=build_uncertainty(request,bundle['binding'],support,baselines); budget=usage_report(budget_profile,request,baselines['trial_count'])
        evidence=build_evidence(bundle['binding'],request,[input_validation,budget_validation,slice_doc,completeness,support,baselines,catalog,value,uncertainty,budget]); decision=issue_decision(request,completeness,support,value,uncertainty,assessed_at)
        sections={'IDENTITY_AND_SCOPE':input_validation,'INPUT_COMPLETENESS':completeness,'SECURITY_READINESS':bundle['binding'],'FAST_DATA_SLICE':slice_doc,'SUPPORT_DIAGNOSTICS':support,'CONSTRAINED_BASELINES':baselines,'SETUP_FAMILY_DISCOVERY':catalog,'VALUE_DECOMPOSITION':value,'UNCERTAINTY':uncertainty,'FAILURE_SIGNATURES':uncertainty,'LIMITATIONS':uncertainty,'NEXT_ALLOWED_ACTIONS':decision}
        report,executive=build_report(request,bundle['binding'],sections,decision,budget,assessed_at); security=build_security(bundle['binding'],decision)
        run_id=stable_id('TRIAGERUN',request['assessment_request_id'],report['report_digest'],decision['assessment_result_digest'],length=32)
        run=with_digest({'schema_version':'1.0.0','assessment_run_id':run_id,'security_hardening_run_id':bundle['binding']['security_hardening_run_id'],'context_id':request['context_id'],'context_version':request['context_version'],'service_version':SERVICE_VERSION,'claim_ceiling':CLAIM_CEILING,'state':'COMPLETED_BOUNDED_RESEARCH_TRIAGE','assessed_at':assessed_at,'decision':decision['decision'],'report_id':report['report_id'],'observation_count':slice_doc['row_count'],'context_occurrence_count':support['context_occurrences'],'setup_family_count':catalog['family_count'],'first_real_context_pilot_design_allowed':decision['first_real_context_pilot_design_allowed'],'first_real_context_pilot_execution_allowed':False,'validation_claim_allowed':False,'alpha_claim_allowed':False,'production_security_ready':False,'runtime_activation_allowed':False,'live_order_submission_allowed':False,'capital_activation_allowed':False},'assessment_run_digest')
        events=build_event_ledger(run_id,assessed_at,[('ACL12_SECURITY_PACKAGE_ACCEPTED',{'binding_digest':bundle['binding']['binding_digest']}),('AUTHORITY_AND_BUDGET_BOUND',{'authority_report_digest':authority['authority_report_digest'],'budget_validation_digest':budget_validation['budget_validation_digest']}),('INPUT_CONTRACT_VALIDATED',{'input_validation_digest':input_validation['input_validation_digest']}),('FAST_DATA_SLICE_MATERIALIZED',{'slice_digest':slice_doc['slice_digest']}),('SUPPORT_AND_BASELINES_COMPUTED',{'support_digest':support['support_diagnostics_digest'],'baseline_digest':baselines['baseline_report_digest']}),('SETUP_FAMILIES_AND_VALUE_ASSESSED',{'catalog_digest':catalog['catalog_digest'],'value_digest':value['value_decomposition_digest']}),('NON_CAPITAL_TRIAGE_DECISION_ISSUED',{'assessment_result_digest':decision['assessment_result_digest']}),('ONE_HOUR_REPORT_BUILT',{'report_digest':report['report_digest']}),('ACL14_HANDOFF_PREPARED',{'pilot_design_allowed':decision['first_real_context_pilot_design_allowed'],'pilot_execution_allowed':False})])
        provenance=build_provenance(bundle['binding'],request,slice_doc,evidence,decision,report); handoff=build_handoff(run,decision,report,evidence,budget,events,provenance)
        staging=Path(tempfile.mkdtemp(prefix='acl13-',dir=str(destination.parent)))
        try:
            (staging/'.acl13_generated_root').write_text('ACL13_ONE_HOUR_ASSESSMENT_REFERENCE\n',encoding='utf-8',newline='\n')
            section_registry=with_digest({'schema_version':'1.0.0','registry_id':'ACL13_REPORT_SECTION_REGISTRY_V1','closed':True,'section_count':len(SECTION_IDS),'sections':[{'section_id':x,'version':'1.0.0','required':True} for x in SECTION_IDS]},'registry_digest')
            state_registry=with_digest({'schema_version':'1.0.0','registry_id':'ACL13_TRIAGE_STATE_REGISTRY_V1','closed':True,'states':['INPUT_REJECTED','BOUNDED_TRIAGE_COMPLETE_PILOT_DESIGN_ELIGIBLE_NON_CAPITAL','BOUNDED_TRIAGE_COMPLETE_ESCALATION_REQUIRED','INSUFFICIENT_INPUT_FOR_TRIAGE']},'registry_digest')
            outputs={'binding/acl12_binding.json':bundle['binding'],'authority/authority_report.json':authority,'input/assessment_request.json':request,'input/input_validation_report.json':input_validation,'policy/one_hour_budget_profile.json':budget_profile,'budget/budget_validation_report.json':budget_validation,'budget/budget_usage_report.json':budget,'registry/report_section_registry.json':section_registry,'registry/triage_state_registry.json':state_registry,'slice/fast_data_slice.json':slice_doc,'diagnostics/input_completeness_report.json':completeness,'diagnostics/support_diagnostics.json':support,'baselines/constrained_random_baseline.json':baselines,'discovery/setup_family_catalog.json':catalog,'value/context_value_decomposition.json':value,'uncertainty/uncertainty_and_limitations.json':uncertainty,'evidence/one_hour_evidence_bundle.json':evidence,'decision/one_hour_assessment_result.json':decision,'report/one_hour_assessment_report.json':report,'report/executive_summary.json':executive,'security/security_boundary_report.json':security,'events/one_hour_assessment_event_ledger.json':events,'lineage/one_hour_assessment_provenance_graph.json':provenance,'run/one_hour_assessment_run.json':run,'handoff/acl14_handoff.json':handoff}
            for rel,obj in outputs.items(): dump_json(staging/rel,obj)
            project(staging,run,report,executive,support,baselines,catalog,uncertainty,handoff)
            integrity=with_digest({'schema_version':'1.0.0','passed':True,'acl12_package_verified':True,'request_known_time_safe':True,'budget_breached':False,'synthetic_reference_disclosed':request.get('synthetic_reference_data',False),'production_security_reinterpreted':False,'validation_evidence_invented':False,'runtime_candidate_invented':False,'pilot_execution_authority_created':False,'live_order_authority_created':False,'capital_authority_created':False},'integrity_report_digest'); dump_json(staging/'reports/integrity_report.json',integrity)
            manifest=build_output_manifest(staging,run_id); dump_json(staging/'output_manifest.json',manifest)
            receipt=with_digest({'schema_version':'1.0.0','assessment_run_id':run_id,'assessment_run_digest':run['assessment_run_digest'],'output_manifest_digest':manifest['manifest_digest'],'acl14_handoff_digest':handoff['handoff_digest'],'assessment_result_digest':decision['assessment_result_digest'],'report_digest':report['report_digest'],'artifact_count':manifest['artifact_count'],'reference_only':True},'receipt_digest'); dump_json(staging/'one_hour_assessment_receipt.json',receipt)
            atomic_publish(staging,destination)
        except Exception:
            shutil.rmtree(staging,ignore_errors=True); raise
        return {'assessment_run_id':run_id,'report_id':report['report_id'],'decision':decision['decision'],'pilot_design_allowed':decision['first_real_context_pilot_design_allowed'],'pilot_execution_allowed':False,'passed':True,'handoff_digest':handoff['handoff_digest']}
