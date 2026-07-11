import json
from strategy_factory_contracts.codec import canonical_json
from strategy_factory_contracts import SchemaIdentity

def test_canonical_json_is_deterministic():
    a=canonical_json({"z":1,"a":2})
    b=canonical_json({"a":2,"z":1})
    assert a==b=='{"a":2,"z":1}'

def test_schema_serializes():
    payload=json.loads(canonical_json(SchemaIdentity("alpha_lab.strategy_factory","x",1,0,0)))
    assert payload["namespace"]=="alpha_lab.strategy_factory"
