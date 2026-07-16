from __future__ import annotations
from collections import Counter, defaultdict
from datetime import datetime
import math
from .canonical import content_hash
from .contracts import ACTIONS, ROLES, REQUIRED_RECORD_FIELDS
from .errors import DatasetError

def parse_time(value):
    return datetime.fromisoformat(str(value).replace('Z', '+00:00'))

def validate(records, contract, ledger):
    if not isinstance(records, list) or len(records) < contract.minimum_records:
        raise DatasetError('insufficient records')
    seen = set()
    clusters = set()
    regimes = Counter()
    roles = Counter()
    cluster_roles = defaultdict(set)
    previous_decision = None
    for record in records:
        if set(record) != REQUIRED_RECORD_FIELDS:
            raise DatasetError('record fields mismatch')
        if record['record_id'] in seen:
            raise DatasetError('duplicate record id')
        seen.add(record['record_id'])
        clusters.add(record['cluster_id'])
        regimes[record['regime']] += 1
        roles[record['role']] += 1
        cluster_roles[record['cluster_id']].add(record['role'])
        if record['role'] not in ROLES or record['candidate_action'] not in ACTIONS:
            raise DatasetError('unknown role or action')
        if set(record['features']) != set(contract.feature_names):
            raise DatasetError('feature registry mismatch')
        if any(not math.isfinite(float(value)) for value in record['features'].values()):
            raise DatasetError('non-finite feature')
        if 'skip' not in record['allowed_actions'] or not set(record['allowed_actions']) <= ACTIONS or record['candidate_action'] not in record['allowed_actions']:
            raise DatasetError('invalid action mask')
        decision_time = parse_time(record['decision_time'])
        feature_known_at = parse_time(record['feature_known_at'])
        outcome_observed_at = parse_time(record['outcome_observed_at'])
        if previous_decision is not None and decision_time <= previous_decision:
            raise DatasetError('decision time order violation')
        previous_decision = decision_time
        if feature_known_at > decision_time or outcome_observed_at <= decision_time:
            raise DatasetError('known-time boundary violation')
        if record['future_suffix_accessed'] or record['protected_evidence_accessed']:
            raise DatasetError('evidence firewall violation')
        if not 0 < float(record['behavior_probability']) <= 1 or not 0 <= float(record['candidate_probability']) <= 1 or not 0 <= float(record['support_score']) <= 1:
            raise DatasetError('probability or support domain violation')
    if len(clusters) < contract.minimum_clusters or min(regimes.values()) < contract.minimum_records_per_regime:
        raise DatasetError('cluster or regime support below contract')
    if any(len(value) != 1 for value in cluster_roles.values()):
        raise DatasetError('cluster role leakage')
    ledger.consume('records', len(records), 'validated calibration research records')
    output = {
        'phase': 'SAED_V4_24',
        'record_count': len(records),
        'cluster_count': len(clusters),
        'role_counts': [{'role': key, 'count': roles[key]} for key in sorted(roles)],
        'regime_counts': [{'regime': key, 'count': regimes[key]} for key in sorted(regimes)],
        'feature_names': list(contract.feature_names),
        'strict_decision_time_order': True,
        'feature_known_by_decision': True,
        'outcome_after_decision': True,
        'future_suffix_access_count': 0,
        'protected_evidence_access_count': 0,
        'cluster_role_separation': True,
        'dataset_hash': content_hash(records),
    }
    output['summary_hash'] = content_hash(output)
    return output

def by_role(records):
    return {role: [record for record in records if record['role'] == role] for role in sorted(ROLES)}
