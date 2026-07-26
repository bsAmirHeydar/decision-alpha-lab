import pytest
from src.engine.tooling.strategy_factory.lcm.lcm_10b.guards import CapabilityGuard
from src.engine.tooling.strategy_factory.lcm.lcm_10b.errors import CapabilityDeniedError
from .conftest import j
def test_guard_denies_broker_mutation():
 g=CapabilityGuard(j("guards/capability_guard_policy.json"));assert not g.decide("SUBMIT_ORDER","DRY_RUN").allowed
 with pytest.raises(CapabilityDeniedError):g.require("SUBMIT_ORDER","LIVE")
