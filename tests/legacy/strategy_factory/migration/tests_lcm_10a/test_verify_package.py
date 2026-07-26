from src.engine.tooling.strategy_factory.lcm.lcm_10a.verify import verify_package
from .conftest import ROOT
def test_full_package_verifies():
 r=verify_package(ROOT);assert r['passed'] and r['source_file_count']==7382 and r['setup_binding_count']==60
