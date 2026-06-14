import os
import numpy as np
import pandas as pd


class M0001RTV:

    def __init__(
        self,
        engine,
        detector,
        zone_ratio: float = 0.9,
        exit_gap: int = 6,
        consumption_mode: str = "hunt",
        base_path: str = "lab/cache_metrics",
    ):
        """
        Parameters
        ----------
        engine :
            MarketDataEngine

        detector :
            LRuleNodeDetector

        zone_ratio :
            Example:
                node=100
                extreme=150
                ratio=0.9

                zone = [95, 105]

        exit_gap :
            Number of consecutive candles completely outside
            the zone required to terminate an event.

        consumption_mode :
            "touch"
                First completed event consumes node.

            "hunt"
                Node survives until actual hunt.
                LOW  -> low  < node_price
                HIGH -> high > node_price

        base_path :
            Metric cache path.
        """

        self.engine = engine
        self.detector = detector

        self.zone_ratio = zone_ratio
        self.exit_gap = exit_gap
        self.consumption_mode = consumption_mode

        self.base_path = base_path

        self._cache = {}

    # ==================================================
    # CACHE PATHS
    # ==================================================

    def _metric_file(
        self,
        symbol,
        timeframe,
    ):

        path = os.path.join(
            self.base_path,
            "M0001_relative_territory_volatility",
            f"L_{self.detector.L}",
            symbol,
            timeframe.name,
        )

        os.makedirs(
            path,
            exist_ok=True,
        )

        return os.path.join(
            path,
            (
                f"{symbol}_"
                f"{timeframe.name}_"
                f"L{self.detector.L}_"
                f"ZR{self.zone_ratio}_"
                f"EG{self.exit_gap}_"
                f"{self.consumption_mode}.parquet"
            ),
        )
    
        def _load_cache(
        self,
        symbol,
        timeframe,
    ):

        file = self._metric_file(
            symbol,
            timeframe,
        )

        if not os.path.exists(file):
            return None

        return pd.read_parquet(file)


    def _save_cache(
        self,
        result,
        symbol,
        timeframe,
    ):

        file = self._metric_file(
            symbol,
            timeframe,
        )

        result.to_parquet(
            file,
            index=False,
        )
    # ==================================================
    # WICK-BASED LOG MOVEMENT
    # ==================================================

    def _log_move(
        self,
        high,
        low,
    ):

        move = abs(high - low)

        if move <= 0:
            return 0.0

        return float(
            np.log(move)
        )
    # ==================================================
    # ZONE CHECK
    # ==================================================

    def _in_zone(
        self,
        high,
        low,
        lower,
        upper,
    ):

        return not (
            high < lower
            or
            low > upper
        )
    # ==================================================
    # DYNAMIC ZONE
    # ==================================================

    def _build_zone(
        self,
        node_price,
        extreme,
    ):

        distance = abs(
            extreme - node_price
        )

        half_width = (
            distance
            *
            (1.0 - self.zone_ratio)
        )

        lower = (
            node_price
            - half_width
        )

        upper = (
            node_price
            + half_width
        )

        return (
            lower,
            upper,
        )
    # ==================================================
    # INITIAL NODE STATES
    # ==================================================

    def _initialize_node_states(
        self,
        nodes_df,
        df,
    ):

        states = []

        confirmed_nodes = (
            nodes_df[
                nodes_df["confirmed"] == True
            ]
            .reset_index(drop=True)
        )

        for node_id, node in confirmed_nodes.iterrows():

            idx_list = df.index[
                df["time"] == node["time"]
            ].tolist()

            if not idx_list:
                continue

            candle_index = idx_list[0]

            node_price = float(
                node["price"]
            )

            node_type = node["type"]

            states.append(
                {
                    # ---------------------
                    # Identity
                    # ---------------------
                    "node_id": node_id,

                    "node_time":
                        node["time"],

                    "node_index":
                        candle_index,

                    "node_price":
                        node_price,

                    "node_type":
                        node_type,

                    # ---------------------
                    # Tracking
                    # ---------------------
                    "extreme":
                        node_price,

                    "consumed":
                        False,

                    # ---------------------
                    # Event
                    # ---------------------
                    "in_event":
                        False,

                    "revisit_id":
                        0,

                    "outside_count":
                        0,

                    "entry_index":
                        None,

                    "entry_time":
                        None,

                    "exit_index":
                        None,

                    "exit_time":
                        None,

                    # ---------------------
                    # Zone
                    # ---------------------
                    "territory_lower":
                        None,

                    "territory_upper":
                        None,

                    # ---------------------
                    # Metrics
                    # ---------------------
                    "inside_logs":
                        [],

                    "before_logs":
                        [],

                    # ---------------------
                    # Event freeze
                    # ---------------------
                    "frozen_extreme":
                        None,

                    # ---------------------
                    # Hunt
                    # ---------------------
                    "hunted":
                        False,
                    "revisit_seeded": False,
                }
            )

        return states
    # ==================================================
    # UPDATE EXTREME
    # ==================================================

    def _update_extreme(
        self,
        state,
        high,
        low,
    ):

        if state["in_event"]:
            return

        if state["node_type"] == "LOW":

            if high > state["extreme"]:

                state["extreme"] = high

        else:

            if low < state["extreme"]:

                state["extreme"] = low
    # ==================================================
    # UPDATE TERRITORY
    # ==================================================

    def _update_territory(
        self,
        state,
    ):

        lower, upper = (
            self._build_zone(
                state["node_price"],
                state["extreme"],
            )
        )

        state["territory_lower"] = (
            lower
        )

        state["territory_upper"] = (
            upper
        )
    # ==================================================
    # HUNT CHECK
    # ==================================================

    def _check_hunt(
        self,
        state,
        high,
        low,
    ):

        if state["hunted"]:
            return

        if state["node_type"] == "LOW":

            if low < state["node_price"]:

                state["hunted"] = True

        else:

            if high > state["node_price"]:

                state["hunted"] = True

    # ==================================================
    # CONSUMPTION
    # ==================================================

    def _consume_if_needed(
        self,
        state,
    ):

        if (
            self.consumption_mode
            ==
            "touch"
        ):

            state["consumed"] = True

        elif (
            self.consumption_mode
            ==
            "hunt"
        ):

            if state["hunted"]:

                state["consumed"] = True
    # ==================================================
    # COMPUTE
    # ==================================================

    def compute(
        self,
        symbol,
        timeframe,
        reset_cache: bool = False,
    ):

        if not reset_cache:

            cached = self._load_cache(
                symbol,
                timeframe,
            )

            if cached is not None:

                return cached

        df = self.engine.get_df(
            symbol,
            timeframe,
        )

        if df is None or df.empty:

            return pd.DataFrame()

        nodes_df = self.detector.detect(
            symbol,
            timeframe,
        )

        states = self._initialize_node_states(
            nodes_df,
            df,
        )

        events = []

        # ==========================================
        # LIVE MARKET SIMULATION
        # ==========================================

        for i in range(len(df)):

            candle = df.iloc[i]

            high = candle["high"]
            low = candle["low"]
            time = candle["time"]

            log_move = self._log_move(
                high,
                low,
            )

            for state in states:


                if i <= state["node_index"]:

                    continue


                if state["consumed"]:

                    continue
                if not state["in_event"]:
                    if state["extreme"] is None:
                        
                        inside = self._in_zone(
                            high,
                            low,
                            state["territory_lower"],
                            state["territory_upper"],
                        )

                        if not inside:
                            continue

                        if state["node_type"] == "LOW":
                            state["extreme"] = high
                        else:
                            state["extreme"] = low

                        state["revisit_seeded"] = True
                    self._update_extreme(
                        state,
                        high,
                        low,
                    )

                    self._update_territory(
                        state,
                    )

                    self._check_hunt(
                        state,
                        high,
                        low,
                    )
                    state[
                        "before_logs"
                    ].append(
                        log_move
                    )               
                    inside = self._in_zone(
                        high,
                        low,
                        state[
                            "territory_lower"
                        ],
                        state[
                            "territory_upper"
                        ],
                    )            
                    if inside:

                        state[
                            "in_event"
                        ] = True

                        state[
                            "revisit_id"
                        ] += 1

                        state[
                            "outside_count"
                        ] = 0

                        state[
                            "entry_index"
                        ] = i

                        state[
                            "entry_time"
                        ] = time

                        state[
                            "inside_logs"
                        ] = []

                        state[
                            "frozen_extreme"
                        ] = state[
                            "extreme"
                        ]
                # ==================================
                # ACTIVE EVENT
                # ==================================

                else:

                    inside = self._in_zone(
                        high,
                        low,
                        state[
                            "territory_lower"
                        ],
                        state[
                            "territory_upper"
                        ],
                    )
                    state[
                        "inside_logs"
                    ].append(
                        log_move
                    )
                    if inside:

                        state[
                            "outside_count"
                        ] = 0
                    else:

                        state[
                            "outside_count"
                        ] += 1
                    if (
                        state[
                            "outside_count"
                        ]
                        <
                        self.exit_gap
                    ):

                        continue
                    state[
                        "exit_index"
                    ] = i

                    state[
                        "exit_time"
                    ] = time
                    N = len(
                        state[
                            "inside_logs"
                        ]
                    )

                    before = (
                        state[
                            "before_logs"
                        ][-N:]
                    )

                    inside_logs = (
                        state[
                            "inside_logs"
                        ]
                    )
                    if (
                        N == 0
                        or
                        len(before) < N
                    ):

                        state[
                            "in_event"
                        ] = False

                        state[
                            "outside_count"
                        ] = 0

                        continue
                    mean_inside = float(
                        np.mean(
                            inside_logs
                        )
                    )

                    mean_before = float(
                        np.mean(
                            before
                        )
                    )

                    median_inside = float(
                        np.median(
                            inside_logs
                        )
                    )

                    median_before = float(
                        np.median(
                            before
                        )
                    )
                    RTV = None

                    if mean_before != 0:

                        RTV = (
                            mean_inside
                            /
                            mean_before
                        )
                    events.append(
                        {
                            "node_id":
                                state[
                                    "node_id"
                                ],

                            "node_time":
                                state[
                                    "node_time"
                                ],

                            "node_type":
                                state[
                                    "node_type"
                                ],

                            "node_price":
                                state[
                                    "node_price"
                                ],

                            "revisit_id":
                                state[
                                    "revisit_id"
                                ],

                            "entry_time":
                                state[
                                    "entry_time"
                                ],

                            "exit_time":
                                state[
                                    "exit_time"
                                ],

                            "event_length":
                                N,

                            "territory_lower":
                                state[
                                    "territory_lower"
                                ],

                            "territory_upper":
                                state[
                                    "territory_upper"
                                ],

                            "expansion_extreme":
                                state[
                                    "frozen_extreme"
                                ],

                            "mean_inside":
                                mean_inside,

                            "mean_before":
                                mean_before,

                            "median_inside":
                                median_inside,

                            "median_before":
                                median_before,

                            "RTV":
                                RTV,

                            "hunted":
                                state[
                                    "hunted"
                                ],
                        }
                    )
                    # ==================================
                    # TOUCH CONSUMPTION
                    # ==================================

                    if (
                        self.consumption_mode
                        ==
                        "touch"
                    ):

                        state[
                            "consumed"
                        ] = True
                    # ==================================
                    # HUNT CONSUMPTION
                    # ==================================

                    elif (
                        self.consumption_mode
                        ==
                        "hunt"
                    ):

                        if state[
                            "hunted"
                        ]:

                            state[
                                "consumed"
                            ] = True
                    # ==================================
                    # EVENT CLOSED
                    # ==================================

                    state[
                        "in_event"
                    ] = False

                    state[
                        "outside_count"
                    ] = 0
                    if state[
                        "consumed"
                    ]:

                        continue
                    # ==================================
                    # PREPARE REVISIT
                    # ==================================

                    state[
                        "before_logs"
                    ] = []

                    state[
                        "inside_logs"
                    ] = []

                    state[
                        "entry_index"
                    ] = None

                    state[
                        "entry_time"
                    ] = None

                    state[
                        "exit_index"
                    ] = None

                    state[
                        "exit_time"
                    ] = None

                    state["before_logs"] = []

                    state["inside_logs"] = []

                    state["entry_index"] = None
                    state["entry_time"] = None

                    state["exit_index"] = None
                    state["exit_time"] = None

                    state["frozen_extreme"] = None

                    state["extreme"] = None