from src.engine.tooling.strategy_factory.lcm.lcm_10b.verify import verify_package
from .conftest import ROOT
def test_full_package_verifies():assert verify_package(ROOT)["passed"]
