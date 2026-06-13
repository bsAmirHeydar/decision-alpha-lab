import os
import pandas as pd


class LRuleNodeDetector:

    def __init__(
        self,
        engine,
        L: int = 5,
        base_path: str = "lab/cache_nodes",
    ):
        self.engine = engine
        self.L = L
        self.base_path = base_path

        self._cache = {}
    # ==========================================
    # NODE CACHE PATH
    # ==========================================

    def _node_file(self, symbol, timeframe):

        path = os.path.join(
            self.base_path,
            "L_rule",
            f"L_{self.L}",
            symbol,
            timeframe.name,
        )

        os.makedirs(path, exist_ok=True)

        return os.path.join(
            path,
            f"{symbol}_{timeframe.name}_L{self.L}.parquet"
        )

    def _load_nodes(self, symbol, timeframe):

        file = self._node_file(symbol, timeframe)

        if not os.path.exists(file):
            return None

        return pd.read_parquet(file)

    def _save_nodes(self, nodes, symbol, timeframe):

        file = self._node_file(symbol, timeframe)

        nodes.to_parquet(file, index=False)
    # ==========================================
    # DETECT
    # ==========================================

    def detect(self, symbol, timeframe):

        df = self.engine.get_df(symbol, timeframe)
        if df is None or df.empty:
            empty = pd.DataFrame(
                columns=[
                    "time",
                    "type",
                    "price",
                    "confirmed",
                ]
            )

            key = (symbol, timeframe.name)

            self._cache[key] = {
                "nodes": empty,
                "high": empty.copy(),
                "low": empty.copy(),
            }

            return empty
        # --------------------------------------
        # Load existing node cache
        # --------------------------------------
        cached_nodes = self._load_nodes(symbol, timeframe)

        rebuild_start = 0

        # --------------------------------------
        # Incremental rebuild
        # --------------------------------------
        if cached_nodes is not None and not cached_nodes.empty:

            confirmed = cached_nodes[
                cached_nodes["confirmed"] == True
            ]

            if not confirmed.empty:

                last_confirmed_time = confirmed.iloc[-1]["time"]

                try:
                    rebuild_start = (
                        df.index[
                            df["time"] == last_confirmed_time
                        ][0]
                    )

                    rebuild_start = max(
                        rebuild_start - self.L,
                        0,
                    )

                    cached_nodes = cached_nodes[
                        cached_nodes["time"] <=
                        last_confirmed_time
                    ].reset_index(drop=True)

                except Exception:
                    # fallback:
                    # full rebuild
                    rebuild_start = 0
                    cached_nodes = None

            else:
                # no confirmed nodes
                rebuild_start = 0
                cached_nodes = None

        # --------------------------------------
        # Full rebuild
        # --------------------------------------
        if cached_nodes is None:
            cached_nodes = pd.DataFrame(
                columns=[
                    "time",
                    "type",
                    "price",
                    "confirmed",
                ]
            )

        # --------------------------------------
        # Detect nodes
        # --------------------------------------
        nodes = []

        highs = df["high"].to_numpy()
        lows = df["low"].to_numpy()
        times = df["time"].to_numpy()

        n = len(df)
        L = self.L

        for i in range(rebuild_start, n):

            # ==========================
            # LEFT SIDE
            # ==========================
            if i < L:
                continue

            left_high = highs[i - L:i]
            left_low = lows[i - L:i]

            current_high = highs[i]
            current_low = lows[i]

            high_left_ok = (
                current_high > left_high.max()
            )

            low_left_ok = (
                current_low < left_low.min()
            )

            # ==========================
            # RIGHT SIDE
            # ==========================
            available_right = min(
                L,
                n - i - 1,
            )

            right_high = highs[
                i + 1:i + 1 + available_right
            ]

            right_low = lows[
                i + 1:i + 1 + available_right
            ]

            high_right_ok = True
            low_right_ok = True

            if available_right > 0:

                high_right_ok = (
                    current_high > right_high.max()
                )

                low_right_ok = (
                    current_low < right_low.min()
                )
            # ==========================
            # HIGH NODE
            # ==========================
            if high_left_ok and high_right_ok:

                nodes.append(
                    {
                        "time": times[i],
                        "type": "HIGH",
                        "price": float(current_high),
                        "confirmed": (
                            available_right == L
                        ),
                    }
                )

            # ==========================
            # LOW NODE
            # ==========================
            if low_left_ok and low_right_ok:

                nodes.append(
                    {
                        "time": times[i],
                        "type": "LOW",
                        "price": float(current_low),
                        "confirmed": (
                            available_right == L
                        ),
                    }
                )
        # --------------------------------------
        # Merge old + new
        # --------------------------------------
        detected = pd.DataFrame(nodes)

        final = pd.concat(
            [
                cached_nodes,
                detected,
            ],
            ignore_index=True,
        )

        if not final.empty:

            final = (
                final
                .drop_duplicates(
                    subset=[
                        "time",
                        "type",
                    ],
                    keep="last",
                )
                .sort_values("time")
                .reset_index(drop=True)
            )

        # --------------------------------------
        # Save parquet
        # --------------------------------------
        self._save_nodes(
            final,
            symbol,
            timeframe,
        )

        # --------------------------------------
        # Internal caches
        # --------------------------------------
        ordered = (
            final
            .sort_values(
                "time",
                ascending=False,
            )
            .reset_index(drop=True)
        )

        key = (symbol, timeframe.name)

        self._cache[key] = {
            "nodes": ordered,
            "high": ordered[
                ordered["type"] == "HIGH"
            ].reset_index(drop=True),
            "low": ordered[
                ordered["type"] == "LOW"
            ].reset_index(drop=True),
        }
        return self._cache[key]["nodes"]    
    # ==========================================
    # INTERNAL
    # ==========================================

    def _ensure_loaded(
        self,
        symbol,
        timeframe,
    ):

        key = (symbol, timeframe.name)

        if key not in self._cache:
            self.detect(symbol, timeframe)

    # ==========================================
    # ALL NODES
    # ==========================================

    def iNode(
        self,
        symbol,
        timeframe,
        shift: int = 0,
    ):

        self._ensure_loaded(
            symbol,
            timeframe,
        )

        if shift < 0:
            raise ValueError(
                "shift must be >= 0"
            )

        key = (symbol, timeframe.name)

        nodes = self._cache[key]["nodes"]

        if shift >= len(nodes):
            return None

        return nodes.iloc[shift].to_dict()

    # ==========================================
    # HIGH NODES
    # ==========================================

    def iHighNode(
        self,
        symbol,
        timeframe,
        shift: int = 0,
    ):

        self._ensure_loaded(
            symbol,
            timeframe,
        )

        if shift < 0:
            raise ValueError(
                "shift must be >= 0"
            )

        key = (symbol, timeframe.name)

        nodes = self._cache[key]["high"]

        if shift >= len(nodes):
            return None

        return nodes.iloc[shift].to_dict()

    # ==========================================
    # LOW NODES
    # ==========================================

    def iLowNode(
        self,
        symbol,
        timeframe,
        shift: int = 0,
    ):

        self._ensure_loaded(
            symbol,
            timeframe,
        )

        if shift < 0:
            raise ValueError(
                "shift must be >= 0"
            )

        key = (symbol, timeframe.name)

        nodes = self._cache[key]["low"]

        if shift >= len(nodes):
            return None

        return nodes.iloc[shift].to_dict()