import pytest
from strategy_factory_outcome.fixtures import bar
from strategy_factory_outcome import *
def test_observation_id_stable():assert bar(1,2000,100,101,99,100.5).observation_id==bar(1,2000,100,101,99,100.5).observation_id
def test_invalid_ohlc_rejected():
    with pytest.raises(ValueError):PriceObservation("EURUSD",ObservationKind.CLOSED_BAR,DataFidelity.BAR_APPROXIMATION,1,2000,1000,2000,100,99,101,100,0,None,None,"src")
def test_bid_ask_pair_required():
    with pytest.raises(ValueError):PriceObservation("EURUSD",ObservationKind.TICK,DataFidelity.REAL_TICK,1,2000,2000,2000,100,100,100,100,0,99,None,"src")
