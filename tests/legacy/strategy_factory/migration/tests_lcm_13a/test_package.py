def test_package_verifier_passes(dual_root):
    from src.engine.tooling.strategy_factory.lcm.lcm_13a.verify import verify_package
    assert verify_package(dual_root) == []
