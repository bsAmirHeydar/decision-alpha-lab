# EXP0015 CME Live Provider Patch

This patch makes the EXP0015 data bridge able to pull CME-price bars in practice.

## Provider modes

- `databento_historical`: licensed CME/Globex historical bars through Databento.
- `databento_live`: licensed CME/Globex live 1-minute OHLCV stream through Databento.
- `yahoo_delayed`: delayed ES/NQ futures fallback for quick testing without CME credentials.

## Boundary

MQL5 remains source-agnostic. Providers write:

```text
data/cme/bars/ES_M1.csv
data/cme/bars/NQ_M1.csv
```

The existing `dal_cme_bridge.py --mode live_csv_tail` copies those files into MT5 Common Files:

```text
Common/Files/dal/cme/ES_M1.csv
Common/Files/dal/cme/NQ_M1.csv
```

EXP0015 reads them through `IMD_DS_EXTERNAL_CSV` in both backtest and live monitor modes.

## Licensing

True real-time CME requires licensed market-data access. The code is a connector; it does not include credentials or entitlements.
