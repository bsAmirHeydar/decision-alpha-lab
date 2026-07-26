import json
from jsonschema import Draft202012Validator
from src.engine.tooling.strategy_factory.acl_os.acl_12.static_validation import validate_registry
from src.engine.tooling.strategy_factory.acl_os.acl_12.delivery_validation import validate_delivery
def test_registry_valid(ROOT): assert validate_registry(ROOT)['passed']
def test_delivery_valid(ROOT): assert validate_delivery(ROOT)['passed']
def test_all_schemas_valid(ROOT):
    for p in (ROOT/'registry/history/acl/acl_12/schemas/v1').glob('*.json'): Draft202012Validator.check_schema(json.loads(p.read_text()))
def test_policies_closed(ROOT):
    for p in (ROOT/'registry/history/acl/acl_12/policies/v1').glob('*.json'): assert json.loads(p.read_text())['closed'] is True
