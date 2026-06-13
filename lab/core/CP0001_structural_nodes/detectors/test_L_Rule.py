from lab.core.CP0000_market_data.connectors.MT5Connector import MT5Connector
from lab.core.CP0000_market_data.services.MarketDataEngine import MarketDataEngine
from lab.core.CP0000_market_data.utils.timeframes import Timeframe

from lab.core.CP0001_structural_nodes.detectors.L_Rule import (
    LRuleNodeDetector,
)


SYMBOL = "GOLD"
TIMEFRAME = Timeframe.M15
BARS = 5000
L = 4


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

        # -------------------------
        # آخرین 10 نود (جدیدترین)
        # -------------------------
        print("\nLAST 10 ALL NODES:")

        for shift in range(min(10, len(nodes))):
            node = detector.iNode(
                SYMBOL,
                TIMEFRAME,
                shift,
            )

            print(node)

        # -------------------------
        # آخرین 5 قله
        # -------------------------
        print("\nLAST 5 HIGH NODES:")

        for shift in range(5):
            node = detector.iHighNode(
                SYMBOL,
                TIMEFRAME,
                shift,
            )

            if node is None:
                break

            print(node)

        # -------------------------
        # آخرین 5 دره
        # -------------------------
        print("\nLAST 5 LOW NODES:")

        for shift in range(5):
            node = detector.iLowNode(
                SYMBOL,
                TIMEFRAME,
                shift,
            )

            if node is None:
                break

            print(node)

    finally:
        connector.disconnect()


if __name__ == "__main__":
    run_test(reset_cache=True)   # ساخت مجدد cache
    run_test(reset_cache=False)  # تست sync و استفاده از cache