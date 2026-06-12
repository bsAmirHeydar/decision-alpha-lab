# lab/core/CP0000_market_data/exceptions.py


class MT5ConnectionError(Exception):
    """Raised when MT5 fails to initialize or shutdown properly."""
    pass


class SymbolNotFoundError(Exception):
    """Raised when the requested symbol does not exist in MT5."""
    pass


class NoDataError(Exception):
    """Raised when MT5 returns no data for the requested query."""
    pass


class InvalidTimeframeError(Exception):
    """Raised when an unsupported timeframe is provided."""
    pass