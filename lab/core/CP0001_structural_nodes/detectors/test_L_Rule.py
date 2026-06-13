from lab.core.CP0000_market_data.connectors.MT5Connector import MT5Connector
from lab.core.CP0000_market_data.services.MarketDataEngine import MarketDataEngine
from lab.core.CP0000_market_data.utils.timeframes import Timeframe

from lab.core.CP0001_structural_nodes.detectors.L_Rule import (
    LRuleNodeDetector,
)


SYMBOL = "GOLD"
TIMEFRAME = Timeframe.M15
BARS = 5000
L = 2


def run_test(reset_cache=False):
    print("\n=== L NODE TEST ===")

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

        print(f"Data Shape: {df.shape}")

        detector = LRuleNodeDetector(
            engine=engine,
            L=L,
        )

        nodes = detector.detect(
            symbol=SYMBOL,
            timeframe=TIMEFRAME,
        )

        print(f"\nL = {L}")
        print(f"Total Nodes: {len(nodes)}")

        print("\nLAST 10 NODES:")

        for node in nodes[-10:]:
            print(node)

    finally:
        connector.disconnect()


if __name__ == "__main__":
    run_test(reset_cache=False)