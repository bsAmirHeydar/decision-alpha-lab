import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
def test_negative_unknown_field_fixture_exists():
 x=json.loads((ROOT/'lab/11_strategy_factory/examples/saed_v4_08/negative/unknown_field_context.json').read_text());assert 'unknown_field' in x
