# lab/core/CP0000_market_data/connectors/MT5Connector.py

from datetime import datetime, timedelta
import difflib

import MetaTrader5 as mt5
import pandas as pd

from lab.core.CP0000_market_data.exceptions import (
    MT5ConnectionError,
    SymbolNotFoundError,
    NoDataError,
    InvalidTimeframeError,
)

from lab.core.CP0000_market_data.utils.timeframes import Timeframe


class MT5Connector:
    """
    Institutional-grade MetaTrader 5 data connector.
    """

    def __init__(self):
        self.connected = False

    # =========================
    # CONNECTION
    # =========================

    def connect(self):
        if self.connected:
            return

        if not mt5.initialize():
            raise MT5ConnectionError(f"MT5 init failed: {mt5.last_error()}")

        self.connected = True

    def disconnect(self):
        if self.connected:
            mt5.shutdown()
            self.connected = False

    # =========================
    # SYMBOL VALIDATION
    # =========================

    def _validate_symbol(self, symbol: str):
        info = mt5.symbol_info(symbol)

        if info is None:
            available = mt5.symbols_get()
            available_names = [s.name for s in available[:100]]

            suggestions = difflib.get_close_matches(
                symbol,
                available_names,
                n=5,
                cutoff=0.4,
            )

            raise SymbolNotFoundError(
                f"Symbol '{symbol}' not found.\n"
                f"Suggestions: {suggestions if suggestions else 'None'}"
            )

    # =========================
    # FETCH ENGINE
    # =========================

    def fetch(
        self,
        symbol: str,
        timeframe: Timeframe,
        start: datetime | None = None,
        end: datetime | None = None,
        bars: int | None = None,
        days: int | None = None,
        strict: bool = True,
    ) -> pd.DataFrame:

        if not self.connected:
            raise MT5ConnectionError(
                "MT5 is not connected. Call connect() first."
            )

        if not isinstance(timeframe, Timeframe):
            raise InvalidTimeframeError(
                "Timeframe must be Timeframe Enum."
            )

        self._validate_symbol(symbol)

        tf = timeframe.value

        # ==================================
        # 1) EXPLICIT RANGE
        # ==================================
        if start is not None and end is not None:

            rates = mt5.copy_rates_range(
                symbol,
                tf,
                start,
                end,
            )

        # ==================================
        # 2) DAYS MODE
        # ==================================
        elif days is not None:

            end_time = datetime.now()
            start_time = end_time - timedelta(days=days)

            rates = mt5.copy_rates_range(
                symbol,
                tf,
                start_time,
                end_time,
            )

        # ==================================
        # 3) LAST N BARS
        # ==================================
        elif bars is not None:

            rates = mt5.copy_rates_from_pos(
                symbol,
                tf,
                0,
                bars,
            )

        # ==================================
        # 4) FULL HISTORY
        # ==================================
        else:

            chunks = []
            offset = 0
            chunk_size = 1000

            while True:

                chunk = mt5.copy_rates_from_pos(
                    symbol,
                    tf,
                    offset,
                    chunk_size,
                )

                if chunk is None:
                    break

                if len(chunk) == 0:
                    break

                chunks.append(pd.DataFrame(chunk))

                if len(chunk) < chunk_size:
                    break

                offset += chunk_size

            if len(chunks) == 0:
                rates = []
            else:
                df = pd.concat(
                    chunks,
                    ignore_index=True,
                )

                df["time"] = pd.to_datetime(
                    df["time"],
                    unit="s",
                )

                df = (
                    df[
                        [
                            "time",
                            "open",
                            "high",
                            "low",
                            "close",
                            "tick_volume",
                            "spread",
                            "real_volume",
                        ]
                    ]
                    .drop_duplicates(
                        subset=["time"]
                    )
                    .sort_values("time")
                    .reset_index(drop=True)
                )

                df.attrs["timezone"] = "terminal"

                return df

        # ==================================
        # ERROR HANDLING
        # ==================================

        if rates is None:

            raise MT5ConnectionError(
                f"MT5 error: {mt5.last_error()}"
            )

        if len(rates) == 0:

            if strict:
                raise NoDataError(
                    f"No data found for "
                    f"{symbol} {timeframe.name}"
                )

            return pd.DataFrame()

        # ==================================
        # DATAFRAME BUILD
        # ==================================

        df = pd.DataFrame(rates)

        df["time"] = pd.to_datetime(
            df["time"],
            unit="s",
        )

        df = (
            df[
                [
                    "time",
                    "open",
                    "high",
                    "low",
                    "close",
                    "tick_volume",
                    "spread",
                    "real_volume",
                ]
            ]
            .drop_duplicates(
                subset=["time"]
            )
            .sort_values("time")
            .reset_index(drop=True)
        )

        df.attrs["timezone"] = "terminal"

        return df
    
    # =========================
    # CONTEXT MANAGER
    # =========================

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()