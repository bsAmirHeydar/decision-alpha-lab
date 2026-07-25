# DAL CME Bridge for EXP0015

This directory contains the data bridge used by **Decision Alpha Lab / EXP0015 Intermarket Divergence**.

The goal is to give the MQL5 divergence engine clean ES/NQ-style futures bars for both:

1. **Backtesting / offline research** from historical CME-sourced data.
2. **Live monitoring** from a licensed real-time feed or a near-live historical polling workflow.

The MQL5 expert stays source-agnostic. It only reads canonical CSV bars from MetaTrader Common Files. The bridge is responsible for obtaining, normalizing, storing, and copying those bars.

---

## Important licensing boundary

This project does **not** bypass CME or vendor licensing.

For true CME real-time data you need a legal market-data account, credentials, and the required exchange entitlements. The provided Databento provider expects `DATABENTO_API_KEY` and valid CME/Globex permissions. The Yahoo fallback is delayed and is included only for development sanity checks.

Use this bridge only with data you are legally allowed to access and store.

---

## Architecture

```text
Licensed CME/vendor feed
        ↓
adapters/legacy/market_data/cme_bridge providers
        ↓
Canonical DAL CSV bars
        ↓
MetaTrader Common Files copier
        ↓
MQL5 EXP0015 IMD001_CandleSessionDivergence
```

Canonical CSV schema:

```csv
time,open,high,low,close,volume
2026-06-25 13:30:00,6120.25,6122.00,6118.75,6121.50,15230
```

Time is stored in UTC by default. The current files are designed for `M1` bars:

```text
data/cme/bars/ES_M1.csv
data/cme/bars/NQ_M1.csv
```

The MQL5 expert can read these files after they are copied to Common Files:

```text
Common/Files/dal/cme/ES_M1.csv
Common/Files/dal/cme/NQ_M1.csv
```

---

## Files

```text
adapters/legacy/market_data/cme_bridge/
  README.md
  requirements.txt
  dal_bar_store.py
  dal_candle_builder.py
  dal_cme_bridge.py
  dal_cme_live_prices.py
  dal_cme_historical_poller.py
  dal_cme_config.example.json
  configs/
    databento_es_nq.example.json
    yahoo_delayed_es_nq.example.json
  providers/
    databento_provider.py
    yahoo_delayed_provider.py
```

### Main entrypoints

```text
dal_cme_live_prices.py
  One-command launcher for providers.

providers/databento_provider.py
  Databento historical and live provider.

dal_cme_historical_poller.py
  Repeated incremental historical polling, default every 5 minutes.

dal_cme_bridge.py
  Copies / tails local bridge CSVs into MetaTrader Common Files.
```

---

## Install

From the project root:

```powershell
pip install -r .\adapters\legacy\market_data\cme_bridge\requirements.txt
```

Or on Linux/macOS:

```bash
pip install -r adapters/legacy/market_data/cme_bridge/requirements.txt
```

Requirements:

```text
databento
pandas
yfinance
```

---

## Set your Databento API key

PowerShell:

```powershell
setx DATABENTO_API_KEY "db-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

For the current terminal only:

```powershell
$env:DATABENTO_API_KEY="db-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

Linux/macOS:

```bash
export DATABENTO_API_KEY="db-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

Do not commit your API key to Git.

---

## Databento config

Default config:

```text
adapters/legacy/market_data/cme_bridge/configs/databento_es_nq.example.json
```

Example:

```json
{
  "dataset": "GLBX.MDP3",
  "schema": "ohlcv-1m",
  "stype_in": "continuous",
  "output_dir": "data/cme/bars",
  "max_rows": 5000,
  "poll_status_seconds": 10,
  "historical_poll_seconds": 300,
  "historical_overlap_minutes": 10,
  "historical_bootstrap_minutes": 180,
  "historical_end_delay_seconds": 90,
  "symbols": {
    "ES": "ES.c.0",
    "NQ": "NQ.c.0"
  }
}
```

Meaning:

```text
dataset
  Databento dataset. GLBX.MDP3 is CME Globex MDP 3.0.

schema
  Bar schema. ohlcv-1m writes one-minute OHLCV bars.

stype_in
  Symbol type. continuous lets ES.c.0 and NQ.c.0 follow front contracts.

output_dir
  Local bridge output directory.

max_rows
  Maximum rows kept in live/polling files. 0 means keep all rows for full historical downloads.

historical_poll_seconds
  Default historical polling interval. 300 seconds = 5 minutes.

historical_overlap_minutes
  How far back each incremental poll overlaps the previous request.
  This allows the script to replace late/revised/incomplete bars safely.

historical_bootstrap_minutes
  Initial lookback if the output CSV does not exist.

historical_end_delay_seconds
  Delay from current UTC time to avoid requesting the still-forming current bar.
```

---

# Workflow A — Offline historical backtest

Use this when you want to download a fixed historical range and run research.

## 1. Download historical ES/NQ bars

PowerShell:

```powershell
$env:DATABENTO_API_KEY="db-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

python .\adapters\legacy\market_data\cme_bridge\dal_cme_live_prices.py databento_historical `
  --start 2026-01-01 `
  --end 2026-06-26
```

Linux/macOS:

```bash
export DATABENTO_API_KEY="db-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

python adapters/legacy/market_data/cme_bridge/dal_cme_live_prices.py databento_historical \
  --start 2026-01-01 \
  --end 2026-06-26
```

Output:

```text
data/cme/bars/ES_M1.csv
data/cme/bars/NQ_M1.csv
```

## 2. Run the Python EXP0015 experiment

PowerShell:

```powershell
python .\contexts\legacy\lab_experiments\EXP0015_intermarket_time_divergence\experiment.py `
  --a data/cme/bars/ES_M1.csv `
  --b data/cme/bars/NQ_M1.csv `
  --symbol-a ES `
  --symbol-b NQ `
  --level-family current_session `
  --destination-lag-bars 2 `
  --signal-valid-bars 12
```

Linux/macOS:

```bash
python contexts/legacy/lab_experiments/EXP0015_intermarket_time_divergence/experiment.py \
  --a data/cme/bars/ES_M1.csv \
  --b data/cme/bars/NQ_M1.csv \
  --symbol-a ES \
  --symbol-b NQ \
  --level-family current_session \
  --destination-lag-bars 2 \
  --signal-valid-bars 12
```

Experiment output:

```text
contexts/legacy/lab_experiments/EXP0015_intermarket_time_divergence/out/imd001_divergence_events.csv
contexts/legacy/lab_experiments/EXP0015_intermarket_time_divergence/out/imd001_summary.csv
contexts/legacy/lab_experiments/EXP0015_intermarket_time_divergence/out/imd001_summary.json
```

---

# Workflow B — Backtest inside MetaTrader 5 using external CSV

## 1. Download historical bars

Use Workflow A step 1.

## 2. Copy bridge CSVs into MetaTrader Common Files

Run:

```powershell
python .\adapters\legacy\market_data\cme_bridge\dal_cme_bridge.py `
  --config .\adapters\legacy\market_data\cme_bridge\dal_cme_config.example.json `
  --mode copy_once
```

If your bridge config points to the correct Common Files path, this creates:

```text
Common/Files/dal/cme/ES_M1.csv
Common/Files/dal/cme/NQ_M1.csv
```

## 3. Compile the MQL5 expert

```text
mql5/Experts/IntermarketDivergence/IMD001_CandleSessionDivergence.mq5
```

## 4. Use these MQL5 inputs

```text
InpRunMode       = IMD_RUN_BACKTEST_BATCH
InpDataSource    = IMD_DS_EXTERNAL_CSV
InpSymbolA       = ES
InpSymbolB       = NQ
InpCsvACommon    = dal/cme/ES_M1.csv
InpCsvBCommon    = dal/cme/NQ_M1.csv
InpLevelFamily   = IMD_LEVEL_CURRENT_SESSION
InpTriggerMode   = IMD_TRIGGER_WICK_TOUCH
```

MQL5 output:

```text
Common/Files/imd/EXP0015/imd001_divergence_events.csv
Common/Files/imd/EXP0015/imd001_summary.csv
```

---

# Workflow C — True live Databento stream

Use this when you have live CME/Globex entitlement and want a real live stream.

## 1. Terminal 1: start live Databento stream

```powershell
$env:DATABENTO_API_KEY="db-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

python .\adapters\legacy\market_data\cme_bridge\dal_cme_live_prices.py databento_live
```

Output files:

```text
data/cme/bars/ES_M1.csv
data/cme/bars/NQ_M1.csv
```

## 2. Terminal 2: tail files into MetaTrader Common Files

```powershell
python .\adapters\legacy\market_data\cme_bridge\dal_cme_bridge.py `
  --config .\adapters\legacy\market_data\cme_bridge\dal_cme_config.example.json `
  --mode live_csv_tail
```

## 3. MT5 inputs

```text
InpRunMode          = IMD_RUN_LIVE_MONITOR
InpDataSource       = IMD_DS_EXTERNAL_CSV
InpSymbolA          = ES
InpSymbolB          = NQ
InpCsvACommon       = dal/cme/ES_M1.csv
InpCsvBCommon       = dal/cme/NQ_M1.csv
InpLiveTimerSeconds = 10
```

The expert reloads the CSVs periodically and updates divergence state.

---

# Workflow D — Near-live historical polling every 5 minutes

This is the new polling workflow.

It repeatedly requests a small recent historical range, merges the returned bars into the local CSV files, and keeps MT5 fed through the same `live_csv_tail` copier.

This is useful when:

```text
- you do not want to keep a live WebSocket open;
- you only need closed M1 bars;
- a few minutes of delay is acceptable;
- your provider account permits frequent historical requests.
```

It is **not** tick-real-time. It is near-live, bar-close-based polling.

## Is polling historical data every 5 minutes safe?

Technically, yes, if done incrementally:

```text
Good:
  every 5 minutes request only the latest small window;
  overlap by 5-10 minutes;
  deduplicate by timestamp;
  write atomically;
  delay the end time so the current forming bar is not used.

Bad:
  every 5 minutes download months or years again;
  no overlap/dedupe;
  no rate/cost control;
  use it as if it were tick-real-time.
```

This poller uses the safe version.

## 1. Run one incremental poll

```powershell
$env:DATABENTO_API_KEY="db-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

python .\adapters\legacy\market_data\cme_bridge\dal_cme_live_prices.py databento_historical_poll `
  --once `
  --interval-seconds 300 `
  --overlap-minutes 10 `
  --bootstrap-minutes 180 `
  --end-delay-seconds 90
```

## 2. Run continuous polling every 5 minutes

```powershell
$env:DATABENTO_API_KEY="db-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

python .\adapters\legacy\market_data\cme_bridge\dal_cme_live_prices.py databento_historical_poll `
  --interval-seconds 300 `
  --overlap-minutes 10 `
  --bootstrap-minutes 180 `
  --end-delay-seconds 90
```

Equivalent direct command:

```powershell
python .\adapters\legacy\market_data\cme_bridge\dal_cme_historical_poller.py `
  --config .\adapters\legacy\market_data\cme_bridge\configs\databento_es_nq.example.json `
  --interval-seconds 300 `
  --overlap-minutes 10 `
  --bootstrap-minutes 180 `
  --end-delay-seconds 90
```

## 3. Terminal 2: copy/tail into MetaTrader Common Files

```powershell
python .\adapters\legacy\market_data\cme_bridge\dal_cme_bridge.py `
  --config .\adapters\legacy\market_data\cme_bridge\dal_cme_config.example.json `
  --mode live_csv_tail
```

## 4. MT5 live monitor inputs

```text
InpRunMode          = IMD_RUN_LIVE_MONITOR
InpDataSource       = IMD_DS_EXTERNAL_CSV
InpSymbolA          = ES
InpSymbolB          = NQ
InpCsvACommon       = dal/cme/ES_M1.csv
InpCsvBCommon       = dal/cme/NQ_M1.csv
InpLiveTimerSeconds = 10
```

## How the poller avoids data problems

```text
- Reads the latest timestamp already stored in ES_M1.csv and NQ_M1.csv.
- Starts the next request from latest_time - overlap_minutes.
- Requests only up to now - end_delay_seconds.
- Merges by timestamp.
- Replaces duplicate/overlap rows.
- Sorts rows by time.
- Atomically rewrites the CSV so MT5 does not read a half-written file.
- Keeps only max_rows rows if max_rows > 0.
```

Recommended defaults:

```text
interval_seconds       = 300   # five minutes
overlap_minutes        = 10    # enough to replace recent late bars
bootstrap_minutes      = 180   # first run fetches last three hours
end_delay_seconds      = 90    # avoid incomplete most-recent M1 bar
```

For less delay, try:

```text
end_delay_seconds = 30
```

For more safety around provider bar finalization, use:

```text
end_delay_seconds = 120
```

---

# Workflow E — Delayed fallback without CME credentials

This is not real-time CME. It is only for development without API credentials.

```powershell
python .\adapters\legacy\market_data\cme_bridge\dal_cme_live_prices.py yahoo_delayed
```

Then run the Common Files copier in Terminal 2:

```powershell
python .\adapters\legacy\market_data\cme_bridge\dal_cme_bridge.py `
  --config .\adapters\legacy\market_data\cme_bridge\dal_cme_config.example.json `
  --mode live_csv_tail
```

Use the same MQL5 live monitor inputs.

---

# Common troubleshooting

## `ModuleNotFoundError: No module named databento`

Run:

```powershell
pip install -r .\adapters\legacy\market_data\cme_bridge\requirements.txt
```

## `DATABENTO_API_KEY` missing or invalid

Set:

```powershell
$env:DATABENTO_API_KEY="db-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

Or permanently:

```powershell
setx DATABENTO_API_KEY "db-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

Open a new terminal after `setx`.

## CSV files are not appearing in MT5

Check that the Common Files copy/tail bridge is running:

```powershell
python .\adapters\legacy\market_data\cme_bridge\dal_cme_bridge.py `
  --config .\adapters\legacy\market_data\cme_bridge\dal_cme_config.example.json `
  --mode live_csv_tail
```

Check the destination configured inside:

```text
adapters/legacy/market_data/cme_bridge/dal_cme_config.example.json
```

## MT5 expert sees stale data

Increase `InpLiveTimerSeconds` frequency or verify that:

```text
Common/Files/dal/cme/ES_M1.csv
Common/Files/dal/cme/NQ_M1.csv
```

are changing.

## Historical polling looks delayed

This is expected. The poller intentionally uses `--end-delay-seconds` to avoid incomplete current bars. Reduce it if you accept more risk of partial bars.

## Historical polling costs too much

Increase interval and reduce bootstrap:

```powershell
python .\adapters\legacy\market_data\cme_bridge\dal_cme_live_prices.py databento_historical_poll `
  --interval-seconds 900 `
  --bootstrap-minutes 60 `
  --overlap-minutes 5
```

Also monitor provider usage in your vendor portal.

---

# Recommended modes

```text
Research / long backtest:
  databento_historical

Live-quality monitoring:
  databento_live

Near-live closed-bar monitoring with simple operational setup:
  databento_historical_poll every 300 seconds

No credentials / sanity check:
  yahoo_delayed
```

---

# Safety rule

Use `databento_live` for real-time trading-quality monitoring.
Use `databento_historical_poll` when closed-bar delay is acceptable and you want a simpler, restart-friendly workflow.
