# Run Astro Path Cleanliness Screen

## 1. Build the CSV/XLSX first

Use the command guide here:

```text
docs/evidence/exp0013_astro_excel_csv_build_commands/6e29545f8168_BUILD_EXCEL_COMMANDS.md
```

Example:

```powershell
python -m pip install -r tools/astro_feature_builder/requirements.txt

python tools/astro_feature_builder/astro_feature_builder.py `
  --start-broker "2024-01-01 00:00:00" `
  --end-broker "2024-02-01 00:00:00" `
  --timeframe-minutes 1 `
  --broker-gmt-offset-hours 2 `
  --ephe-path "tools/astro_feature_builder/ephe" `
  --out-csv "data/astro/astro_XAUUSD_M1_202401_mql.csv" `
  --out-xlsx "data/astro/astro_XAUUSD_M1_202401_review.xlsx"
```

## 2. Copy the runtime CSV into MetaTrader

Copy the CSV to:

```text
<MetaTrader Data Folder>/MQL5/Files/astro/astro_XAUUSD_M1_202401_mql.csv
```

In MetaTrader:

```text
File → Open Data Folder → MQL5 → Files → astro
```

Create the `astro` folder if it does not exist.

## 3. Compile the screen-only demo

Compile:

```text
mql5/Experts/Research/EXP0013_AstroPathCleanlinessMetrics_Demo.mq5
```

## 4. Run in Visual Tester

Recommended inputs:

```text
InpAstroCsvFile             = astro\astro_XAUUSD_M1_202401_mql.csv
InpBrokerGmtOffsetHours     = 2.0
InpReadTimeframe            = PERIOD_M1
InpRequireExactBarTime      = true
InpReadOnlyOnNewBar         = true
InpValidateUtcOffset        = true
InpShowRawBodies            = true
InpShowFeatureKeys          = true
InpUseObjectPanel           = true
InpUseTerminalComment       = true
InpPrintMetricsOnNewBar     = true
```

## 5. What to watch visually

Look at the market path while the panel changes candle by candle.

Questions:

```text
Does CleanPath rise before cleaner movements?
Does PullbackRisk rise before deeper pullbacks?
Does ChopRisk rise before fake moves or ranges?
Does clean_impulse appear before direct breakouts?
Does clean_flow appear during smoother continuation?
```

Do not trade from this screen. It is an observation layer only.
