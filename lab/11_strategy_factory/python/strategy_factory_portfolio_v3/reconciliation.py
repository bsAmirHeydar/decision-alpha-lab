from __future__ import annotations
from .errors import PortfolioError
def reconcile(plan,ledger,observed_reservations):
    expected={x.reservation_id:x.allocated_risk for x in plan.selected};observed=dict(observed_reservations)
    missing=tuple(sorted(set(expected)-set(observed)));extra=tuple(sorted(set(observed)-set(expected)));mismatch=tuple(sorted(k for k in set(expected)&set(observed) if abs(expected[k]-observed[k])>1e-9))
    return {'safe':not(missing or extra or mismatch),'missing':missing,'extra':extra,'mismatch':mismatch,'ledger_hash':ledger.ledger_hash}
def require_safe_reconciliation(report):
    if not report['safe']: raise PortfolioError('reservation_reconciliation_failed','reservation reconciliation failed',report)
    return True
