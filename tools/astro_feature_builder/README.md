# Astro Feature Builder

Python-side deterministic generator for candle-aligned astrological feature stores.

Primary runtime architecture:

```text
Python builds the sky map per candle.
MQL5 reads the CSV mirror per candle.
Excel/XLSX is for review, not runtime.
```

The builder uses `pyswisseph` / Swiss Ephemeris. It does not call APIs and does not require internet during generation once dependencies and ephemeris files are available.

## Install

```powershell
python -m pip install -r tools/astro_feature_builder/requirements.txt
```

## Generate CSV + Excel

```powershell
python tools/astro_feature_builder/astro_feature_builder.py `
  --start-broker "2024-01-01 00:00:00" `
  --end-broker "2024-02-01 00:00:00" `
  --timeframe-minutes 1 `
  --broker-gmt-offset-hours 2 `
  --ephe-path "tools/astro_feature_builder/ephe" `
  --out-csv "data/astro/astro_XAUUSD_M1_202401_mql.csv" `
  --out-xlsx "data/astro/astro_XAUUSD_M1_202401_review.xlsx"
```

## Time contract

```text
utc_time = broker_time - broker_gmt_offset_hours
```

Every row is computed at candle open time. This keeps the data causal for Strategy Tester and live execution.

## MQL5 runtime

Copy the CSV file into:

```text
<Terminal Data Folder>/MQL5/Files/astro/
```

Then load it from MQL5 with:

```mql5
#include <Research/DAL_AstroExcelCandleReader.mqh>

DAL_AstroMapStore store;
DAL_AstroMapStore_LoadExcelCsv(store, "astro\\astro_XAUUSD_M1_202401_mql.csv", 2.0, 1);
```

## Excel limit

`.xlsx` is limited to 1,048,576 rows per worksheet. For large M1 datasets, generate yearly/monthly chunks or use CSV only.
