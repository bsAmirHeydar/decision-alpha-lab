from datetime import datetime
from lab.core.CP0000_market_data.connectors.MT5Connector import MT5Connector
from lab.core.CP0000_market_data.utils.timeframes import Timeframe

connector = MT5Connector()
connector.connect()

df = connector.fetch(
    symbol="GOLD",
    timeframe=Timeframe.M15,
    bars=2000,
)
connector.disconnect()

print(df.head())
print("ROWS:", len(df))
print("START:", df["time"].min())
print("END:", df["time"].max())