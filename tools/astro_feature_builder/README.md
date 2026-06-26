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
  --house-lat 35.6892 `
  --house-lon 51.3890 `
  --natal-local-datetime "1987-08-16 14:35:00" `
  --natal-utc-offset-hours 3.5 `
  --natal-lat 35.6892 `
  --natal-lon 51.3890 `
  --natal-label "gold_ref" `
  --ephe-path "tools/astro_feature_builder/ephe" `
  --out-csv "data/astro/astro_XAUUSD_M1_202401_mql.csv" `
  --out-xlsx "data/astro/astro_XAUUSD_M1_202401_review.xlsx"
```

## Time contract

```text
utc_time = broker_time - broker_gmt_offset_hours
```

Every row is computed at candle open time. This keeps the data causal for Strategy Tester and live execution.

## Natal / inception support

The builder can optionally embed a fixed natal or inception chart into every row:

```text
--natal-local-datetime
--natal-utc-offset-hours
--natal-lat
--natal-lon
--natal-house-system
--natal-label
```

When natal inputs are present, the CSV also contains:

- natal body positions and houses
- natal ASC / MC / cusps
- transit-to-natal aspects for Sun..Saturn
- transit-to-transit and transit-to-natal declination parallels / contra-parallels
- declination speed and out-of-bounds flags
- current transit body placement inside natal houses
- pure astro language fields such as `astro_bias_text`, `astro_path_text`, `astro_signal_text`
- doctrine metadata such as `schema_version`, `doctrine_id`, `zodiac_mode`, `orb_family`

The current schema also exports doctrine-ready raw layers that were previously only implicit:

- `*_speed_state`, `*_station_intensity`, `*_ingress_intensity`
- `*_dignity_state`, `*_dignity_score`, `*_dispositor`
- `mutual_reception_count`, `mutual_reception_pairs`, `rulership_chain_score`
- `*_triplicity_role`, `*_triplicity_score`, `*_decan_ruler`
- `*_solar_condition`, `*_solar_separation`
- `moon_phase_half`
- `solar_quarter_name`, `solar_quarter_score`
- `sect_name`, `node_axis_sign`, `nodal_pressure_score`, `nodal_state`
- `eclipse_proximity_score`, `eclipse_state`, `eclipse_family_phase`

These fields stay fully causal because they are derived only from the candle-open sky state.

## Doctrine metadata

The builder now stamps every row with:

```text
--doctrine-id
--schema-version
--zodiac-mode
--body-universe
--orb-family
--parallel-orb-limit
```

That makes each CSV self-describing, which is important when multiple astro doctrines are being tested side by side.

Current default schema:

```text
astro_feature_schema_v4
```

## JSON config

The builder can now load a doctrine/build config directly:

```powershell
python tools/astro_feature_builder/astro_feature_builder.py `
  --config "tools/astro_feature_builder/astro_config.example.json"
```

CLI flags still win over config values, so the JSON file can hold the stable doctrine while one-off runs override dates or outputs.

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
