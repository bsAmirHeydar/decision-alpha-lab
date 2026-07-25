from tools.strategy_factory.lcm.lcm_15a.verify import verify_package
def test_manifest(repo_root,proof_root):
 r=verify_package(repo_root,proof_root);assert r.candidate_count==2168 and r.blocked_deletion_count==2168
