from helpers import load
from saed_v4_outcome_cube.conformance import run_vectors
def test_conformance_vectors_pass():
 r=run_vectors(load('tests/fixtures/legacy/strategy_factory/saed_v4_08/SAED_V4_08_CONFORMANCE_VECTORS.json'));assert r['all_passed'];assert r['vector_count']>=4
