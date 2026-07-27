from saed_v4_baseline_manual.compiler import compile_program
from saed_v4_baseline_manual.interpreter import evaluate_program
from .helpers import program

def test_manual_projection_is_replayable(load,upstream):
 v,_,l,_=upstream;c=compile_program(program(load),v,l);a=evaluate_program(c,v);b=evaluate_program(c,v);assert a==b;assert a['matched_rule_id']=='manual_context_valid';assert a['projected_node_id']=='actionnode_120319e7bf052c5b59edcb0e';assert not a['selection_authority']
def test_fallback_is_abstain(load,upstream):
 v,_,l,_=upstream;p=program(load);p['rules'][0]['predicates'][0]['expected']='not_confirmed';c=compile_program(p,v,l);t=evaluate_program(c,v);assert t['matched_rule_id'] is None;assert t['projected_node_id']=='actionnode_69e957a950b70ef444c128a5'
