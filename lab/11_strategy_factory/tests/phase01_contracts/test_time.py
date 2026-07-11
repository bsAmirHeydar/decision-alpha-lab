import pytest
from datetime import datetime
from strategy_factory_contracts import MarketTimestamp
from strategy_factory_contracts.validation import ContractValidationError

def test_ordering_is_epoch_based():
    a = MarketTimestamp(1000)
    b = MarketTimestamp(2000)
    assert a < b

def test_naive_datetime_rejected():
    with pytest.raises(ContractValidationError):
        MarketTimestamp.from_datetime(datetime(2026,1,1))
