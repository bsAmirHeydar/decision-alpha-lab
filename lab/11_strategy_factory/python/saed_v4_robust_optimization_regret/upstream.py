from __future__ import annotations
from .contracts import UpstreamIntakeContract
from .errors import UpstreamError
from .canonical import content_hash

def validate_upstream(intake,certificate,registry,exposure,handoff):
    c=UpstreamIntakeContract.from_mapping(intake)
    if certificate.get('certificate_hash')!=c.selection_certificate_hash: raise UpstreamError('selection certificate hash mismatch')
    if registry.get('registry_hash')!=c.selection_registry_hash: raise UpstreamError('selection registry hash mismatch')
    if exposure.get('ledger_hash')!=c.exposure_ledger_hash: raise UpstreamError('exposure ledger hash mismatch')
    if handoff.get('next_phase')!='SAED_V4_21' or not handoff.get('research_only'): raise UpstreamError('invalid V4-20 handoff')
    if any(bool(v) for v in handoff.get('authority',{}).values()): raise UpstreamError('upstream authority escalation')
    return {'phase':'SAED_V4_20','hash_verified':True,'immutable':True,'research_only':True,'intake_hash':content_hash(intake),'certificate_hash':c.selection_certificate_hash,'registry_hash':c.selection_registry_hash,'exposure_ledger_hash':c.exposure_ledger_hash}
