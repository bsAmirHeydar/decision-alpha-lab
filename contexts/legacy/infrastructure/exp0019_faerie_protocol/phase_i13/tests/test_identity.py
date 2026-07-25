from fp_i13_release import *
def test_identity_deterministic(config_hash):
 a=build_instance_identity(1,'/x','PAIR','E',config_hash);b=build_instance_identity(1,'/x','PAIR','E',config_hash);assert a==b
def test_chart_id_changes_instance(config_hash): assert build_instance_identity(1,'/x','PAIR','E',config_hash).instance_id!=build_instance_identity(2,'/x','PAIR','E',config_hash).instance_id
def test_chart_timeframe_not_in_identity(config_hash):
 a=build_instance_identity(1,'/x','PAIR','E',config_hash);assert 'timeframe' not in a.instance_id.lower()
def test_namespaces_scoped(instance): assert instance.object_namespace.startswith('FP19::') and instance.object_namespace.endswith('::')
def test_checkpoint_and_export_keys_differ(instance): assert instance.checkpoint_key!=instance.export_file_key
