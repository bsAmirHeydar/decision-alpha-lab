from saed_v4_baseline_manual.compiler import compile_program
from .helpers import program

def test_compile_closed_and_deterministic(load,upstream):
 v,_,l,_=upstream;p=program(load);a=compile_program(p,v,l);b=compile_program(p,v,l);assert a==b;assert a['compiled_program_hash']==b['compiled_program_hash'];assert not a['selection_authority']
def test_rule_order_is_priority(load,upstream):
 v,_,l,_=upstream;p=program(load);p['rules'].append(dict(p['rules'][0],rule_id='lower',priority=1));x=compile_program(p,v,l);assert x['rules'][0]['priority']>x['rules'][1]['priority']
