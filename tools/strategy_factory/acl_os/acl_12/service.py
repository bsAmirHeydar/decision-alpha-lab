from __future__ import annotations
import shutil,tempfile
from pathlib import Path
from .artifact_manifest import build_output_manifest
from .authority import validate_permit
from .canonical import stable_id,with_digest
from .controls import assess_controls
from .custody import build_key_custody_interface
from .events import build_event_ledger
from .evidence import build_evidence_bundle
from .handoff import build_handoff
from .handoff_input import load_acl11_bundle
from .io import dump_json,atomic_publish
from .obsidian import project
from .operator import build_operator_separation
from .policies import CLAIM_CEILING,SERVICE_VERSION
from .provenance import build_provenance
from .readiness import issue_readiness_decision
from .registries import security_control_registry,threat_registry,readiness_state_registry
from .response import build_incident_readiness,build_revocation_plan
from .risk import build_risk_register
from .scanners import scan_secrets,scan_paths,scan_mql5,scan_static
from .security import build_security_boundary_report
from .supply_chain import build_reference_sbom,build_dependency_recall_graph
from .threats import assess_threats
class ACL12SecurityHardeningService:
    def build(self,acl11_root:Path,permit:dict,destination:Path,hardened_at:str='2026-07-18T05:00:00Z')->dict:
        bundle=load_acl11_bundle(acl11_root); authority=validate_permit(permit,bundle['binding'])
        controls=security_control_registry(); threats=threat_registry(); states=readiness_state_registry()
        secret_scan=scan_secrets(acl11_root); path_scan=scan_paths(acl11_root); mql5_scan=scan_mql5(acl11_root); static_scan=scan_static(acl11_root)
        sbom=build_reference_sbom(acl11_root); recall=build_dependency_recall_graph(sbom,bundle['binding']); operator=build_operator_separation(); key_custody=build_key_custody_interface(bundle['signing']); incident=build_incident_readiness(); revocation=build_revocation_plan()
        artifacts={'secret_scan':secret_scan,'path_scan':path_scan,'mql5_scan':mql5_scan,'static_scan':static_scan,'sbom':sbom,'recall':recall,'operator':operator,'key_custody':key_custody,'incident':incident,'revocation':revocation}
        matrix=assess_controls(bundle,controls,artifacts,hardened_at); threat_assessment=assess_threats(threats,matrix); risk=build_risk_register(threat_assessment); evidence=build_evidence_bundle(bundle['binding'],artifacts,matrix,threat_assessment,risk); decision=issue_readiness_decision(bundle,matrix,threat_assessment,risk,evidence,hardened_at); security=build_security_boundary_report(bundle,decision,artifacts)
        run_id=stable_id('SECRUN',bundle['handoff']['runtime_custody_run_id'],matrix['assessment_digest'],decision['readiness_decision_digest'],length=32)
        run=with_digest({'schema_version':'1.0.0','security_hardening_run_id':run_id,'runtime_custody_run_id':bundle['handoff']['runtime_custody_run_id'],'promotion_run_id':bundle['handoff']['promotion_run_id'],'service_version':SERVICE_VERSION,'claim_ceiling':CLAIM_CEILING,'state':'COMPLETED_REFERENCE_HARDENING_PRODUCTION_NOT_READY','hardened_at':hardened_at,'runtime_candidate_count':0,'security_control_matrix_digest':matrix['assessment_digest'],'security_readiness_decision_digest':decision['readiness_decision_digest'],'production_security_ready':False,'runtime_activation_allowed':False,'live_order_submission_allowed':False,'capital_activation_allowed':False},'security_hardening_run_digest')
        events=build_event_ledger(run_id,hardened_at,[('ACL11_PACKAGE_ACCEPTED',{'binding_digest':bundle['binding']['binding_digest']}),('AUTHORITY_PERMIT_BOUND',{'authority_report_digest':authority['authority_report_digest']}),('SECURITY_REGISTRIES_BOUND',{'control_registry_digest':controls['registry_digest'],'threat_registry_digest':threats['registry_digest']}),('REFERENCE_SCANS_COMPLETED',{'secret_scan_digest':secret_scan['scan_digest'],'static_scan_digest':static_scan['scan_digest'],'mql5_scan_digest':mql5_scan['scan_digest']}),('SUPPLY_CHAIN_EVIDENCE_BUILT',{'sbom_digest':sbom['sbom_digest'],'recall_graph_digest':recall['graph_digest']}),('SECURITY_CONTROLS_ASSESSED',{'assessment_digest':matrix['assessment_digest']}),('THREATS_AND_RISKS_ASSESSED',{'threat_assessment_digest':threat_assessment['assessment_digest'],'risk_register_digest':risk['register_digest']}),('NON_PRODUCTION_READINESS_DECISION_ISSUED',{'readiness_decision_digest':decision['readiness_decision_digest']}),('ACL13_HANDOFF_PREPARED',{'production_security_ready':False})])
        provenance=build_provenance(bundle,matrix,evidence,decision); handoff=build_handoff(run,decision,matrix,evidence,risk,events,provenance)
        staging=Path(tempfile.mkdtemp(prefix='acl12-',dir=str(destination.parent)))
        try:
            (staging/'.acl12_generated_root').write_text('ACL12_SECURITY_HARDENING_REFERENCE\n',encoding='utf-8',newline='\n')
            outputs={'binding/acl11_binding.json':bundle['binding'],'authority/authority_report.json':authority,'registry/security_control_registry.json':controls,'registry/threat_registry.json':threats,'registry/security_readiness_state_registry.json':states,'scans/secret_scan_report.json':secret_scan,'scans/path_and_symlink_scan_report.json':path_scan,'scans/mql5_forbidden_api_scan_report.json':mql5_scan,'scans/static_scan_report.json':static_scan,'supply_chain/reference_sbom.json':sbom,'supply_chain/dependency_recall_graph.json':recall,'identity/operator_separation_matrix.json':operator,'custody/key_custody_interface.json':key_custody,'response/incident_response_readiness.json':incident,'response/revocation_quarantine_plan.json':revocation,'assessment/security_control_matrix.json':matrix,'assessment/threat_assessment.json':threat_assessment,'risk/security_risk_register.json':risk,'evidence/security_evidence_bundle.json':evidence,'decision/security_readiness_decision.json':decision,'security/security_boundary_report.json':security,'events/security_hardening_event_ledger.json':events,'lineage/security_hardening_provenance_graph.json':provenance,'run/security_hardening_run.json':run,'handoff/acl13_handoff.json':handoff}
            for rel,obj in outputs.items(): dump_json(staging/rel,obj)
            project(staging,run,decision,matrix,risk,handoff)
            integrity=with_digest({'schema_version':'1.0.0','passed':True,'acl11_package_verified':True,'runtime_candidate_invented':False,'runtime_generation_materialized':False,'production_security_evidence_invented':False,'production_key_material_accessed':False,'all_reference_scans_passed':security['scan_passed']},'integrity_report_digest'); dump_json(staging/'reports/integrity_report.json',integrity)
            manifest=build_output_manifest(staging,run_id); dump_json(staging/'output_manifest.json',manifest)
            receipt=with_digest({'schema_version':'1.0.0','security_hardening_run_id':run_id,'security_hardening_run_digest':run['security_hardening_run_digest'],'output_manifest_digest':manifest['manifest_digest'],'acl13_handoff_digest':handoff['handoff_digest'],'security_readiness_decision_digest':decision['readiness_decision_digest'],'artifact_count':manifest['artifact_count'],'reference_only':True},'receipt_digest'); dump_json(staging/'security_hardening_receipt.json',receipt)
            atomic_publish(staging,destination)
        except Exception:
            shutil.rmtree(staging,ignore_errors=True); raise
        return {'security_hardening_run_id':run_id,'decision':decision['decision'],'production_security_ready':False,'control_count':matrix['control_count'],'handoff_digest':handoff['handoff_digest']}
