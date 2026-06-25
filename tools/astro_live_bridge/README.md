# EXP0013 Astro Live Bridge

This folder contains the live architecture for seeing the current astrological state inside MetaTrader without relying on custom indicators.

## Recommended live design

```text
Python / Swiss Ephemeris
        ↓ writes rolling CSV atomically
MetaQuotes Common\Files\astro_live_mql.csv
        ↓ MQL5 EA reloads periodically
EXP0013_AstroUnifiedDashboardEA
        ↓ renders
Text panel + oscillator object dashboard
```

## Why this design

MQL5 should not calculate ephemeris directly.  
MQL5 should also not depend on custom indicator loading inside Strategy Tester.

The robust split is:

```text
Python = astronomical computation
MQL5   = visualization + market alignment + research logging
```

## Run example

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

Then in MetaTrader attach:

```text
Experts\Research\EXP0013_AstroUnifiedDashboardEA
```

Inputs:

```text
InpAstroCsvFile = astro_live_mql.csv
InpBrokerGmtOffsetHours = 0
InpReloadCsvEverySeconds = 10
InpRequireExactBarTime = true
```

## Time contract

The Python-generated CSV already contains broker_time.  
MQL5 matches chart candle open time directly against CSV broker_time.  
There is no second GMT shift in MQL lookup.
