# EXP0015 Intermarket Candle + Session Divergence

This experiment detects two-symbol divergence with both candle-based and
session-based reference levels.

## Current level families

- `previous_candle`
- `rolling`
- `current_session`
- `previous_session`

## Trigger modes

- `wick_touch`
- `close_break`
- `hunt_reject_close`

## Backtest from normalized CSV

Required CSV schema:

```csv
time,open,high,low,close,volume
2026-06-25 13:30:00,6120.25,6122.00,6118.75,6121.50,15230
```

Run:

```bash
python lab/03_experiments/EXP0015_intermarket_time_divergence/experiment.py \
  --a data/cme/bars/ES_M1.csv \
  --b data/cme/bars/NQ_M1.csv \
  --symbol-a ES \
  --symbol-b NQ \
  --level-family current_session \
  --destination-lag-bars 2 \
  --signal-valid-bars 12
```

Outputs:

```text
out/imd001_divergence_events.csv
out/imd001_summary.csv
out/imd001_summary.json
```

## Live bridge path

The live path is intentionally decoupled:

```text
CME/vendor/legal data feed -> tools/cme_bridge -> Common/Files/dal/cme/*.csv -> MQL5 IMD001 live monitor
```

The MQL5 expert can read the same normalized CSV files repeatedly in timer mode.
This keeps raw data-feed authentication and WebSocket/reconnect logic outside MQL5.
