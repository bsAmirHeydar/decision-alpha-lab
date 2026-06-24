# EXP0013 — Astro Feature Store

## Purpose

EXP0013 creates a professional bridge between Python-generated astrological ephemeris data and MQL5 execution/research modules.

The experiment lets every candle in visual tester, Strategy Tester, or live execution access the full sky-state feature row for that candle.

## Components

```text
tools/astro_feature_builder/astro_feature_builder.py
mql5/Include/Research/DAL_AstroFeatureTypes.mqh
mql5/Include/Research/DAL_AstroFeatureStore.mqh
mql5/Include/Research/DAL_AstroDistributionAdapter.mqh
mql5/Experts/Research/EXP0013_AstroFeatureStore_Demo.mq5
```

## Generate CSV

```powershell
python -m pip install -r tools/astro_feature_builder/requirements.txt

python tools/astro_feature_builder/astro_feature_builder.py `
  --start-broker "2024-01-01 00:00:00" `
  --end-broker "2024-02-01 00:00:00" `
  --timeframe-minutes 1 `
  --broker-gmt-offset-hours 2 `
  --ephe-path "tools/astro_feature_builder/ephe" `
  --out "astro_XAUUSD_M1_202401.csv"
```

Copy output into:

```text
<META_TRADER_DATA_FOLDER>/MQL5/Files/astro/astro_XAUUSD_M1_202401.csv
```

Set:

```text
InpAstroCsvFile = astro/astro_XAUUSD_M1_202401.csv
InpBrokerGmtOffsetHours = 2
```

## MQL5 Runtime

The demo expert loads the CSV and matches rows by broker bar time:

```mql5
DAL_AstroFeatureStore_FindByBrokerTime(store, iTime(_Symbol, PERIOD_M1, 0), row, true);
```

It then displays the state on the visual tester chart and creates a distribution key:

```mql5
string dist_key = DAL_Astro_AppendToDistributionKey(execution_key, row, true);
```

## Execution Integration

In any execution:

```mql5
#include <Research/DAL_AstroFeatureStore.mqh>
#include <Research/DAL_AstroDistributionAdapter.mqh>

DAL_AstroFeatureStore g_astro;

int OnInit()
{
   DAL_AstroFeatureStore_LoadCsv(g_astro, InpAstroCsvFile, InpBrokerGmtOffsetHours);
   return INIT_SUCCEEDED;
}
```

On each new bar:

```mql5
DAL_AstroFeatureRow astro;
if(DAL_AstroFeatureStore_FindByBrokerTime(g_astro, bar_time, astro, true))
{
   feature_key = DAL_Astro_AppendToDistributionKey(feature_key, astro, true);
}
```

Then pass `feature_key` to EXP0012 Distribution Engineering when recording the outcome.

## Notes

The Python builder is intentionally outside Strategy Tester. Strategy Tester must read deterministic files, not call Python or APIs during backtest.
