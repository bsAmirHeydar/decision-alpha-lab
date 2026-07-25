import json,pytest
from jsonschema import Draft202012Validator

def test_all_schema_pairs(root):
 m=json.loads((root/'releases/history/strategy_factory/artifacts/saed_v4_12/CONTRACT_VALIDATION_MAP.JSON').read_text())
 for p in m['pairs']:
  s=json.loads((root/p['schema']).read_text());d=json.loads((root/p['document']).read_text());Draft202012Validator.check_schema(s);Draft202012Validator(s).validate(d)
def test_unknown_field_rejected(root):
 m=json.loads((root/'releases/history/strategy_factory/artifacts/saed_v4_12/CONTRACT_VALIDATION_MAP.JSON').read_text());p=m['pairs'][0];s=json.loads((root/p['schema']).read_text());d=json.loads((root/p['document']).read_text());d['unknown_field']=1
 with pytest.raises(Exception):Draft202012Validator(s).validate(d)
