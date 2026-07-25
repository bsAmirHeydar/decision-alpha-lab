from helpers import solve
from saed_v4_action_lattice.graph import validate_dag,validate_atomic_edges
def test_dag_and_atomic_edges():
 l=solve()['action_lattice'];assert len(validate_dag(l['nodes'],l['edges']))==38;validate_atomic_edges(l['nodes'],l['edges'])
def test_mandatory_fallback_nodes():
 l=solve()['action_lattice'];classes=[n['action_class'] for n in l['nodes']];assert classes.count('skip')==1 and classes.count('abstain')==1
def test_edge_classes():
 l=solve()['action_lattice'];counts={k:sum(e['edge_kind']==k for e in l['edges']) for k in ('atomic_parameter_step','fallback_abstain','fallback_skip')};assert counts=={'atomic_parameter_step':84,'fallback_abstain':36,'fallback_skip':1}
def test_no_preference_semantics():
 l=solve()['action_lattice'];assert l['preference_semantics']=='none' and all(e['semantic_claim']=='adjacency_only_not_preference' for e in l['edges'])
