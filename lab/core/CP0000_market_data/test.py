from lab.core.CP0000_market_data.connectors.MT5Connector import MT5Connector
from lab.core.CP0000_market_data.services.MarketDataEngine import MarketDataEngine
from lab.core.CP0000_market_data.utils.timeframes import Timeframe


def run_test_normal():
    print("\n=== NORMAL MODE TEST ===")

    connector = MT5Connector()
    connector.connect()

    engine = MarketDataEngine(connector)

    df = engine.fetch(
        symbol="GOLD",
        timeframe=Timeframe.M15,
        bars=500
    )

    connector.disconnect()

    print(df.shape)
    print("\nLAST 5 CANDLES:")
    print(df.tail(5))


def run_test_reset():
    print("\n=== RESET CACHE TEST ===")

    connector = MT5Connector()
    connector.connect()

    engine = MarketDataEngine(connector)

    df = engine.fetch(
        symbol="GOLD",
        timeframe=Timeframe.M15,
        bars=500,
        reset_cache=False
    )

    connector.disconnect()

    print(df.shape)
    print("\nLAST 5 CANDLES:")
    print(df.tail(5))


if __name__ == "__main__":
    run_test_normal()
    run_test_reset()