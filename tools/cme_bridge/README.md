# DAL CME Bridge

This bridge gives EXP0015 a live/backtest data boundary for CME futures bars.

It does **not** bypass CME/vendor licensing. For true real-time CME you need a licensed feed and credentials. The bridge supports two practical paths:

1. **Databento real CME/Globex data**: live and historical, requires `DATABENTO_API_KEY` and exchange entitlements.
2. **Yahoo delayed fallback**: delayed ES/NQ futures quotes for quick sanity checks only, not trading.

## Install

```bash
pip install -r tools/cme_bridge/requirements.txt
```

## Real CME/Globex live via Databento

Set your API key:

```bash
set DATABENTO_API_KEY=db-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Start live ES/NQ 1-minute bars:

```bash
python tools/cme_bridge/dal_cme_live_prices.py databento_live
```

Output:

```text
data/cme/bars/ES_M1.csv
data/cme/bars/NQ_M1.csv
```

To copy those bars into MetaTrader Common Files for the MQL5 expert, run a second terminal:

```bash
python tools/cme_bridge/dal_cme_bridge.py --config tools/cme_bridge/dal_cme_config.example.json --mode live_csv_tail
```

Then in MT5 use:

```text
InpRunMode    = IMD_RUN_LIVE_MONITOR
InpDataSource = IMD_DS_EXTERNAL_CSV
InpCsvACommon = dal/cme/ES_M1.csv
InpCsvBCommon = dal/cme/NQ_M1.csv
```

## Historical backtest via Databento

```bash
python tools/cme_bridge/dal_cme_live_prices.py databento_historical --start 2026-01-01 --end 2026-06-26
```

Then either run the MQL5 expert with `EXTERNAL_CSV`, or run the Python experiment:

```bash
python lab/03_experiments/EXP0015_intermarket_time_divergence/experiment.py --a data/cme/bars/ES_M1.csv --b data/cme/bars/NQ_M1.csv --symbol-a ES --symbol-b NQ --level-family current_session
```

## Delayed fallback without CME credentials

This uses Yahoo Finance symbols `ES=F` and `NQ=F`. Yahoo labels these as CME delayed quotes. This is useful only for development and sanity checks.

```bash
python tools/cme_bridge/dal_cme_live_prices.py yahoo_delayed
```

Then run `live_csv_tail` in a second terminal as above.

## Config

Databento default config:

```text
tools/cme_bridge/configs/databento_es_nq.example.json
```

Yahoo delayed fallback config:

```text
tools/cme_bridge/configs/yahoo_delayed_es_nq.example.json
```

Both produce the same canonical CSV schema:

```csv
time,open,high,low,close,volume
2026-06-25 13:30:00,6120.25,6122.00,6118.75,6121.50,15230
```
