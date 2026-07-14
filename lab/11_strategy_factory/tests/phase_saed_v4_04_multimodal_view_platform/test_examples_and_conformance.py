import json
from pathlib import Path
from saed_v4_multimodal_views.conformance import run_vectors
ROOT=Path(__file__).resolve().parents[4]
def test_golden_examples_exist_and_hashes_present():
 p=json.loads((ROOT/'lab/11_strategy_factory/examples/saed_v4_04/golden_multimodal_view_package.json').read_text());assert len(p['views'])==10;assert len(p['package_hash'])==64
def test_conformance_vectors_all_pass():
 vectors=json.loads((ROOT/'lab/11_strategy_factory/test_vectors/saed_v4_04/SAED_V4_04_CONFORMANCE_VECTORS.json').read_text());r=run_vectors(vectors);assert len(r)>=10;assert all(x['passed'] for x in r),r
