from __future__ import annotations
from pathlib import Path
from typing import Any
from .artifact_manifest import verify_output_manifest
from .canonical import verify_embedded_digest,with_digest
from .errors import IntegrityError
from .io import load_json
from .policies import HANDOFF_IN,REQUIRED_UPSTREAM_ACTIONS,FORBIDDEN_UPSTREAM_ACTIONS
def req(v: bool,code: str) -> None:
    if not v: raise IntegrityError(code)
def load_acl10_bundle(root: Path) -> dict[str,Any]:
    req((root/'.acl10_generated_root').is_file(),'ACL10_MARKER_MISSING')
    paths={
      'manifest':'output_manifest.json','receipt':'promotion_receipt.json','handoff':'handoff/acl11_handoff.json',
      'run':'run/promotion_run.json','decisions':'decisions/promotion_decision_bundle.json','matrix':'evaluations/prerequisite_matrix.json',
      'runtime':'runtime/runtime_candidate_manifest.json','events':'events/promotion_event_ledger.json','provenance':'lineage/promotion_provenance_graph.json',
      'security':'security/security_boundary_report.json','integrity':'reports/integrity_report.json','subjects':'subjects/source_subject_bundle.json'}
    d={k:load_json(root/v) for k,v in paths.items()}
    req(verify_output_manifest(root,d['manifest']),'ACL10_MANIFEST_INVALID')
    checks=[('receipt','receipt_digest'),('handoff','handoff_digest'),('run','promotion_run_digest'),('decisions','decision_bundle_digest'),('matrix','matrix_digest'),('runtime','runtime_candidate_manifest_digest'),('events','ledger_digest'),('provenance','graph_digest'),('security','security_report_digest'),('integrity','integrity_report_digest'),('subjects','subject_bundle_digest')]
    for key,field in checks: req(verify_embedded_digest(d[key],field),f'ACL10_{key.upper()}_DIGEST_INVALID')
    h=d['handoff']
    req(h.get('handoff_type')==HANDOFF_IN,'ACL10_HANDOFF_TYPE_INVALID')
    req(set(h.get('required_acl11_actions',[]))==REQUIRED_UPSTREAM_ACTIONS,'ACL10_REQUIRED_ACTIONS_INVALID')
    req(set(h.get('forbidden_acl11_actions',[]))==FORBIDDEN_UPSTREAM_ACTIONS,'ACL10_FORBIDDEN_ACTIONS_INVALID')
    req(h['promotion_run_digest']==d['run']['promotion_run_digest'],'ACL10_RUN_BINDING_MISMATCH')
    req(h['decision_bundle_digest']==d['decisions']['decision_bundle_digest'],'ACL10_DECISION_BINDING_MISMATCH')
    req(h['runtime_candidate_manifest_digest']==d['runtime']['runtime_candidate_manifest_digest'],'ACL10_RUNTIME_BINDING_MISMATCH')
    req(d['receipt']['output_manifest_digest']==d['manifest']['manifest_digest'],'ACL10_RECEIPT_MANIFEST_MISMATCH')
    req(d['receipt']['acl11_handoff_digest']==h['handoff_digest'],'ACL10_RECEIPT_HANDOFF_MISMATCH')
    req(d['run'].get('state')=='COMPLETED_NON_PROMOTIONAL','ACL10_RUN_STATE_INVALID')
    req(d['run'].get('promotion_executed') is False,'ACL10_PROMOTION_EXECUTED')
    req(d['runtime'].get('runtime_candidate_count')==len(d['runtime'].get('runtime_candidates',[])),'ACL10_RUNTIME_COUNT_MISMATCH')
    req(d['runtime'].get('runtime_generation_allowed') is False,'ACL10_RUNTIME_GENERATION_ESCALATION')
    req(not any([h.get('promotion_execution_allowed'),h.get('runtime_generation_allowed'),h.get('live_order_submission_allowed'),h.get('capital_activation_allowed')]),'ACL10_AUTHORITY_ESCALATION')
    req(d['security'].get('passed') is True and d['integrity'].get('passed') is True,'ACL10_SECURITY_OR_INTEGRITY_FAILED')
    req(d['provenance'].get('source_decisions_mutated') is False,'ACL10_DECISIONS_MUTATED')
    for item in d['decisions'].get('decisions',[]):
        p=root/'decisions/records'/f"{item['state_decision_id']}.json"; req(p.is_file(), 'ACL10_STATE_DECISION_FILE_MISSING')
        doc=load_json(p); req(verify_embedded_digest(doc,'state_decision_digest'),'ACL10_STATE_DECISION_INVALID')
        req(doc['state_decision_digest']==item['state_decision_digest'],'ACL10_STATE_DECISION_INDEX_MISMATCH')
    body={'schema_version':'1.0.0','promotion_run_id':h['promotion_run_id'],'memory_run_id':h['memory_run_id'],'handoff_digest':h['handoff_digest'],'promotion_run_digest':d['run']['promotion_run_digest'],'decision_bundle_digest':d['decisions']['decision_bundle_digest'],'prerequisite_matrix_digest':d['matrix']['matrix_digest'],'runtime_candidate_manifest_digest':d['runtime']['runtime_candidate_manifest_digest'],'runtime_candidate_count':d['runtime']['runtime_candidate_count'],'promotion_review_eligible_count':h['promotion_review_eligible_count'],'event_ledger_digest':d['events']['ledger_digest'],'provenance_graph_digest':d['provenance']['graph_digest']}
    d['binding']=with_digest(body,'binding_digest'); return d
