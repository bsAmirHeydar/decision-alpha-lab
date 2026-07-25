from tools.strategy_factory.lcm.lcm_12a.verify import verify_package
def test_package_verification(mapping_root):
    assert verify_package(mapping_root)==[]
