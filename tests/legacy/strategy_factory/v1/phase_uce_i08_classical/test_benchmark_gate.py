from strategy_factory_classical_v3 import *
def test_conformance_report_passes():
 o=run_conformance();assert o['passed'],o
def test_gate_blocks_missing_tree():
 r=BenchmarkReport('r','p',(),(AlgorithmFamily.BASELINE,AlgorithmFamily.LINEAR,AlgorithmFamily.TREE),(AlgorithmFamily.TREE,),True,True,False,'h');g=ClassicalGateEvaluator.evaluate('c',r);assert g.state is ComparisonGateState.BLOCK;assert 'missing_required_classical_family' in g.blockers
def test_high_capacity_requires_classical_comparison():
 r=BenchmarkReport('r','p',(),(AlgorithmFamily.BASELINE,AlgorithmFamily.LINEAR,AlgorithmFamily.TREE),(AlgorithmFamily.LINEAR,),True,True,False,'h');assert ClassicalGateEvaluator.evaluate('c',r).state.value=='block'
