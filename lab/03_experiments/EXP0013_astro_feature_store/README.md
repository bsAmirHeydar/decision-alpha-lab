# EXP0013 - Astro Feature Store

## Purpose

EXP0013 is the deterministic astronomy-to-MQL pipeline inside Decision Alpha Lab.

It now supports both:

- transit-only raw sky state
- natal or inception chart activation models

The goal is to make every candle in tester or live execution able to read a full astro state row without calling Python or external APIs at runtime.

## Main architecture

```text
Python builder
-> deterministic CSV
-> MQL astro map reader
-> raw dashboard / diagnostics
-> pure astro language
-> astro-only execution families
```

## Current modules

```text
tools/astro_feature_builder/astro_feature_builder.py
tools/astro_live_bridge/astro_live_bridge.py
mql5/Include/Research/DAL_AstroMapTypes.mqh
mql5/Include/Research/DAL_AstroExcelCandleReader.mqh
mql5/Include/Research/DAL_AstroDerivedFeatures.mqh
mql5/Include/Research/DAL_AstroPathCleanlinessMetrics.mqh
mql5/Include/Research/DAL_AstroFractalPathMetrics.mqh
mql5/Include/Research/DAL_AstroPureAstrologySignals.mqh
mql5/Experts/Research/EXP0013_AstroUnifiedDashboardEA.mq5
mql5/Experts/AstroExecution/
```

## Data families now supported

- transit raw bodies
- transit houses and angles
- transit-to-transit aspects
- transit declination speed and out-of-bounds state
- transit-to-transit parallels and contra-parallels
- natal raw bodies
- natal houses and angles
- transit-to-natal aspects for Sun..Saturn
- transit-to-natal parallels and contra-parallels for Sun..Saturn
- transit placement inside natal houses
- pure astro language fields
- doctrine and schema metadata embedded into every row

## Build a transit + natal CSV

```powershell
python -m pip install -r tools/astro_feature_builder/requirements.txt

python tools/astro_feature_builder/astro_feature_builder.py `
  --start-broker "2024-01-01 00:00:00" `
  --end-broker "2024-02-01 00:00:00" `
  --timeframe-minutes 1 `
  --broker-gmt-offset-hours 2 `
  --house-lat 35.6892 `
  --house-lon 51.3890 `
  --natal-local-datetime "1987-08-16 14:35:00" `
  --natal-utc-offset-hours 3.5 `
  --natal-lat 35.6892 `
  --natal-lon 51.3890 `
  --natal-label "gold_ref" `
  --doctrine-id "astro_only_doctrine_v1" `
  --schema-version "astro_feature_schema_v2" `
  --ephe-path "tools/astro_feature_builder/ephe" `
  --out-csv "data/astro/astro_XAUUSD_M1_202401_mql.csv"
```

## Runtime contract

- Python computes astro rows at candle open time.
- CSV stores both `broker_time` and `utc_time`.
- MQL looks up by `broker_time` exactly.
- MQL does not apply a second GMT shift.

## Dashboard

`EXP0013_AstroUnifiedDashboardEA.mq5` now exposes:

- `OVERVIEW`
- `BODIES`
- `ASPECTS`
- `HOUSES`
- `METRICS`
- `NATAL`
- `SIGNALS`
- `TIMING`

The dashboard can display:

- raw transit state
- natal chart metadata
- transit-to-natal activations
- pure astro signal language
- hierarchical timing doctrine from macro background to minute trigger

## Astro-only execution

The `mql5/Experts/AstroExecution` folder contains pure-astro execution families.

- `A0001` transit trend pulse
- `A0002` natal resonance
- `A0003` friction polarity
- `A0090` live order shell

The paper families now share:

- deterministic state transitions: `wait -> armed -> enter -> hold -> reduce -> exit`
- per-family journal CSVs
- doctrine and schema traceability in the journal
- offline validation through `tools/astro_validation/astro_signal_validator.py`

The signal layer is now explicitly hierarchical:

- macro field
- meso gate
- micro trigger
- minute window
- entry / exit language

These families read only the astro CSV and the pure astro signal layer. They do not use market structure or indicators.

## Research discipline

Read these next:

- `ASTRO_FEATURE_MEANING.md`
- `ASTRO_ONLY_EXECUTION_CONTRACT.md`
- `ASTRO_ONLY_EXECUTION_ROADMAP.md`
- `ASTRO_PURE_SIGNAL_ALGORITHMS.md`
- `ASTRO_TIMING_DOCTRINE.md`
- `ASTRO_RAW_SKY_TABBED_UI_AND_NATAL_DOCTRINE.md`

## Important note

The EA birth inputs are not a substitute for CSV generation.

If the natal anchor changes, regenerate the CSV with the same natal inputs. The dashboard can display and validate the anchor, but the astronomical row itself is still produced by Python.
