from tools.repository_paths import find_repository_root
import json
from pathlib import Path
ROOT=find_repository_root(__file__)
def test_all_schemas_are_closed_and_valid_json():
 files=sorted((ROOT/'schemas/legacy/strategy_factory/saed_v4_08').glob('*.schema.json'));assert len(files)>=27
 for p in files:
  x=json.loads(p.read_text());assert x.get('additionalProperties') is False;assert x['$schema'].endswith('2020-12/schema')
