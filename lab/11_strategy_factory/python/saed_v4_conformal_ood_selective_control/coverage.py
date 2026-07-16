from __future__ import annotations
from .canonical import content_hash
from .numerics import cluster_bootstrap_binary, mean, trapz

def build(decisions, selection_records, contract, ledger):
    record_map = {record['record_id']: record for record in selection_records}
    rows = []
    for index, threshold in enumerate(contract.threshold_grid):
        accepted = [decision for decision in decisions if decision['accepted'] and decision['confidence_score'] >= threshold]
        accepted_ids = [decision['record_id'] for decision in accepted]
        accepted_records = [record_map[record_id] for record_id in accepted_ids]
        coverage = len(accepted) / len(decisions) if decisions else 0.0
        risk = mean(1.0 if record['realized_value'] < 0 else 0.0 for record in accepted_records) if accepted_records else 0.0
        interval = cluster_bootstrap_binary(selection_records, accepted_ids, seed=424 + index * 17, draws=contract.bootstrap_draws, alpha=1.0 - contract.confidence_level)
        rows.append({
            'threshold': float(threshold),
            'accepted_count': len(accepted),
            'coverage': coverage,
            'selective_risk': risk,
            'selective_risk_lower': interval['lower'],
            'selective_risk_upper': interval['upper'],
            'bootstrap_draws': interval['draws'],
            'coverage_gate_passed': coverage >= contract.minimum_coverage,
            'risk_upper_gate_passed': interval['upper'] <= contract.maximum_selective_risk_upper,
        })
        ledger.consume('frontier_points', 1, 'coverage-risk threshold')
        ledger.consume('bootstrap_draws', contract.bootstrap_draws, 'cluster bootstrap')
    # Conservative monotone upper envelope: looser coverage cannot receive a lower certified risk than any stricter threshold.
    running_upper = 0.0
    for row in reversed(rows):
        running_upper = max(running_upper, row['selective_risk_upper'])
        row['monotone_risk_upper'] = running_upper
    points = [(row['coverage'], row['monotone_risk_upper']) for row in rows]
    baseline_risk = mean(1.0 if record['realized_value'] < 0 else 0.0 for record in selection_records)
    output = {
        'phase': 'SAED_V4_24',
        'risk_definition': contract.risk_definition,
        'rows': rows,
        'aurc_upper': trapz(points),
        'baseline_risk': baseline_risk,
        'minimum_coverage': contract.minimum_coverage,
        'maximum_selective_risk_upper': contract.maximum_selective_risk_upper,
        'monotone_envelope_applied': True,
        'cluster_bootstrap_applied': True,
        'retrospective_selection_validation_only': True,
    }
    output['frontier_hash'] = content_hash(output)
    return output
