import pytest
from helpers import load
from saed_v4_outcome_cube import ContextSnapshot
from saed_v4_outcome_cube.errors import KnownTimeError
def test_future_feature_fails_closed():
 with pytest.raises(KnownTimeError):ContextSnapshot.from_mapping(load('examples/legacy/strategy_factory/saed_v4_08/negative/future_feature_context.json'))
