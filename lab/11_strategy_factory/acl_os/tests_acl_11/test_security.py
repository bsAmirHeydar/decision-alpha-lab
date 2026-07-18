from tools.strategy_factory.acl_os.acl_11.security import build_tcb
def test_tcb_excludes_training(): assert 'TRAINING_ENGINE' in build_tcb()['forbidden_component_classes']
def test_tcb_excludes_dynamic_plugins(): assert 'ARBITRARY_PLUGIN_LOADER' in build_tcb()['forbidden_component_classes']
def test_no_production_tcb_claim(): assert build_tcb()['production_tcb_verified'] is False
