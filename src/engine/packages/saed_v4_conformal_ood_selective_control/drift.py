from __future__ import annotations
from .canonical import content_hash
from .numerics import mean, psi

def assess(detector, drift_evaluations, contract, ledger):
    if len(drift_evaluations) < contract.minimum_window_records:
        output = {
            'phase': 'SAED_V4_24', 'window_count': len(drift_evaluations), 'status': 'insufficient_window',
            'breach': True, 'ood_rate': 1.0, 'population_stability_index': 1e6, 'mean_score_ratio': 1e6,
            'reasons': ['minimum_window_not_met'], 'action': 'research_abstention_only', 'runtime_mutation': False,
        }
        output['report_hash'] = content_hash(output)
        return output
    scores = [evaluation['ood_score'] for evaluation in drift_evaluations]
    reference = detector['calibration_scores']
    ood_rate = mean(1.0 if evaluation['is_ood'] else 0.0 for evaluation in drift_evaluations)
    population_shift = psi(reference, scores)
    mean_ratio = mean(scores) / max(mean(reference), 1e-9)
    reasons = []
    if ood_rate > contract.maximum_ood_rate:
        reasons.append('ood_rate_breach')
    if population_shift > contract.maximum_psi:
        reasons.append('psi_breach')
    if mean_ratio > contract.maximum_mean_score_ratio:
        reasons.append('mean_score_ratio_breach')
    output = {
        'phase': 'SAED_V4_24',
        'window_count': len(drift_evaluations),
        'status': 'breach' if reasons else 'stable',
        'breach': bool(reasons),
        'ood_rate': ood_rate,
        'population_stability_index': population_shift,
        'mean_score_ratio': mean_ratio,
        'reasons': reasons if reasons else ['within_contract'],
        'action': contract.action_on_breach if reasons else 'none',
        'runtime_mutation': False,
    }
    output['report_hash'] = content_hash(output)
    ledger.consume('drift_windows', 1, 'OOD drift assessment')
    return output
