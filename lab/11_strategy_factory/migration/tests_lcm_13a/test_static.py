def test_static_validation_passes():
    from pathlib import Path
    from tools.strategy_factory.lcm.lcm_13a.static_validation import static_validate
    assert static_validate(Path("tools/strategy_factory/lcm/lcm_13a")) == []
