from helpers import inputs
from saed_v4_outcome_cube.partition import partition_nodes
def test_partition_complete_and_deterministic():
 l,*_=inputs();a=partition_nodes(l,4);b=partition_nodes(l,4);assert a==b;assert sum(x['node_count'] for x in a['partitions'])==len(l['nodes'])
