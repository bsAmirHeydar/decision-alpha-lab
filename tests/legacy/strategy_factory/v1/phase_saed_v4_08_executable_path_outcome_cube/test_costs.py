from .helpers import inputs
from saed_v4_outcome_cube.costs import compute_cost
def test_cost_identity_and_net_math():
 *_,reg=inputs();m=reg.resolve('fixed_conservative','1.0.0');c=compute_cost(m,10,0.2,0.2);assert c.total_cost_r>0;assert c.cost_hash
