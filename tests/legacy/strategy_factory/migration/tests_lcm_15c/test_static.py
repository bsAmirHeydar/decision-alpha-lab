from tools.strategy_factory.lcm.lcm_15c.static_validation import static_validate
def test_static(repo_root):assert static_validate(repo_root/'src/engine/tooling/strategy_factory/lcm/lcm_15c')>=10
