from lab.core.CP0000_market_data.connectors.MT5Connector import MT5Connector
from lab.core.CP0000_market_data.services.MarketDataEngine import MarketDataEngine
from lab.core.CP0000_market_data.utils.timeframes import Timeframe


SYMBOL = "GOLD"
TIMEFRAME = Timeframe.M15
BARS = 500


def print_last_5(engine, symbol, timeframe):
    print("\nLAST 5 CANDLES:")

    df = engine._get_df(symbol, timeframe)

    for i in range(-5, 0):
        print({
            "time": engine.iTime(symbol, timeframe, i),
            "open": engine.iOpen(symbol, timeframe, i),
            "high": engine.iHigh(symbol, timeframe, i),
            "low": engine.iLow(symbol, timeframe, i),
            "close": engine.iClose(symbol, timeframe, i),
            "volume": engine.iVolume(symbol, timeframe, i),
            "spread": engine.iSpread(symbol, timeframe, i),
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
    run_test(reset_cache=True)   # دانلود مجدد و ساخت cache
    run_test()                   # استفاده از cache + sync