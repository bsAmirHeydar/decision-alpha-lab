from __future__ import annotations
from .canonical import content_hash, stable_id

def calibrate(frontier, contract):
    feasible = [row for row in frontier['rows'] if row['coverage'] >= contract.minimum_coverage and row['monotone_risk_upper'] <= contract.target_risk_upper]
    if feasible:
        chosen = sorted(feasible, key=lambda row: (-row['coverage'], -row['threshold'], row['monotone_risk_upper']))[0]
        full_fallback = False
    else:
        chosen = {'threshold': 1.0, 'coverage': 0.0, 'selective_risk': 0.0, 'monotone_risk_upper': 0.0, 'accepted_count': 0}
        full_fallback = True
    output = {
        'phase': 'SAED_V4_24',
        'target_risk_upper': contract.target_risk_upper,
        'minimum_coverage': contract.minimum_coverage,
        'chosen_threshold': float(chosen['threshold']),
        'calibrated_coverage': float(chosen['coverage']),
        'calibrated_risk': float(chosen['selective_risk']),
        'calibrated_risk_upper': float(chosen['monotone_risk_upper']),
        'accepted_count': int(chosen['accepted_count']),
        'safe_action': contract.safe_action,
        'full_safe_fallback': full_fallback,
        'objective': contract.objective,
        'tie_break': contract.tie_break,
        'research_only': True,
    }
    output['policy_id'] = stable_id('abstention_policy', output)
    output['policy_hash'] = content_hash(output)
    return output
