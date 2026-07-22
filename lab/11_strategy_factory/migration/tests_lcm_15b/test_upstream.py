from tools.strategy_factory.lcm.lcm_15b.upstream import verify_upstream
def test_upstream(repo_root):assert verify_upstream(repo_root)["handoff_digest"].endswith("4018bd")
