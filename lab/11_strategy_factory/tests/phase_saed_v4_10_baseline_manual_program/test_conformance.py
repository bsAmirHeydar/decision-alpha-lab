from saed_v4_baseline_manual.conformance import run_vectors

def test_conformance_vectors_pass(load,upstream):
 v,_,l,_=upstream;x=run_vectors(load('lab/11_strategy_factory/examples/saed_v4_10/conformance_vectors.json'),v,l);assert x['passed'];assert x['vector_count']==4
