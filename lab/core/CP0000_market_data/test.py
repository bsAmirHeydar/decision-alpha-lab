from lab.core.CP0000_market_data.connectors.MT5Connector import MT5Connector
from lab.core.CP0000_market_data.services.MarketDataEngine import MarketDataEngine
from lab.core.CP0000_market_data.utils.timeframes import Timeframe


SYMBOL = "GOLD"
TIMEFRAME = Timeframe.M15
BARS = 5000


def print_last_5(engine, symbol, timeframe):
    print("\nLAST 5 CANDLES (MQL5 style):")

    for shift in range(4, -1, -1):
        print({
            "shift": shift,
            "time": engine.iTime(symbol, timeframe, shift),
            "open": engine.iOpen(symbol, timeframe, shift),
            "high": engine.iHigh(symbol, timeframe, shift),
            "low": engine.iLow(symbol, timeframe, shift),
            "close": engine.iClose(symbol, timeframe, shift),
            "volume": engine.iVolume(symbol, timeframe, shift),
            "spread": engine.iSpread(symbol, timeframe, shift),
        })


def run_test(reset_cache=False):
    mode = "RESET CACHE" if reset_cache else "NORMAL"

    print(f"\n=== {mode} TEST ===")

    connector = MT5Connector()
    connector.connect()

    try:
        engine = MarketDataEngine(connector)

        df = engine.fetch(
            symbol=SYMBOL,
            timeframe=TIMEFRAME,
            bars=BARS,
            reset_cache=reset_cache,
        )

        print(f"Shape: {df.shape}")

        print_last_5(
            engine,
            SYMBOL,
            TIMEFRAME,
        )

    finally:
        connector.disconnect()


if __name__ == "__main__":
    run_test(reset_cache=True)    # rebuild cache
    run_test(reset_cache=False)   # cache + sync