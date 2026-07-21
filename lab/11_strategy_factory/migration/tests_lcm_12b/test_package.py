from tools.strategy_factory.lcm.lcm_12b.verify import verify_package
def test_package_verifies(reconciliation_root):
    assert verify_package(reconciliation_root)==[]
