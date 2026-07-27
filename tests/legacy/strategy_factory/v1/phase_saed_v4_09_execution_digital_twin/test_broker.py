from .helpers import inputs
from saed_v4_execution_twin.models import ExecutionTwinProfile
from saed_v4_execution_twin.broker import normalize_volume,evaluate_broker_feasibility

def test_volume_normalization_is_bounded():
    *_,m=inputs();p=ExecutionTwinProfile.from_mapping(m);assert normalize_volume(.104,p.broker)==.1

def test_skip_is_non_order_feasible():
    *_,m=inputs();p=ExecutionTwinProfile.from_mapping(m);r=evaluate_broker_feasibility('skip',p.order_volume,{},p.broker);assert r.feasible and r.normalized_volume==0
