from tools.strategy_factory.lcm.lcm_10a.static_validation import scan_module
from .conftest import REPO
def test_inventory_tooling_imports_no_broker_network_or_process_runtime():assert scan_module(REPO/'tools/strategy_factory/lcm/lcm_10a')['passed']
