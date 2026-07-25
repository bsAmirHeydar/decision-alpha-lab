from helpers import cube,inputs
from saed_v4_outcome_cube.replay import replay
def test_deterministic_replay():
 c=cube();r,receipt=replay(*inputs(),'fixed_conservative','1.0.0',expected_cube_hash=c.cube_hash);assert receipt['match'];assert r.cube_hash==c.cube_hash
