from tools.strategy_factory.lcm.lcm_15a.upstream import verify_upstream
def test_upstream(repo_root): assert verify_upstream(repo_root)["handoff_digest"].endswith("ab02cb8")
