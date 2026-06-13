import numpy as np


class LRuleNodeDetector:
    """
    MQL-style Structural Node Detector

    Rule:
        A candle is a node if:
        - High is greater than L candles left and right
        - OR Low is lower than L candles left and right

    Access style:
        shift-based (MQL-like)
        shift=0 -> current candle
        shift=1 -> last closed candle
    """

    def __init__(self, engine, L: int = 5):
        self.engine = engine
        self.L = L

    # =========================
    # MAIN API
    # =========================
    def detect(self, symbol, timeframe):

        df = self.engine._get_df(symbol, timeframe)

        highs = df["high"].to_numpy()
        lows = df["low"].to_numpy()
        times = df["time"].to_numpy()

        L = self.L
        n = len(df)

        nodes = []

        # NOTE:
        # we respect MQL structure:
        # ignore first/last L candles (no full window)
        for shift in range(L, n - L):

            current_high = highs[shift]
            current_low = lows[shift]

            # -------------------------
            # WINDOW
            # -------------------------
            left_high = highs[shift - L: shift]
            right_high = highs[shift + 1: shift + L + 1]

            left_low = lows[shift - L: shift]
            right_low = lows[shift + 1: shift + L + 1]

            # =========================
            # HIGH NODE CONDITION
            # =========================
            if current_high > np.max(left_high) and current_high > np.max(right_high):

                nodes.append({
                    "shift": shift,
                    "type": "HIGH",
                    "price": float(current_high),
                    "time": times[shift],
                })

            # =========================
            # LOW NODE CONDITION
            # =========================
            if current_low < np.min(left_low) and current_low < np.min(right_low):

                nodes.append({
                    "shift": shift,
                    "type": "LOW",
                    "price": float(current_low),
                    "time": times[shift],
                })

        return nodes

    # =========================
    # MQL STYLE HELPERS (optional)
    # =========================
    def is_high_node(self, symbol, timeframe, shift: int):

        df = self.engine._get_df(symbol, timeframe)
        highs = df["high"].to_numpy()

        L = self.L
        if shift < L or shift >= len(df) - L:
            return False

        current = highs[shift]

        return (
            current > np.max(highs[shift - L:shift]) and
            current > np.max(highs[shift + 1:shift + L + 1])
        )

    def is_low_node(self, symbol, timeframe, shift: int):

        df = self.engine._get_df(symbol, timeframe)
        lows = df["low"].to_numpy()

        L = self.L
        if shift < L or shift >= len(df) - L:
            return False

        current = lows[shift]

        return (
            current < np.min(lows[shift - L:shift]) and
            current < np.min(lows[shift + 1:shift + L + 1])
        )