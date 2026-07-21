from __future__ import annotations
from tools.strategy_factory.lcm.lcm_13b.verify import verify_package

def test_package_verifies(cutover_root):
    assert verify_package(cutover_root) == []
