from datetime import datetime
import MetaTrader5 as mt5
import pandas as pd


class MT5Connector:
    """
    Connector responsible only for:
    - Connecting to MetaTrader 5
    - Fetching raw OHLCV data
    - Returning a standardized DataFrame
    """

    TIMEFRAME_MAP = {
        "M1": mt5.TIMEFRAME_M1,
        "M2": mt5.TIMEFRAME_M2,
        "M3": mt5.TIMEFRAME_M3,
        "M4": mt5.TIMEFRAME_M4,
        "M5": mt5.TIMEFRAME_M5,
        "M6": mt5.TIMEFRAME_M6,
        "M10": mt5.TIMEFRAME_M10,
        "M12": mt5.TIMEFRAME_M12,
        "M15": mt5.TIMEFRAME_M15,
        "M20": mt5.TIMEFRAME_M20,
        "M30": mt5.TIMEFRAME_M30,
        "H1": mt5.TIMEFRAME_H1,
        "H2": mt5.TIMEFRAME_H2,
        "H3": mt5.TIMEFRAME_H3,
        "H4": mt5.TIMEFRAME_H4,
        "H6": mt5.TIMEFRAME_H6,
        "H8": mt5.TIMEFRAME_H8,
        "H12": mt5.TIMEFRAME_H12,
        "D1": mt5.TIMEFRAME_D1,
        "W1": mt5.TIMEFRAME_W1,
        "MN1": mt5.TIMEFRAME_MN1,
    }

    def __init__(self):
        self.connected = False

    def connect(self):
        """
        Initialize MT5 connection.
        """

        if self.connected:
            return

        if not mt5.initialize():
            raise RuntimeError(
                f"Failed to initialize MT5: {mt5.last_error()}"
            )

        self.connected = True

    def disconnect(self):
        """
        Shutdown MT5 connection.
        """

        if self.connected:
            mt5.shutdown()
            self.connected = False

    def fetch(
        self,
        symbol: str,
        timeframe: str,
        start: str,
        end: str,
    ) -> pd.DataFrame:
        """
        Fetch OHLCV data from MT5.

        Parameters
        ----------
        symbol : str
            e.g. "XAUUSD"

        timeframe : str
            e.g. "M15"

        start : str
            e.g. "2024-01-01"

        end : str
            e.g. "2024-02-01"

        Returns
        -------
        pandas.DataFrame
        """

        if not self.connected:
            raise RuntimeError(
                "MT5 is not connected. Call connect() first."
            )

        if timeframe not in self.TIMEFRAME_MAP:
            raise ValueError(
                f"Unsupported timeframe: {timeframe}"
            )

        start_dt = datetime.fromisoformat(start)
        end_dt = datetime.fromisoformat(end)

        rates = mt5.copy_rates_range(
            symbol,
            self.TIMEFRAME_MAP[timeframe],
            start_dt,
            end_dt,
        )

        if rates is None:
            raise RuntimeError(
                f"Failed to fetch data: {mt5.last_error()}"
            )

        if len(rates) == 0:
            raise ValueError(
                f"No data returned for {symbol} {timeframe}"
            )

        df = pd.DataFrame(rates)

        # Standardize datetime
        df["time"] = pd.to_datetime(
            df["time"],
            unit="s",
        )

        # Standardize column order
        columns = [
            "time",
            "open",
            "high",
            "low",
            "close",
            "tick_volume",
            "spread",
            "real_volume",
        ]

        df = df[columns]

        return df