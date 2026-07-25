from tools.strategy_factory.lcm.lcm_15b.verify import verify_package
def test_manifest(repo_root,package_root):assert verify_package(repo_root,package_root).documentation_relocation_count==934
