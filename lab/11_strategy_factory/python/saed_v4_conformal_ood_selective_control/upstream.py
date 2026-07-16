from __future__ import annotations
from .canonical import content_hash
from .errors import UpstreamError

ALLOWED_NEXT_WORK = {
    'conformal_value_bounds', 'support_aware_ood_detection', 'selective_action_control',
    'abstention_calibration', 'coverage_risk_tradeoff'
}

def verify(contract, documents):
    if set(documents) != {'handoff', 'certificate'}:
        raise UpstreamError('upstream document set mismatch')
    handoff = documents['handoff']
    certificate = documents['certificate']
    if handoff.get('phase') != 'SAED_V4_23' or handoff.get('next_phase') != 'SAED_V4_24':
        raise UpstreamError('wrong phase lineage')
    if handoff.get('handoff_hash') != contract.handoff_hash or certificate.get('certificate_hash') != contract.certificate_hash:
        raise UpstreamError('upstream hash mismatch')
    if handoff.get('research_policy_id') != contract.research_policy_id:
        raise UpstreamError('research policy identity mismatch')
    if not handoff.get('research_only') or any(handoff.get('authority', {}).values()):
        raise UpstreamError('upstream authority leakage')
    if set(handoff.get('allowed_next_work', [])) != ALLOWED_NEXT_WORK:
        raise UpstreamError('handoff scope mismatch')
    output = {
        'phase': 'SAED_V4_24',
        'upstream_phase': 'SAED_V4_23',
        'handoff_hash': contract.handoff_hash,
        'certificate_hash': contract.certificate_hash,
        'research_policy_id': contract.research_policy_id,
        'scope_verified': True,
        'authority_verified_zero': True,
        'immutable': True,
    }
    output['receipt_hash'] = content_hash(output)
    return output
