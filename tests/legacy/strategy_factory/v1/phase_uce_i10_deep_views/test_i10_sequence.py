import pytest
from strategy_factory_deep_views_v3.golden import sequence_case
from strategy_factory_deep_views_v3.sequence import CausalTemporalConvModel,validate_causal_sequence
from strategy_factory_deep_views_v3.errors import DeepViewError
def test_sequence_is_deterministic_and_fits_reference_signal():
    values,targets,shape=sequence_case();a=CausalTemporalConvModel.fit(values,targets,shape);b=CausalTemporalConvModel.fit(values,targets,shape)
    assert a.state_hash==b.state_hash
    err=sum(abs(a.predict(x)[0]-y[0]) for x,y in zip(values,targets))/len(values);assert err<.01
def test_sequence_rejects_future_timestamp_and_bad_mask():
    values,_,shape=sequence_case(8)
    with pytest.raises(DeepViewError,match='future'):
        validate_causal_sequence(values[0],shape,tuple(range(shape[0]-1))+(999,),10)
    with pytest.raises(DeepViewError,match='mask'):
        validate_causal_sequence(values[0],shape,tuple(range(shape[0])),100,(1,))
