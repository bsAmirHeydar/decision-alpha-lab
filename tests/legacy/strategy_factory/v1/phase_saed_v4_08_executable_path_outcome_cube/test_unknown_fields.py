from tools.repository_paths import find_repository_root
import json
from pathlib import Path
ROOT=find_repository_root(__file__)
def test_negative_unknown_field_fixture_exists():
 x=json.loads((ROOT/'examples/legacy/strategy_factory/saed_v4_08/negative/unknown_field_context.json').read_text());assert 'unknown_field' in x
