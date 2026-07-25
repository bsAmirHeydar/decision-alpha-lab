from saed_v4_sequence_state_space.conformance import run_vectors

def test_conformance(load):
 v=load('examples/legacy/strategy_factory/saed_v4_12/conformance_vectors.json');r=run_vectors(v);assert r['passed'] and r['vector_count']==6
