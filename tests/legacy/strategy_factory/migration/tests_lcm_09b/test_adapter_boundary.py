import pytest
from src.engine.tooling.strategy_factory.lcm.lcm_09b.adapters import LegacyDecisionAdapter
from src.engine.tooling.strategy_factory.lcm.lcm_09b.errors import ContractError
from .conftest import j
def test_blocked_adapter_cannot_execute_or_normalize():
 reg=j("adapters/setup_adapter_registry.json")["adapters"][0];assert reg["executes_legacy_source"] is False
 with pytest.raises(ContractError):LegacyDecisionAdapter().normalize(reg,{})
