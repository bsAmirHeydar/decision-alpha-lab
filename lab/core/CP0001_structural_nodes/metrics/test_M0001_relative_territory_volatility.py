from lab.core.CP0000_market_data.connectors.MT5Connector import (
    MT5Connector,
)
from lab.core.CP0000_market_data.services.MarketDataEngine import (
    MarketDataEngine,
)
from lab.core.CP0000_market_data.utils.timeframes import (
    Timeframe,
)

from lab.core.CP0001_structural_nodes.detectors.L_Rule import (
    LRuleNodeDetector,
)

from lab.core.CP0001_structural_nodes.metrics.M0001_relative_territory_volatility import (
    M0001RTV,
)


SYMBOL = "#US30"
TIMEFRAME = Timeframe.M15
BARS = 5000

L = 5
ZONE_RATIO = 0.9
EXIT_GAP = 6


def run_test(
    reset_market_cache=False,
):

    print("\n=== M0001 RTV TEST ===")

    connector = MT5Connector()
    connector.connect()

    try:

        engine = MarketDataEngine(connector)

        df = engine.fetch(
            symbol=SYMBOL,
            timeframe=TIMEFRAME,
            bars=BARS,
            reset_cache=reset_market_cache,
        )

        print(f"Market Bars: {len(df)}")

        detector = LRuleNodeDetector(
            engine=engine,
            L=L,
        )

        nodes = detector.detect(
            symbol=SYMBOL,
            timeframe=TIMEFRAME,
        )

        confirmed_nodes = nodes[nodes["confirmed"] == True]

        print(f"Confirmed Nodes: {len(confirmed_nodes)}")

        metric = M0001RTV(
            engine=engine,
            L=L,
            zone_ratio=ZONE_RATIO,
            exit_gap=EXIT_GAP,
        )

        result = metric.compute(
            symbol=SYMBOL,
            timeframe=TIMEFRAME,
        )

        print(f"\nTotal Events: {len(result)}")

        if result.empty:
            print("\nNo events found.")
            return

        print("\nColumns:")
        print(result.columns.tolist())

        print("\nLAST 10 EVENTS:")
        print(result.tail(10).to_string(index=False))

        print("\nRTV Summary:")
        print(result["RTV"].describe())

        print("\nMean RTV:", result["RTV"].mean())
        print("Median RTV:", result["RTV"].median())

        print(
            "Hunted Events:",
            int(result["hunted"].sum()) if "hunted" in result else "N/A",
        )

        print("Unique Nodes:", result["node_time"].nunique())

        print("Max Revisit:", result["revisit_id"].max())

    finally:
        connector.disconnect()


if __name__ == "__main__":
    run_test(reset_market_cache=False)