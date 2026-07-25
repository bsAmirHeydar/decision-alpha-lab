from tools.strategy_factory.lcm.lcm_04.static_validation import validate as static
from tools.strategy_factory.lcm.lcm_04.schema_validation import validate as schemas

def test_static(repo_root): assert static(repo_root)['passed']
def test_schemas(repo_root): assert schemas(repo_root)['passed']
