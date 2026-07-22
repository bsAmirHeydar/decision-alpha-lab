from tools.strategy_factory.lcm.lcm_15a.static_validation import static_validate
def test_static(repo_root): assert static_validate(repo_root/"tools/strategy_factory/lcm/lcm_15a")>=10
