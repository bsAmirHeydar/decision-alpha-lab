from __future__ import annotations
from .canonical import content_hash, stable_id
from .errors import OODError
from .numerics import empirical_upper_pvalue, mad, median, quantile, robust_z

def euclidean(left, right, feature_names):
    return sum((float(left[name]) - float(right[name])) ** 2 for name in feature_names) ** 0.5

def _raw_score(record, feature_statistics, reference_records, contract):
    robust_component = max(robust_z(record['features'][row['feature']], row['center'], row['mad'], contract.robust_scale_floor) for row in feature_statistics)
    nearest_component = min((euclidean(record['features'], reference['features'], contract.feature_names) for reference in reference_records if reference['record_id'] != record['record_id']), default=0.0)
    support_component = 1.0 - float(record['support_score'])
    total = robust_component + contract.nearest_neighbor_weight * nearest_component + contract.support_deficit_weight * support_component
    return total, {'robust_mad': robust_component, 'nearest_neighbor': nearest_component, 'support_deficit': support_component}

def fit(records, contract, ledger):
    calibration = [record for record in records if record['role'] == 'calibration']
    if not calibration:
        raise OODError('empty OOD calibration set')
    feature_statistics = []
    for name in contract.feature_names:
        values = [record['features'][name] for record in calibration]
        center = median(values)
        feature_statistics.append({'feature': name, 'center': center, 'mad': max(mad(values, center), contract.robust_scale_floor)})
    calibration_scores = [_raw_score(record, feature_statistics, calibration, contract)[0] for record in calibration]
    output = {
        'phase': 'SAED_V4_24',
        'alpha': contract.alpha,
        'feature_names': list(contract.feature_names),
        'methods': list(contract.methods),
        'feature_statistics': feature_statistics,
        'calibration_scores': calibration_scores,
        'calibration_count': len(calibration),
        'score_threshold': quantile(calibration_scores, 1.0 - contract.alpha),
        'minimum_pvalue': contract.minimum_pvalue,
        'maximum_feature_missingness': contract.maximum_feature_missingness,
        'fail_closed': True,
    }
    output['detector_id'] = stable_id('ood_detector', output)
    output['detector_hash'] = content_hash(output)
    ledger.consume('ood_fits', 1, 'robust support-aware OOD fit')
    return output

def evaluate(record, detector, contract, calibration_records):
    missing = [name for name in contract.feature_names if name not in record['features']]
    missingness = len(missing) / len(contract.feature_names)
    if missingness > contract.maximum_feature_missingness:
        return {
            'record_id': record['record_id'], 'ood_score': 1e300, 'ood_pvalue': 0.0, 'is_ood': True,
            'missingness': missingness, 'reason': 'missingness_gate',
            'score_components': {'robust_mad': None, 'nearest_neighbor': None, 'support_deficit': None},
            'uses_outcome_at_decision': False,
            'evaluation_hash': content_hash({'record_id': record['record_id'], 'reason': 'missingness_gate'}),
        }
    total, components = _raw_score(record, detector['feature_statistics'], calibration_records, contract)
    pvalue = empirical_upper_pvalue(detector['calibration_scores'], total)
    is_ood = pvalue < contract.minimum_pvalue or total > detector['score_threshold']
    output = {
        'record_id': record['record_id'],
        'ood_score': total,
        'ood_pvalue': pvalue,
        'is_ood': is_ood,
        'missingness': missingness,
        'reason': 'ood_gate' if is_ood else 'in_distribution',
        'score_components': components,
        'uses_outcome_at_decision': False,
    }
    output['evaluation_hash'] = content_hash(output)
    return output
