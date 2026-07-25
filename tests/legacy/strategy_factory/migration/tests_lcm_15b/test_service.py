from tools.strategy_factory.lcm.lcm_15b.service import LCM15BRootReleaseReorganizationService
def test_service(repo_root,package_root):assert LCM15BRootReleaseReorganizationService(repo_root).verify(package_root).validation_status=="PASS"
