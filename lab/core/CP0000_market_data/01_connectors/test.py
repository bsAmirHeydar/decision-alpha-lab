from MT5Connector import MT5Connector

connector = MT5Connector()

connector.connect()

df = connector.fetch(
    symbol="GOLD",
    timeframe="M15",
    start="2026-01-01",
    end="2026-01-10",
)

connector.disconnect()

print(df.head())
print()
print(df.tail())
print()
print(df.shape)