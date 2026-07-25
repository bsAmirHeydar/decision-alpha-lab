import pytest

from strategy_factory_operations_v3.golden import NOW, envelope, policy, release, target
from strategy_factory_operations_v3.health import evaluate_health
from strategy_factory_operations_v3.lease import issue_runtime_lease
from strategy_factory_operations_v3.release_binding import compile_deployment_plan
from strategy_factory_operations_v3.enums import DeploymentStage


@pytest.fixture
def live_plan():
    return compile_deployment_plan(
        release(), target(), envelope(), policy(), DeploymentStage.MICRO_LIVE, 0.25,
        "operator-a", "approver-b", NOW - 1000, NOW - 500, NOW + 1_000_000,
    )


@pytest.fixture
def live_lease(live_plan):
    return issue_runtime_lease(
        live_plan, target(), policy(), "lease-1", "issuer-a", "approver-b",
        NOW - 100, NOW + 100_000, 0.25,
    )
