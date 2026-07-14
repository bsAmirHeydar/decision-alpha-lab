from fp_i13_release import *
def test_multi_instance_isolation(fixture,config_hash):
 xs=tuple(build_instance_identity(i,'/terminal/a','PAIR-ES-NQ','FP-EPOCH-1',config_hash) for i in range(1,5));assert verify_multi_instance(fixture,xs).status==IsolationStatus.PASS
def test_no_namespace_collision(fixture,config_hash):
 xs=tuple(build_instance_identity(i,'/terminal/a','PAIR-ES-NQ','FP-EPOCH-1',config_hash) for i in range(1,4));r=verify_multi_instance(fixture,xs);assert len(r.namespaces)==len(set(r.namespaces))
def test_same_semantics_across_instances(fixture,config_hash):
 xs=tuple(build_instance_identity(i,'/terminal/a','PAIR-ES-NQ','FP-EPOCH-1',config_hash) for i in range(1,4));assert len(set(verify_multi_instance(fixture,xs).semantic_inventory_hashes))==1
def test_pair_change_isolates(config_hash): assert build_instance_identity(1,'/t','PAIR-A','E',config_hash).instance_id!=build_instance_identity(1,'/t','PAIR-B','E',config_hash).instance_id
