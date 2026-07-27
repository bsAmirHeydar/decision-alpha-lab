from .conftest import load
from .helpers import inputs
from saed_v4_execution_twin.conformance import run_vectors

def test_reference_vectors_pass():
    cube,handoff,m=inputs();vectors=load('tests/fixtures/legacy/strategy_factory/saed_v4_09/SAED_V4_09_CONFORMANCE_VECTORS.json');result=run_vectors(vectors,cube,handoff,m);assert result['passed']
