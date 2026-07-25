from tools.repository_paths import find_repository_root
import json
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=find_repository_root(__file__);SC=ROOT/'schemas/legacy/strategy_factory/saed_v4_04'
def test_all_schemas_parse_and_are_closed():
 files=list(SC.glob('*.schema.json'));assert len(files)>=35
 for p in files:
  d=json.loads(p.read_text());Draft202012Validator.check_schema(d);assert d.get('additionalProperties') is False
def test_schema_catalog_count_matches():
 c=json.loads((ROOT/'releases/history/strategy_factory/artifacts/saed_v4_04/SCHEMA_CATALOG.json').read_text());assert c['schema_count']==len(list(SC.glob('*.schema.json')))
