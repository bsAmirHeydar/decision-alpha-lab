from dataclasses import replace
import pytest

from strategy_factory_operations_v3.enums import DeploymentStage
from strategy_factory_operations_v3.errors import OperationsError
from strategy_factory_operations_v3.golden import NOW, policy, target
from strategy_factory_operations_v3.lease import issue_runtime_lease, revoke_runtime_lease


def issue(plan, **kw):
    args = dict(lease_id="lease", issued_by="issuer", approved_by="approver", issued_at_ms=NOW, expires_at_ms=NOW+1000, max_risk_units=0.2)
    args.update(kw)
    return issue_runtime_lease(plan, target(), policy(), **args)


def test_issue_live_lease(live_plan):
    lease = issue(live_plan)
    assert lease.stage is DeploymentStage.MICRO_LIVE and lease.max_risk_units == 0.2


def test_lease_target_mismatch(live_plan):
    with pytest.raises(OperationsError, match="target_mismatch"):
        issue_runtime_lease(live_plan, replace(target(), allowed_symbols=("USDJPY",)), policy(), "l", "i", "a", NOW, NOW+1, .1)


def test_lease_outside_plan_start(live_plan):
    with pytest.raises(OperationsError, match="lease_window"): issue(live_plan, issued_at_ms=live_plan.starts_at_ms-1)


def test_lease_outside_plan_expiry(live_plan):
    with pytest.raises(OperationsError, match="lease_window"): issue(live_plan, expires_at_ms=live_plan.expires_at_ms+1)


def test_lease_duration_limit(live_plan):
    extended = replace(live_plan, expires_at_ms=NOW+policy().max_lease_minutes*60_000+1000)
    with pytest.raises(OperationsError, match="lease_duration"): issue(extended, expires_at_ms=NOW+policy().max_lease_minutes*60_000+1)


def test_lease_sod(live_plan):
    with pytest.raises(OperationsError, match="lease_sod"): issue(live_plan, issued_by="same", approved_by="same")


@pytest.mark.parametrize("risk", [-1, .251, 100])
def test_lease_risk_is_bounded(live_plan, risk):
    with pytest.raises(OperationsError, match="lease_risk"): issue(live_plan, max_risk_units=risk)


def test_revoke_lease(live_lease):
    revoked = revoke_runtime_lease(live_lease, NOW, "manual kill")
    assert revoked.revoked_at_ms == NOW and not revoked.active_at(NOW)


def test_revoke_requires_reason(live_lease):
    with pytest.raises(OperationsError, match="revocation_reason"): revoke_runtime_lease(live_lease, NOW, "")


def test_revoke_time_bounded(live_lease):
    with pytest.raises(OperationsError, match="revocation_time"): revoke_runtime_lease(live_lease, live_lease.expires_at_ms+1, "late")
