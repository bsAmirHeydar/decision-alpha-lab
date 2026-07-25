from tools.strategy_factory.acl_os.acl_04.lcm10b_reference import load_lcm10b_reference
from .conftest import ROOT
def test_acl04_bridge_is_read_only():
 b=load_lcm10b_reference(ROOT);one=next(iter(b.by_setup));r=b.resolve(one);assert r["execution_authorized"] is False
