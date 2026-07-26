from src.engine.tooling.strategy_factory.lcm.lcm_12b.static_validation import static_validate
def test_no_runtime_or_order_authority(repo_root):
    assert static_validate(repo_root/"src/engine/tooling/strategy_factory/lcm/lcm_12b")==[]
