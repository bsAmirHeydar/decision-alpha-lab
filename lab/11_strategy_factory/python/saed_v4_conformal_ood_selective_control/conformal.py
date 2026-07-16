from __future__ import annotations
from collections import defaultdict
from .canonical import content_hash, stable_id
from .errors import ConformalError
from .numerics import conformal_quantile, mean

def downside_residual(record):
    return max(0.0, float(record['predicted_value']) - float(record['realized_value']))

def fit(records, contract, ledger):
    calibration = [record for record in records if record['role'] == 'calibration']
    if len(calibration) < contract.minimum_group_size:
        raise ConformalError('insufficient calibration records')
    pooled_scores = [downside_residual(record) for record in calibration]
    grouped = defaultdict(list)
    for record in calibration:
        grouped[record['regime']].append(downside_residual(record))
    group_rows = []
    for regime in sorted(grouped):
        scores = grouped[regime]
        eligible = len(scores) >= contract.minimum_group_size
        group_rows.append({
            'regime': regime,
            'count': len(scores),
            'eligible': eligible,
            'scores': scores,
            'quantile': conformal_quantile(scores, contract.alpha) if eligible else None,
            'mean_score': mean(scores),
        })
    output = {
        'phase': 'SAED_V4_24',
        'alpha': contract.alpha,
        'coverage_level': 1.0 - contract.alpha,
        'score_type': contract.score_type,
        'pooled_count': len(pooled_scores),
        'pooled_scores': pooled_scores,
        'pooled_quantile': conformal_quantile(pooled_scores, contract.alpha),
        'groups': group_rows,
        'minimum_group_size': contract.minimum_group_size,
        'finite_sample_correction': True,
        'one_sided_lower': True,
        'pooled_fallback': True,
    }
    output['calibrator_id'] = stable_id('conformal_calibrator', output)
    output['calibrator_hash'] = content_hash(output)
    ledger.consume('conformal_fits', 1, 'one-sided split/Mondrian conformal fit')
    return output

def lower_bound(record, calibrator):
    group = next((row for row in calibrator['groups'] if row['regime'] == record['regime'] and row['eligible']), None)
    quantile = float(group['quantile']) if group is not None else float(calibrator['pooled_quantile'])
    source = 'mondrian' if group is not None else 'pooled_fallback'
    output = {
        'record_id': record['record_id'],
        'regime': record['regime'],
        'predicted_value': float(record['predicted_value']),
        'quantile': quantile,
        'value_lower_bound': float(record['predicted_value']) - quantile,
        'coverage_level': float(calibrator['coverage_level']),
        'quantile_source': source,
        'calibration_count': int(group['count']) if group is not None else int(calibrator['pooled_count']),
        'uses_outcome_at_decision': False,
    }
    output['bound_hash'] = content_hash(output)
    return output

def retrospective_coverage(records, calibrator):
    rows = []
    for record in records:
        bound = lower_bound(record, calibrator)
        covered = float(record['realized_value']) >= bound['value_lower_bound']
        rows.append({'record_id': record['record_id'], 'regime': record['regime'], 'value_lower_bound': bound['value_lower_bound'], 'realized_value': float(record['realized_value']), 'covered': covered})
    output = {
        'phase': 'SAED_V4_24',
        'rows': rows,
        'record_count': len(rows),
        'empirical_coverage': mean(1.0 if row['covered'] else 0.0 for row in rows),
        'target_coverage': float(calibrator['coverage_level']),
        'retrospective_only': True,
        'decision_authority': False,
    }
    output['coverage_hash'] = content_hash(output)
    return output
