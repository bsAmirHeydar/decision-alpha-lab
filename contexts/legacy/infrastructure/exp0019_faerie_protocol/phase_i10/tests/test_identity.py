from fp_i10_indicator import *

def test_identity_deterministic(config): assert build_instance_identity(config,1,'TERM').identity_hash==build_instance_identity(config,1,'TERM').identity_hash
def test_chart_isolation(config): assert build_instance_identity(config,1,'TERM').instance_id!=build_instance_identity(config,2,'TERM').instance_id
def test_terminal_isolation(config): assert build_instance_identity(config,1,'A').instance_id!=build_instance_identity(config,1,'B').instance_id
def test_namespace_scoped(config): assert build_instance_identity(config,1,'TERM').object_namespace.startswith('FP19::FPINST_')
def test_checkpoint_key_unique(config): assert build_instance_identity(config,1,'TERM').checkpoint_key!=build_instance_identity(config,2,'TERM').checkpoint_key
