from tools.strategy_factory.lcm.lcm_09b.static_validation import scan_module
from .conftest import REPO
def test_core_has_no_order_drawing_network_or_process_surface():
 r=scan_module(REPO/"tools/strategy_factory/lcm/lcm_09b");assert r["passed"],r["findings"]
