import json
from pathlib import Path
import pytest
from jsonschema import Draft202012Validator

def test_all_schemas_are_closed(root):
    paths=list((root/'schemas/legacy/strategy_factory/saed_v4_03').glob('*.schema.json'));assert len(paths)>=30
    for p in paths:
        s=json.loads(p.read_text());Draft202012Validator.check_schema(s);assert s.get('additionalProperties') is False

def test_unknown_field_rejected(root):
    s=json.loads((root/'schemas/legacy/strategy_factory/saed_v4_03/event_source_descriptor.schema.json').read_text());d={'source_id':'x','source_version':'1','clock_domain':'canonical_utc','source_hash':'a'*64,'trusted':True,'timezone':'UTC','metadata':{},'unknown':1};assert list(Draft202012Validator(s).iter_errors(d))
