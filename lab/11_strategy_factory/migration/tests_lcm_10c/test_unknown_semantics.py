import json
from conftest import CLOSURE
def test_unknowns_not_erased():
 r=json.loads((CLOSURE/'closure/residual_unknown_registry.json').read_text());dims={x['dimension'] for x in r['unknowns']};assert 'BROKER_RUNTIME_CONSTRAINTS' in dims;assert 'HUMAN_OWNER_APPROVAL' in dims
