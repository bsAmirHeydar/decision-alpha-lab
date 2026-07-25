from __future__ import annotations
from .canonical import content_id,digest_object
from .errors import AuthorityError
from .registries import AUTHORITY_ACTION

def build_permit(source_handoff_digest: str, identity_run_id: str, issued_at: str):
    p={'schema_version':'1.0.0','phase_id':'LCM-04','action':AUTHORITY_ACTION,
       'identity_run_id':identity_run_id,'source_handoff_digest':source_handoff_digest,
       'issued_at':issued_at,'expires_at':'2027-07-19T00:00:00Z',
       'permit_id':content_id('LCM04PERMIT',{'h':source_handoff_digest,'i':identity_run_id,'t':issued_at}),
       'characterization_packet_build_allowed':True,'golden_case_registration_allowed':True,
       'reference_harness_execution_allowed':True,'legacy_trace_execution_allowed':False,
       'source_instrumentation_mutation_allowed':False,'source_move_allowed':False,
       'source_delete_allowed':False,'semantic_refactor_allowed':False,'merge_allowed':False,
       'cutover_allowed':False,'runtime_authority':False,'live_order_authority':False,
       'capital_authority':False,'permit_digest':None}
    p['permit_digest']=digest_object(p,'permit_digest');return p

def verify_permit(p,source_handoff_digest):
    if p.get('permit_digest')!=digest_object(p,'permit_digest'): raise AuthorityError('permit digest mismatch')
    if p.get('action')!=AUTHORITY_ACTION or p.get('source_handoff_digest')!=source_handoff_digest: raise AuthorityError('permit binding mismatch')
    denied=['legacy_trace_execution_allowed','source_instrumentation_mutation_allowed','source_move_allowed','source_delete_allowed','semantic_refactor_allowed','merge_allowed','cutover_allowed','runtime_authority','live_order_authority','capital_authority']
    if any(p.get(k) for k in denied): raise AuthorityError('authority escalation')
    return True
