from tools.strategy_factory.lcm.lcm_04.verify import verify_package
from tools.strategy_factory.lcm.lcm_04.event_ledger import verify
from tools.strategy_factory.lcm.lcm_04.io import read_json

def test_package_verifies(char_root): assert verify_package(char_root)['passed']
def test_event_chain(char_root): assert verify(read_json(char_root/'events/characterization_event_ledger.json'))
