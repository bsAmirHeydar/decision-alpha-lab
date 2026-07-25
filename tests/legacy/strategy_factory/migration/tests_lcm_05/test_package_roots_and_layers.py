from tools.strategy_factory.lcm.lcm_05.io import read_json
from tools.strategy_factory.lcm.lcm_05.layering import layer_graph,is_acyclic,allowed

def test_package_roots_unique(topology_root):
    r=read_json(topology_root/'registries/package_root_registry.json');assert r['no_artifact_class_has_two_canonical_homes'];assert len({x['artifact_role_or_identity_kind'] for x in r['records']})==r['record_count']
def test_layer_graph_acyclic():
    n,e=layer_graph();assert is_acyclic(n,e)
def test_context_cannot_depend_execution():assert not allowed('CONTEXT','EXECUTION_ADAPTER')
def test_visualizer_cannot_depend_execution():assert not allowed('VISUALIZER','EXECUTION_ADAPTER')
def test_setup_can_depend_context():assert allowed('SETUP','CONTEXT')
