import pytest
from strategy_factory_contracts.records import BarRecord
from strategy_factory_contracts.validation import validate_terminal_symbol
from helpers import bar

@pytest.mark.parametrize("symbol", ["#US30", "NQ.c", "EURUSD.a", "XAUUSD-pro", "BTCUSD_i"])
def test_real_broker_symbol_grammar_is_supported(symbol: str) -> None:
    validate_terminal_symbol(symbol)
    assert bar(symbol=symbol).symbol == symbol

@pytest.mark.parametrize("symbol", ["", "NQ|ES", "NQ,ES", 'NQ"ES', "NQ\\ES", "NQ ES"])
def test_wire_unsafe_symbols_are_rejected(symbol: str) -> None:
    with pytest.raises(ValueError):
        validate_terminal_symbol(symbol)
