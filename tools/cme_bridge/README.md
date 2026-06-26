# DAL CME-compatible data bridge

This bridge is the external data layer for EXP0015 intermarket divergence.

It does not bypass CME entitlements. It assumes you have legal access to CME or
CME-sourced data, then normalizes it into the DAL candle schema.

## Candle schema

MQL5 reader expects CSV files in MetaTrader Common Files with this header:

```csv
time,open,high,low,close,volume
2026-06-25 13:30:00,6120.25,6122.00,6118.75,6121.50,15230
```

## Backtest mode

Place historical candles here:

```text
data/cme/bars/ES_M1.csv
data/cme/bars/NQ_M1.csv
```

Then run the Python experiment or copy the files into MT5 Common Files:

```text
Common/Files/dal/cme/ES_M1.csv
Common/Files/dal/cme/NQ_M1.csv
```

## Live CSV tail mode

If a vendor/CME process keeps updating `data/cme/bars/ES_M1.csv` and `NQ_M1.csv`,
run:

```bash
python tools/cme_bridge/dal_cme_bridge.py --config tools/cme_bridge/dal_cme_config.example.json --mode live_csv_tail
```

The bridge rewrites strict MQL-readable files into:

```text
Common/Files/dal/cme/ES_M1.csv
Common/Files/dal/cme/NQ_M1.csv
```

Then run `IMD001_CandleSessionDivergence.mq5` with:

```text
InpRunMode = IMD_RUN_LIVE_MONITOR
InpDataSource = IMD_DS_EXTERNAL_CSV
```

## HTTP serve mode

For Python dashboards or external tools:

```bash
python tools/cme_bridge/dal_cme_bridge.py --mode serve
```

Endpoints:

```text
GET /health
GET /bars?symbol=ES&limit=500
```

## Direct CME adapter boundary

Direct CME historical/realtime adapters should feed this bridge's candle schema.
Keep official/vendor authentication, entitlement checks, reconnect logic, and raw
message parsing outside MQL5. MQL5 should consume normalized candles only.
