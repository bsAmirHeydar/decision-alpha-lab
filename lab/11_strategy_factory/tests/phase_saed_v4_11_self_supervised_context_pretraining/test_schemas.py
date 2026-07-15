import json
from jsonschema import Draft202012Validator

def test_all_schemas_well_formed(root,load):
 c=load('lab/11_strategy_factory/artifacts/saed_v4_11/SCHEMA_CATALOG.json');assert c['schema_count']>=30
 for x in c['schemas']:Draft202012Validator.check_schema(load(x['path']))
def test_all_object_schemas_closed(load):
 c=load('lab/11_strategy_factory/artifacts/saed_v4_11/SCHEMA_CATALOG.json')
 for x in c['schemas']:
  s=load(x['path'])
  if s.get('type')=='object':assert s.get('additionalProperties') is False
def test_checkpoint_validates(load):
 s=load('lab/11_strategy_factory/schemas/saed_v4_11/encoder_checkpoint.schema.json');Draft202012Validator(s).validate(load('lab/11_strategy_factory/artifacts/saed_v4_11/GOLDEN_ENCODER_CHECKPOINT.JSON'))
def test_handoff_validates(load):
 s=load('lab/11_strategy_factory/schemas/saed_v4_11/handoff_v4_12.schema.json');Draft202012Validator(s).validate(load('lab/11_strategy_factory/artifacts/saed_v4_11/V4_11_TO_V4_12_HANDOFF.JSON'))
def test_records_validate(load):
 s=load('lab/11_strategy_factory/schemas/saed_v4_11/corpus_records.schema.json');Draft202012Validator(s).validate(load('lab/11_strategy_factory/examples/saed_v4_11/reference_corpus_records.json'))
