from src.engine.tooling.strategy_factory.lcm.lcm_15c.upstream import verify_upstream
def test_upstream(repo_root):assert verify_upstream(repo_root)['handoff_digest'].endswith('6df26f')
