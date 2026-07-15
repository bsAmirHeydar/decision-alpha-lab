import pytest
from helpers import inputs,load
from saed_v4_outcome_cube import PriceObservation,build_cube
from saed_v4_outcome_cube.errors import PathError
def test_non_monotonic_path_fails():
 lattice,handoff,ctx,_,pol,reg=inputs();obs=[PriceObservation.from_mapping(x) for x in load('lab/11_strategy_factory/examples/saed_v4_08/negative/non_monotonic_path.json')['observations']]
 with pytest.raises(PathError):build_cube(lattice,handoff,ctx,obs,pol,reg,'fixed_conservative','1.0.0')
def test_negative_spread_fails():
 with pytest.raises(PathError):[PriceObservation.from_mapping(x) for x in load('lab/11_strategy_factory/examples/saed_v4_08/negative/negative_spread_path.json')['observations']]
