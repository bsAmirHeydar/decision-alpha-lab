# EXP0015 CME/live/backtest implementation plan

The project now separates the divergence engine from data acquisition.

## Stage 1: source-agnostic divergence engine

Implemented in this patch:

- MQL5 candle/session divergence engine.
- Python backtest runner.
- Broker data source mode.
- External CSV data source mode.
- Session reference levels.
- Candle reference levels.
- Step/lag/valid-window logic.
- Basic MFE/MAE/return outcome columns.

## Stage 2: live data bridge

Implemented as a stable bridge boundary:

- `tools/cme_bridge/dal_cme_bridge.py`
- `serve` mode for localhost HTTP bars.
- `live_csv_tail` mode for MT5 Common Files.

The bridge accepts legally obtained CME or CME-sourced data and normalizes it into
DAL candle CSVs. Direct CME/vendor adapters should be added inside this bridge,
not inside MQL5.

## Stage 3: direct CME/vendor adapter

To activate direct CME/vendor live data, provide the credentialed feed details and
schema, then implement an adapter that outputs:

```csv
time,open,high,low,close,volume
```

Expected raw inputs can be:

- historical bar exports,
- historical tick/trade exports converted by `dal_candle_builder.py`,
- live trade/top-of-book stream converted into rolling M1 bars.

## Stage 4: live MQL5 monitor

Run `IMD001_CandleSessionDivergence.mq5` with:

```text
InpRunMode = IMD_RUN_LIVE_MONITOR
InpDataSource = IMD_DS_EXTERNAL_CSV
InpCsvACommon = dal/cme/ES_M1.csv
InpCsvBCommon = dal/cme/NQ_M1.csv
```

MQL5 will re-read the bridge-updated CSV files on a timer and emit fresh event and
summary CSVs.

## Stage 5: next upgrades

- matched random baseline,
- richer session profiles,
- CME contract roll maps,
- custom symbol importer,
- dashboard labels/alerts,
- ICT confirmation layer.
