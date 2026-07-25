from __future__ import annotations
from .canonical import content_hash
from .errors import BudgetError

class ResearchLedger:
    LIMITS = {
        'records': 'max_records',
        'conformal_fits': 'max_conformal_fits',
        'ood_fits': 'max_ood_fits',
        'selective_evaluations': 'max_selective_evaluations',
        'frontier_points': 'max_frontier_points',
        'bootstrap_draws': 'max_bootstrap_draws',
        'drift_windows': 'max_drift_windows',
        'failures': 'max_failures',
        'hidden_evaluation_queries': 'max_hidden_evaluation_queries',
        'protected_evidence_exposures': 'protected_evidence_exposure_limit',
        'runtime_compilations': 'runtime_compilation_limit',
        'order_submissions': 'order_submission_limit',
    }

    def __init__(self, contract):
        self.contract = contract
        self.counts = {key: 0 for key in self.LIMITS}
        self.events = []

    def consume(self, key, amount=1, detail=''):
        if key not in self.counts or int(amount) < 0:
            raise BudgetError('invalid budget counter')
        after = self.counts[key] + int(amount)
        limit = int(getattr(self.contract, self.LIMITS[key]))
        if after > limit:
            raise BudgetError(f'{key} budget exceeded')
        self.counts[key] = after
        self.events.append({'sequence': len(self.events) + 1, 'counter': key, 'delta': int(amount), 'after': after, 'limit': limit, 'detail': str(detail)})

    def snapshot(self):
        output = {
            'phase': 'SAED_V4_24',
            'counts': dict(self.counts),
            'limits': {key: int(getattr(self.contract, field)) for key, field in self.LIMITS.items()},
            'events': list(self.events),
            'complete': True,
        }
        output['ledger_hash'] = content_hash(output)
        return output
