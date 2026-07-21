from tools.strategy_factory.lcm.lcm_10b.static_validation import scan_module
from .conftest import MODULE
def test_python_module_has_no_network_process_or_broker_client_imports():assert scan_module(MODULE)["passed"]
