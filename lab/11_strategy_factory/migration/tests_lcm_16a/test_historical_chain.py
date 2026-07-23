from tools.strategy_factory.lcm.lcm_15a.constants import PACKAGE_RELATIVE as PACKAGE_15A
from tools.strategy_factory.lcm.lcm_15a.verify import verify_package as verify_15a
from tools.strategy_factory.lcm.lcm_15b.constants import PACKAGE_RELATIVE as PACKAGE_15B
from tools.strategy_factory.lcm.lcm_15b.verify import verify_package as verify_15b
from tools.strategy_factory.lcm.lcm_15c.constants import PACKAGE_RELATIVE as PACKAGE_15C
from tools.strategy_factory.lcm.lcm_15c.verify import verify_package as verify_15c


def test_historical_lcm15_verifiers_accept_only_verified_amendment(root):
    a = verify_15a(root, root / PACKAGE_15A)
    b = verify_15b(root, root / PACKAGE_15B)
    c = verify_15c(root, root / PACKAGE_15C)
    assert a.validation_status == b.validation_status == c.validation_status == "PASS"
