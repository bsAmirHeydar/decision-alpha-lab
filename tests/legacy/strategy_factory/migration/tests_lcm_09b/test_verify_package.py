from src.engine.tooling.strategy_factory.lcm.lcm_09b.verify import verify_package
from .conftest import ROOT
def test_full_package_verifies():
 r=verify_package(ROOT);assert r["passed"] and r["package_count"]==60 and r["factory_registration_count"]==60
