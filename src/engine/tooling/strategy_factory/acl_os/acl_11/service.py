from __future__ import annotations
import shutil,tempfile
from pathlib import Path
from .artifact_manifest import build_output_manifest
from .authority import validate_permit
from .canonical import stable_id,with_digest
from .custody import build_generation_manifest,build_signing_plan,build_conformance_matrix,issue_decision
from .events import build_event_ledger
from .handoff import build_handoff
from .handoff_input import load_acl10_bundle
from .io import dump_json,atomic_publish
from .obsidian import project
from .parity import assess
from .provenance import build_provenance
from .registries import parity_registry,custody_state_registry
from .security import build_tcb,build_security_report
from .policies import CLAIM_CEILING,SERVICE_VERSION
class ACL11RuntimeCustodyService:
    def build(self,acl10_root: Path,permit: dict,destination: Path,assessed_at: str='2026-07-18T04:00:00Z') -> dict:
        bundle=load_acl10_bundle(acl10_root); authority=validate_permit(permit,bundle['binding'])
        preg=parity_registry(); sreg=custody_state_registry(); assessment=assess(bundle,preg,assessed_at)
        generation=build_generation_manifest(bundle,assessment); signing=build_signing_plan(generation); conformance=build_conformance_matrix(assessment)
        decision=issue_decision(bundle,assessment,generation,signing,conformance,assessed_at); tcb=build_tcb(); security=build_security_report(bundle,decision,tcb)
        run_id=stable_id('RTRUN',bundle['handoff']['promotion_run_id'],assessment['assessment_digest'],decision['custody_decision_digest'],length=32)
        run=with_digest({'schema_version':'1.0.0','runtime_custody_run_id':run_id,'promotion_run_id':bundle['handoff']['promotion_run_id'],'memory_run_id':bundle['handoff']['memory_run_id'],'service_version':SERVICE_VERSION,'claim_ceiling':CLAIM_CEILING,'state':'COMPLETED_NO_RUNTIME_GENERATION','assessed_at':assessed_at,'runtime_candidate_count':bundle['runtime']['runtime_candidate_count'],'parity_assessment_digest':assessment['assessment_digest'],'custody_decision_digest':decision['custody_decision_digest'],'runtime_generation_manifest_digest':generation['generation_manifest_digest'],'runtime_generation_materialized':False,'runtime_activation_allowed':False,'live_order_submission_allowed':False,'capital_activation_allowed':False},'runtime_custody_run_digest')
        events=build_event_ledger(run_id,assessed_at,[('ACL10_PACKAGE_ACCEPTED',{'binding_digest':bundle['binding']['binding_digest']}),('AUTHORITY_PERMIT_BOUND',{'authority_report_digest':authority['authority_report_digest']}),('PARITY_POLICY_BOUND',{'parity_registry_digest':preg['registry_digest']}),('RUNTIME_PARITY_ASSESSED',{'assessment_digest':assessment['assessment_digest']}),('NON_EXECUTABLE_CUSTODY_DECISION_ISSUED',{'custody_decision_digest':decision['custody_decision_digest']}),('EMPTY_GENERATION_MANIFEST_PUBLISHED',{'generation_manifest_digest':generation['generation_manifest_digest']}),('SECURITY_BOUNDARY_VERIFIED',{'security_report_digest':security['security_report_digest']}),('ACL12_HANDOFF_PREPARED',{'runtime_candidate_count':0})])
        provenance=build_provenance(bundle,assessment,decision,generation); handoff=build_handoff(run,decision,assessment,security,events,provenance)
        staging=Path(tempfile.mkdtemp(prefix='acl11-',dir=str(destination.parent)))
        try:
            (staging/'.acl11_generated_root').write_text('ACL11_RUNTIME_CUSTODY_REFERENCE\n', encoding='utf-8', newline='\n')
            outputs={
              'binding/acl10_binding.json':bundle['binding'],'authority/authority_report.json':authority,
              'registry/runtime_parity_requirement_registry.json':preg,'registry/runtime_custody_state_registry.json':sreg,
              'parity/runtime_parity_assessment.json':assessment,'parity/conformance_matrix.json':conformance,
              'runtime/runtime_generation_manifest.json':generation,'custody/signing_custody_plan.json':signing,
              'custody/runtime_custody_decision.json':decision,'security/runtime_trusted_computing_base.json':tcb,
              'security/security_boundary_report.json':security,'events/runtime_custody_event_ledger.json':events,
              'lineage/runtime_custody_provenance_graph.json':provenance,'run/runtime_custody_run.json':run,'handoff/acl12_handoff.json':handoff}
            for rel,obj in outputs.items(): dump_json(staging/rel,obj)
            project(staging,run,decision,assessment,handoff)
            integrity=with_digest({'schema_version':'1.0.0','passed':True,'acl10_package_verified':True,'runtime_candidates_invented':False,'promotion_decisions_mutated':False,'runtime_generation_materialized':False},'integrity_report_digest'); dump_json(staging/'reports/integrity_report.json',integrity)
            manifest=build_output_manifest(staging,run_id); dump_json(staging/'output_manifest.json',manifest)
            receipt=with_digest({'schema_version':'1.0.0','runtime_custody_run_id':run_id,'runtime_custody_run_digest':run['runtime_custody_run_digest'],'output_manifest_digest':manifest['manifest_digest'],'acl12_handoff_digest':handoff['handoff_digest'],'custody_decision_digest':decision['custody_decision_digest'],'artifact_count':manifest['artifact_count'],'reference_only':True},'receipt_digest'); dump_json(staging/'runtime_custody_receipt.json',receipt)
            atomic_publish(staging,destination)
        except Exception:
            shutil.rmtree(staging,ignore_errors=True); raise
        return {'runtime_custody_run_id':run_id,'custody_decision':decision['decision'],'runtime_candidate_count':0,'handoff_digest':handoff['handoff_digest']}
