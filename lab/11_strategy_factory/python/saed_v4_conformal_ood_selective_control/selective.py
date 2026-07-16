from __future__ import annotations
from .canonical import content_hash

def decide(record, conformal_bound, ood_evaluation, contract, ledger):
    reasons = []
    if record['candidate_action'] not in record['allowed_actions']:
        reasons.append('action_mask_failed')
    if conformal_bound['value_lower_bound'] < contract.minimum_value_lower_bound:
        reasons.append('value_lower_bound_failed')
    if ood_evaluation['is_ood'] or ood_evaluation['ood_pvalue'] < contract.minimum_ood_pvalue:
        reasons.append('ood_gate_failed')
    if float(record['support_score']) < contract.minimum_support_score:
        reasons.append('support_gate_failed')
    if float(ood_evaluation['missingness']) > contract.maximum_missingness:
        reasons.append('missingness_gate_failed')
    if record['candidate_action'] == contract.safe_action:
        reasons.append('candidate_is_safe_action')
    accepted = not reasons
    selected_action = record['candidate_action'] if accepted else contract.safe_action
    value_margin = max(0.0, conformal_bound['value_lower_bound'] - contract.minimum_value_lower_bound)
    confidence_score = min(value_margin, float(ood_evaluation['ood_pvalue']), float(record['support_score']))
    output = {
        'record_id': record['record_id'],
        'candidate_action': record['candidate_action'],
        'selected_action': selected_action,
        'accepted': accepted,
        'abstained': not accepted,
        'reason_codes': ['accepted_all_gates'] if accepted else reasons,
        'value_lower_bound': float(conformal_bound['value_lower_bound']),
        'coverage_level': float(conformal_bound['coverage_level']),
        'ood_pvalue': float(ood_evaluation['ood_pvalue']),
        'support_score': float(record['support_score']),
        'confidence_score': confidence_score,
        'safe_action': contract.safe_action,
        'uses_realized_outcome': False,
        'promotion_eligible': False,
        'runtime_executable': False,
    }
    output['decision_hash'] = content_hash(output)
    ledger.consume('selective_evaluations', 1, 'selective research decision')
    return output
