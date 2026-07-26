from src.engine.tooling.strategy_factory.lcm.lcm_15c.service import LCM15CControlledDeletionClosureService
def test_service(repo_root,package_root):r=LCM15CControlledDeletionClosureService(repo_root).verify(package_root);assert r.deleted_path_count==0 and r.blocked_path_count==2168
