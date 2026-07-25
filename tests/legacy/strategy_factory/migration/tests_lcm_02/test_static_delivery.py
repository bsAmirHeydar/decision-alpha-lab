from tools.strategy_factory.lcm.lcm_02.static_validation import validate
from tools.strategy_factory.lcm.lcm_02.delivery_validation import validate as delivery

def test_static(repo_root): assert validate(repo_root)['passed']
def test_delivery(repo_root): assert delivery(repo_root)['passed']
