from .helpers import inputs
from saed_v4_outcome_cube.compiler import compile_spec
def test_ordinary_specs_have_positive_risk():
 lattice,_,ctx,*_=inputs()
 for n in lattice['nodes']:
  s=compile_spec(n,ctx)
  if s.action_class=='ordinary':assert (s.entry_price-s.stop_price)*s.direction>0 and s.target_price>s.entry_price
def test_component_hashes_preserved():
 lattice,_,ctx,*_=inputs();n=next(x for x in lattice['nodes'] if x['action_class']=='ordinary');s=compile_spec(n,ctx);assert len(s.source_component_hashes)==len(n['instantiated_components'])
