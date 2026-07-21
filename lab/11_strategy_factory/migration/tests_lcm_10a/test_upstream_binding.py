from .conftest import j
def test_exact_lcm09b_handoff_and_seed_count():
 d=j('input/upstream_binding.json');assert d['lcm09b_handoff_digest']=='sha256:104e4567686811724302be71f49f08f382196bed235c1fd969ebec1e58cd67ac';assert d['setup_dependency_seed_count']==60
