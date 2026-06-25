# EXP0013 Astro Live Bridge V2

This bridge generates a small rolling astro CSV for the live MT5 dashboard.

## Runtime contract

Python writes:

- `broker_time`: already aligned to the broker chart time
- `utc_time`: true UTC used for astronomical calculations

MQL5 reads `broker_time` directly. There is no second GMT shift inside MQL.

## One-shot test

```powershell
python tools\astro_live_bridge\astro_live_bridge.py `
  --common-files "C:\Users\ABN\AppData\Roaming\MetaQuotes\Terminal\Common\Files" `
  --output-name "astro_live_mql.csv" `
  --broker-gmt-offset-hours 3 `
  --timeframe-minutes 1 `
  --history-hours 48 `
  --future-hours 6 `
  --once
```

## Continuous live mode

```powershell
python tools\astro_live_bridge\astro_live_bridge.py `
  --common-files "C:\Users\ABN\AppData\Roaming\MetaQuotes\Terminal\Common\Files" `
  --output-name "astro_live_mql.csv" `
  --broker-gmt-offset-hours 3 `
  --timeframe-minutes 1 `
  --history-hours 48 `
  --future-hours 6 `
  --refresh-seconds 60
```

## MT5 EA inputs

```text
InpAstroCsvFile          = astro_live_mql.csv
InpBrokerGmtOffsetHours  = 0
InpReloadCsvEverySeconds = 10
InpRequireExactBarTime   = true
InpViewMode              = ASTRO_VIEW_COCKPIT
```

## Output files

Written atomically into Common Files:

```text
astro_live_mql.csv
astro_live_status.json
```

The status JSON is for human/live diagnostics and includes:

- last update UTC
- output CSV path
- broker start/end window
- rows hint
- error text if generation failed

## Optional house cusps

The live bridge can pass house-location inputs to the builder:

```powershell
python tools\astro_live_bridge\astro_live_bridge.py `
  --common-files "C:\Users\ABN\AppData\Roaming\MetaQuotes\Terminal\Common\Files" `
  --output-name "astro_live_mql.csv" `
  --broker-gmt-offset-hours 3 `
  --timeframe-minutes 1 `
  --history-hours 48 `
  --future-hours 6 `
  --refresh-seconds 60 `
  --house-lat 40.7128 `
  --house-lon -74.0060 `
  --house-system P
```

If `--house-lat` and `--house-lon` are omitted, the CSV remains geocentric-only and the MQL dashboard will show houses as unavailable.

## Optional natal or inception chart

The live bridge can also build a rolling CSV that embeds a fixed natal or inception chart:

```powershell
python tools\astro_live_bridge\astro_live_bridge.py `
  --common-files "C:\Users\ABN\AppData\Roaming\MetaQuotes\Terminal\Common\Files" `
  --output-name "astro_live_mql.csv" `
  --broker-gmt-offset-hours 3 `
  --timeframe-minutes 1 `
  --history-hours 48 `
  --future-hours 6 `
  --refresh-seconds 60 `
  --natal-local-datetime "1987-08-16 14:35:00" `
  --natal-utc-offset-hours 3.5 `
  --natal-lat 35.6892 `
  --natal-lon 51.3890 `
  --natal-label "gold_ref"
```

When natal inputs are present, the rolling CSV contains:

- natal body state
- natal houses and angles
- transit-to-natal activations
- pure astro language fields
