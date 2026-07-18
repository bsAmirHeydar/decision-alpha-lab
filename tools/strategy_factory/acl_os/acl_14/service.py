from __future__ import annotations
import shutil,tempfile
from pathlib import Path
from .artifact_manifest import build_output_manifest
from .authority import validate_permit
from .canonical import stable_id,with_digest
from .contracts import build_contracts
from .decision import issue
from .events import build_event_ledger
from .execution import build_manifest
from .handoff import build as build_handoff
from .handoff_input import load_acl13_bundle
from .io import dump_json,atomic_publish
from .obsidian import project
from .policies import CLAIM_CEILING,SERVICE_VERSION,GATE_IDS,READINESS_STATES,SECTION_IDS
from .provenance import build as build_provenance
from .readiness import assess
from .report import build as build_report
from .request import validate_request
from .security import build as build_security

class ACL14FirstRealContextPilotService:
    def build(self,acl13_root:Path,permit:dict,request:dict,pilot_policy:dict,destination:Path,assessed_at:str='2026-07-18T10:00:00Z')->dict:
        bundle=load_acl13_bundle(acl13_root)
        authority=validate_permit(permit,bundle['binding'])
        input_validation=validate_request(request,bundle['binding'])
        if pilot_policy.get('policy_id')!='ACL14_FIRST_REAL_CONTEXT_PILOT_POLICY_V1' or pilot_policy.get('closed') is not True:
            raise ValueError('ACL14_POLICY_INVALID')
        contracts=build_contracts(request,pilot_policy,authority)
        readiness=assess(bundle['binding'],request,contracts)
        execution=build_manifest(request,contracts['contract'],readiness)
        decision=issue(request,readiness,assessed_at)
        report,executive=build_report(request,bundle['binding'],contracts,readiness,decision,execution,assessed_at)
        security=build_security(bundle['binding'],decision)
        run_id=stable_id('PILOTRUN',request['pilot_request_id'],contracts['contract']['pilot_contract_digest'],decision['pilot_readiness_decision_digest'],length=32)
        run=with_digest({
            'schema_version':'1.0.0','pilot_run_id':run_id,'assessment_run_id':bundle['binding']['assessment_run_id'],
            'pilot_contract_id':contracts['contract']['pilot_contract_id'],'service_version':SERVICE_VERSION,
            'claim_ceiling':CLAIM_CEILING,'state':'COMPLETED_PILOT_CONTRACT_AND_READINESS_ASSESSMENT',
            'assessed_at':assessed_at,'readiness_state':decision['state'],'gate_count':len(GATE_IDS),
            'satisfied_gate_count':readiness['status_counts']['SATISFIED'],'unknown_gate_count':readiness['status_counts']['UNKNOWN'],
            'unsatisfied_gate_count':readiness['status_counts']['UNSATISFIED'],'pilot_ready_non_capital':decision['pilot_ready_non_capital'],
            'pilot_execution_materialized':False,'prospective_evidence_present':False,'validation_claim_allowed':False,
            'alpha_claim_allowed':False,'production_security_ready':False,'runtime_activation_allowed':False,
            'live_order_submission_allowed':False,'capital_activation_allowed':False,
        },'pilot_run_digest')
        events=build_event_ledger(run_id,assessed_at,[
            ('ACL13_PACKAGE_ACCEPTED',{'binding_digest':bundle['binding']['binding_digest']}),
            ('AUTHORITY_AND_POLICY_BOUND',{'authority_report_digest':authority['authority_report_digest'],'policy_id':pilot_policy['policy_id']}),
            ('PILOT_REQUEST_VALIDATED',{'input_validation_digest':input_validation['input_validation_digest']}),
            ('PILOT_CONTRACT_AUTHORED',{'pilot_contract_digest':contracts['contract']['pilot_contract_digest']}),
            ('READINESS_GATES_ASSESSED',{'readiness_matrix_digest':readiness['readiness_matrix_digest']}),
            ('NON_CAPITAL_READINESS_DECISION_ISSUED',{'decision_digest':decision['pilot_readiness_decision_digest']}),
            ('EMPTY_EXECUTION_MANIFEST_PUBLISHED',{'execution_manifest_digest':execution['pilot_execution_manifest_digest']}),
            ('SECURITY_BOUNDARY_VERIFIED',{'security_report_digest':security['security_report_digest']}),
            ('ACL15_HANDOFF_PREPARED',{'pilot_ready_non_capital':decision['pilot_ready_non_capital'],'pilot_execution_materialized':False}),
        ])
        provenance=build_provenance(bundle['binding'],request,contracts['contract'],readiness,decision,execution)
        handoff=build_handoff(run,decision,contracts['contract'],readiness,execution,events,provenance)
        staging=Path(tempfile.mkdtemp(prefix='acl14-',dir=str(destination.parent)))
        try:
            (staging/'.acl14_generated_root').write_text('ACL14_FIRST_REAL_CONTEXT_PILOT_REFERENCE\n',encoding='utf-8',newline='\n')
            gate_registry=with_digest({'schema_version':'1.0.0','registry_id':'ACL14_PILOT_READINESS_GATE_REGISTRY_V1','closed':True,'gate_count':len(GATE_IDS),'gates':[{'gate_id':x,'version':'1.0.0','unknown_blocks_readiness':True} for x in GATE_IDS]},'registry_digest')
            state_registry=with_digest({'schema_version':'1.0.0','registry_id':'ACL14_PILOT_READINESS_STATE_REGISTRY_V1','closed':True,'states':sorted(READINESS_STATES)},'registry_digest')
            section_registry=with_digest({'schema_version':'1.0.0','registry_id':'ACL14_REPORT_SECTION_REGISTRY_V1','closed':True,'section_count':len(SECTION_IDS),'sections':[{'section_id':x,'required':True,'version':'1.0.0'} for x in SECTION_IDS]},'registry_digest')
            evidence_classification=with_digest({'schema_version':'1.0.0','pilot_request_id':request['pilot_request_id'],'classification':request['evidence_classification'],'real_context_evidence_present':request['real_context_evidence_present'],'reference_fixture_not_real_market_evidence':True,'synthetic_or_reference_reuse_as_real':False,'prospective_outcomes_present':False},'evidence_classification_digest')
            outputs={
                'binding/acl13_binding.json':bundle['binding'],'authority/authority_report.json':authority,
                'input/pilot_request.json':request,'input/pilot_input_validation_report.json':input_validation,
                'policy/pilot_policy.json':pilot_policy,'registry/readiness_gate_registry.json':gate_registry,
                'registry/readiness_state_registry.json':state_registry,'registry/report_section_registry.json':section_registry,
                'contract/context_owner_approval_bundle.json':contracts['owner'],'contract/data_mapping_contract.json':contracts['mapping'],
                'contract/availability_semantics_contract.json':contracts['availability'],'contract/evaluation_freeze_contract.json':contracts['evaluation'],
                'contract/search_space_freeze.json':contracts['search'],'contract/support_target_contract.json':contracts['support'],
                'contract/stop_condition_contract.json':contracts['stop'],'contract/failure_condition_contract.json':contracts['failure'],
                'contract/non_capital_boundary_contract.json':contracts['boundary'],'contract/first_real_context_pilot_contract.json':contracts['contract'],
                'assessment/evidence_classification_report.json':evidence_classification,'assessment/pilot_readiness_matrix.json':readiness,
                'decision/pilot_readiness_decision.json':decision,'execution/pilot_execution_manifest.json':execution,
                'report/pilot_design_report.json':report,'report/executive_brief.json':executive,
                'security/security_boundary_report.json':security,'events/pilot_event_ledger.json':events,
                'lineage/pilot_provenance_graph.json':provenance,'run/pilot_run.json':run,'handoff/acl15_handoff.json':handoff,
            }
            for rel,obj in outputs.items(): dump_json(staging/rel,obj)
            project(staging,run,request,contracts['contract'],readiness,decision,report,handoff)
            integrity=with_digest({'schema_version':'1.0.0','passed':True,'acl13_package_verified':True,'pilot_request_verified':True,'reference_fixture_not_real_market_evidence':True,'real_context_evidence_invented':False,'prospective_evidence_invented':False,'validation_evidence_invented':False,'pilot_execution_materialized':False,'runtime_authority_created':False,'live_order_authority_created':False,'capital_authority_created':False},'integrity_report_digest')
            dump_json(staging/'reports/integrity_report.json',integrity)
            manifest=build_output_manifest(staging,run_id)
            dump_json(staging/'output_manifest.json',manifest)
            receipt=with_digest({'schema_version':'1.0.0','pilot_run_id':run_id,'pilot_run_digest':run['pilot_run_digest'],'output_manifest_digest':manifest['manifest_digest'],'acl15_handoff_digest':handoff['handoff_digest'],'pilot_contract_digest':contracts['contract']['pilot_contract_digest'],'pilot_readiness_decision_digest':decision['pilot_readiness_decision_digest'],'artifact_count':manifest['artifact_count'],'reference_only':True},'receipt_digest')
            dump_json(staging/'first_real_context_pilot_receipt.json',receipt)
            atomic_publish(staging,destination)
        except Exception:
            shutil.rmtree(staging,ignore_errors=True)
            raise
        return {'passed':True,'pilot_run_id':run_id,'pilot_contract_id':contracts['contract']['pilot_contract_id'],'state':decision['state'],'pilot_ready_non_capital':decision['pilot_ready_non_capital'],'pilot_execution_materialized':False,'handoff_digest':handoff['handoff_digest']}
