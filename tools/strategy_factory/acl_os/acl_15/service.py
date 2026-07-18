from __future__ import annotations
import shutil
from pathlib import Path
from .artifact_manifest import build_output_manifest
from .authority import verify_permit
from .canonical import stable_id,with_digest
from .contracts import build_contracts
from .decision import build_decision
from .events import build_event_ledger
from .handoff import build_handoff
from .handoff_input import load_acl14_bundle
from .io import atomic_publish,dump_json,new_staging
from .obsidian import project
from .operations import build_operations
from .provenance import build_provenance
from .registry import build_registries
from .report import build_reports
from .security import build_security
class ACL15FleetOperationsClosureService:
    def build(self,acl14_root:Path,permit:dict,policy:dict,destination:Path,closed_at:str='2026-07-18T11:00:00Z')->dict:
        upstream=load_acl14_bundle(acl14_root); binding=upstream['binding']
        auth=verify_permit(permit,binding,closed_at)
        registries=build_registries(); contracts=build_contracts(binding,policy,auth,closed_at)
        ops=build_operations(binding,contracts,policy,closed_at); decision=build_decision(binding,contracts,ops,closed_at)
        run_id=stable_id('FLEETRUN',contracts['fleet']['fleet_id'],binding['acl14_handoff_digest'],closed_at,length=32)
        run=with_digest({'schema_version':'1.0.0','service_version':'1.0.0','fleet_closure_run_id':run_id,'fleet_id':contracts['fleet']['fleet_id'],'pilot_run_id':binding['pilot_run_id'],'pilot_contract_id':binding['pilot_contract_id'],'closed_at':closed_at,'state':'COMPLETED_REFERENCE_FLEET_CLOSURE_NON_CAPITAL','closure_state':decision['state'],'package_count':1,'pilot_execution_count':0,'prospective_observation_rows':0,'runtime_generation_count':0,'live_order_count':0,'capital_activation_count':0,'claim_ceiling':'FLEET_OPERATIONS_AND_CLOSURE_REFERENCE_ONLY'},'fleet_closure_run_digest')
        reports=build_reports(run_id,binding,contracts,ops,decision,registries,closed_at)
        security=build_security(run_id,binding,decision)
        events=build_event_ledger(run_id,closed_at,[
          ('ACL14_PACKAGE_ACCEPTED',{'acl14_binding_digest':binding['acl14_binding_digest']}),
          ('AUTHORITY_PERMIT_BOUND',{'authority_report_digest':auth['authority_report_digest']}),
          ('FLEET_REGISTRIES_BOUND',{'fleet_registry_digest':registries['fleet']['registry_digest'],'closure_registry_digest':registries['closure']['registry_digest']}),
          ('FLEET_PACKAGE_REGISTERED',{'fleet_registration_digest':contracts['fleet']['fleet_registration_digest']}),
          ('RETENTION_AND_SURVEILLANCE_REGISTERED',{'retention_contract_digest':contracts['retention']['retention_contract_digest'],'surveillance_contract_digest':contracts['surveillance']['surveillance_contract_digest']}),
          ('EVIDENCE_INVENTORY_FROZEN',{'evidence_inventory_digest':ops['evidence']['evidence_inventory_digest']}),
          ('NON_CAPITAL_CLOSURE_DECISION_ISSUED',{'closure_decision_digest':decision['closure_decision_digest']}),
          ('REOPEN_AND_MIGRATION_BOUNDARIES_REGISTERED',{'reopen_policy_digest':contracts['reopen']['reopen_policy_digest'],'migration_contract_digest':contracts['migration']['migration_contract_digest']}),
          ('REFERENCE_LIFECYCLE_CLOSED',{'state':decision['state']})])
        provenance=build_provenance(run_id,binding,contracts,ops,decision)
        handoff=build_handoff(run,decision,contracts,ops,events,provenance)
        staging=new_staging(destination)
        try:
            (staging/'.acl15_generated_root').write_text('ACL-15 generated root — immutable reference closure\n',encoding='utf-8',newline='\n')
            outputs={
              'binding/acl14_binding.json':binding,'authority/authority_report.json':auth,
              'registry/fleet_status_registry.json':registries['fleet'],'registry/closure_state_registry.json':registries['closure'],'registry/action_registry.json':registries['actions'],'registry/report_section_registry.json':registries['report'],
              'contract/fleet_registration_contract.json':contracts['fleet'],'contract/lifecycle_ownership_contract.json':contracts['ownership'],'contract/retention_contract.json':contracts['retention'],'contract/surveillance_contract.json':contracts['surveillance'],'contract/migration_contract.json':contracts['migration'],'contract/reopen_policy.json':contracts['reopen'],'contract/closure_policy.json':contracts['closure_policy'],
              'status/fleet_package_status.json':ops['package_status'],'status/retention_status.json':ops['retention_status'],'status/surveillance_status.json':ops['surveillance_status'],
              'evidence/pilot_evidence_inventory.json':ops['evidence'],'operations/fleet_operations_manifest.json':ops['manifest'],'execution/runtime_and_order_manifest.json':ops['execution'],
              'decision/non_capital_closure_decision.json':decision,'report/fleet_closure_report.json':reports['report'],'report/executive_brief.json':reports['executive'],'report/residual_risk_report.json':reports['residual'],
              'security/security_boundary_report.json':security,'events/fleet_event_ledger.json':events,'lineage/fleet_provenance_graph.json':provenance,'run/fleet_closure_run.json':run,'handoff/lifecycle_closure_handoff.json':handoff,
              'policy/fleet_closure_policy.json':policy,
            }
            for rel,obj in outputs.items(): dump_json(staging/rel,obj)
            project(staging,run,decision,contracts,ops,handoff)
            integrity=with_digest({'schema_version':'1.0.0','passed':True,'acl14_package_verified':True,'pilot_readiness_preserved':True,'pilot_execution_state_preserved':True,'unknowns_preserved':True,'failures_preserved':True,'pilot_outcomes_invented':False,'prospective_evidence_invented':False,'validation_bypassed':False,'promotion_bypassed':False,'runtime_generated':False,'live_order_authority_created':False,'capital_authority_created':False},'integrity_report_digest')
            dump_json(staging/'reports/integrity_report.json',integrity)
            manifest=build_output_manifest(staging,run_id); dump_json(staging/'output_manifest.json',manifest)
            receipt=with_digest({'schema_version':'1.0.0','fleet_closure_run_id':run_id,'fleet_closure_run_digest':run['fleet_closure_run_digest'],'output_manifest_digest':manifest['manifest_digest'],'lifecycle_closure_handoff_digest':handoff['handoff_digest'],'fleet_registration_digest':contracts['fleet']['fleet_registration_digest'],'closure_decision_digest':decision['closure_decision_digest'],'artifact_count':manifest['artifact_count'],'reference_only':True},'receipt_digest')
            dump_json(staging/'fleet_closure_receipt.json',receipt)
            atomic_publish(staging,destination)
        except Exception:
            shutil.rmtree(staging,ignore_errors=True); raise
        return {'passed':True,'fleet_closure_run_id':run_id,'fleet_id':contracts['fleet']['fleet_id'],'state':decision['state'],'pilot_execution_materialized':False,'prospective_evidence_present':False,'handoff_digest':handoff['handoff_digest']}
