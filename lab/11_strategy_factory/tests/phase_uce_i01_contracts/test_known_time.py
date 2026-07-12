from datetime import datetime
import pytest
from strategy_factory_contracts_v3.errors import KnownTimeError
from strategy_factory_contracts_v3.fixtures import golden_time_chain
from strategy_factory_contracts_v3.time_model import KnownTimeChain,UtcInstant

def test_golden_chain_and_feature_cut():
    chain=golden_time_chain()
    chain.assert_feature_known(UtcInstant(1783800000000,"feature"))
    with pytest.raises(KnownTimeError) as error:chain.assert_feature_known(UtcInstant(1783800000001,"feature"))
    assert error.value.code=="future_feature"

def test_reversed_chain_rejected():
    with pytest.raises(KnownTimeError) as error:
        KnownTimeChain(UtcInstant(10),UtcInstant(9),UtcInstant(10),UtcInstant(10),UtcInstant(10))
    assert error.value.code=="causal_time_reversal"

def test_fill_requires_action():
    with pytest.raises(KnownTimeError) as error:
        KnownTimeChain(UtcInstant(1),UtcInstant(1),UtcInstant(1),UtcInstant(1),UtcInstant(1),fill_time=UtcInstant(2))
    assert error.value.code=="fill_without_action"

def test_naive_datetime_rejected():
    with pytest.raises(KnownTimeError) as error:UtcInstant.from_datetime(datetime(2026,7,12,10,0,0))
    assert error.value.code=="naive_datetime"
