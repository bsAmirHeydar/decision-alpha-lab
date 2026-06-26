# Astro ML Tools

راهنمای کامل استفاده در این فایل است:

```text
lab/03_experiments/EXP0016_astro_meta_learner/README.md
```

ساده‌ترین دستور عملیاتی:

```powershell
.\tools\astro_ml\run_astro_ml_protocol_common.ps1 `
  -AstroCsvName "astro_NAS100_M1_20260622_to_now_nasdaq100_natal_mql.csv" `
  -PriceCsvName "astro_ml_prices_NAS100_M1_20260622_to_now.csv" `
  -Asset NAS100 `
  -Timeframe M1 `
  -Preset sanity `
  -OpenAfter
```

---

# Human-Learning One-Command Protocol

Use this when you want the system to do the whole research loop itself:

```powershell
.\tools\astro_ml\run_astro_human_learning_protocol_common.ps1 `
  -Asset NAS100 `
  -Symbol NAS100 `
  -Timeframe M1 `
  -From "2026-06-22 00:00" `
  -To "2026-06-27 23:59" `
  -Preset sanity `
  -Horizons "30,60,120" `
  -OpenAfter
```

This does:

1. Fetch MT5 candles with `fetch_mt5_rates.py`.
2. Resolve/build astro features with `resolve_astro_feature_store.py`.
3. Build causal dataset with future outcomes.
4. Run the professional ML protocol.
5. Build skeptical cognitive memory with `build_cognitive_astro_memory.py`.

For multi-year research use `-Preset professional -RunWalkForward` and higher cognitive support thresholds.


## Self-Healing Data Protocol

From this version onward, the human-learning runner is data-self-healing. You do **not** need to manually prepare Excel/CSV price files before running it.

You only provide:

```powershell
-Asset NAS100
-Symbol NAS100
-Timeframe M1
-From "2026-06-22 00:00"
-To "2026-06-27 23:59"
```

The runner then does the following in order:

1. Checks whether a usable price CSV already exists in `Common\Files` or `Common\Files\astro_ml\prices\<SYMBOL>\<TF>`.
2. If price data is missing or unusable, it fetches candles directly from the local MetaTrader 5 terminal through the Python `MetaTrader5` package.
3. Checks whether a usable astro feature CSV already exists in `Common\Files`, `astro_archive`, or `astro/features`.
4. If astro data is missing or does not cover the requested range, it calls the project astro feature builder and creates a deterministic astro CSV using the asset natal defaults.
5. Builds the causal ML dataset.
6. Audits the dataset.
7. Trains the configured models.
8. Builds skeptical cognitive memory and rejects weak/unstable patterns.

### One-command NAS100 example

```powershell
cd "C:\Users\ABN\AppData\Roaming\MetaQuotes\Terminal\4769098028DB821E4654DC6D5C533078\MQL5\Shared Projects\decision-alpha-lab"

.\tools\astro_ml\run_astro_human_learning_protocol_common.ps1 `
  -Asset NAS100 `
  -Symbol NAS100 `
  -Timeframe M1 `
  -From "2026-06-22 00:00" `
  -To "2026-06-27 23:59" `
  -Preset sanity `
  -Horizons "30,60,120" `
  -OpenAfter
```

### Force refresh everything

Use this when you want to ignore old files and rebuild the whole input layer:

```powershell
.\tools\astro_ml\run_astro_human_learning_protocol_common.ps1 `
  -Asset NAS100 `
  -Symbol NAS100 `
  -Timeframe M1 `
  -From "2026-06-22 00:00" `
  -To "2026-06-27 23:59" `
  -Preset sanity `
  -ForceFetchPrice `
  -ForceBuildAstro `
  -OpenAfter
```

### Custom natal override

If the default natal anchor is not desired, pass natal values directly:

```powershell
.\tools\astro_ml\run_astro_human_learning_protocol_common.ps1 `
  -Asset NAS100 `
  -Symbol NAS100 `
  -Timeframe M1 `
  -From "2026-06-22 00:00" `
  -To "2026-06-27 23:59" `
  -NatalLabel "nasdaq100_index_1985_ny_open" `
  -NatalLocalDatetime "1985-01-31 09:30:00" `
  -NatalUtcOffsetHours "-5" `
  -NatalLat "40.7128" `
  -NatalLon "-74.0060" `
  -ForceBuildAstro `
  -OpenAfter
```

### Output proof

Every run prints and stores:

```text
RESOLVED_PRICE_CSV=...
RESOLVED_ASTRO_CSV=...
HUMAN_LEARNING_PROTOCOL_DIR=...
```

The manifest also records whether data came from archive, MT5 fetch, or deterministic astro build.


## Antifragile Learning Layer

The Human Learning V2 protocol now includes an antifragile layer by default. This layer does not try to add more and more fragile conditions. It compresses mechanical astro columns into broad concept families, tests simple principles first, compares them with chronological out-of-sample evidence, and stores only stable principles as reusable knowledge.

Main doctrine file:

```text
lab/03_experiments/EXP0016_astro_meta_learner/ANTIFRAGILE_LEARNING_DOCTRINE.md
```

Standalone command:

```powershell
.\tools\astro_ml\build_antifragile_astro_learning_common.ps1 `
  -DatasetCsv "astro_ml\reports\NAS100\M1\astro_ml_dataset_NAS100_M1_20260622_to_now.csv" `
  -Asset NAS100 `
  -Timeframe M1 `
  -OpenAfter
```

Human-learning protocol command with antifragile learning enabled by default:

```powershell
.\tools\astro_ml\run_astro_human_learning_protocol_common.ps1 `
  -Asset NAS100 `
  -Symbol NAS100 `
  -Timeframe M1 `
  -From "2026-06-22 00:00" `
  -To "2026-06-27 23:59" `
  -Preset professional `
  -Horizons "30,60,120" `
  -RunWalkForward `
  -OpenAfter
```

Optional neural challenger:

```powershell
.\tools\astro_ml\run_astro_human_learning_protocol_common.ps1 `
  -Asset NAS100 `
  -Symbol NAS100 `
  -Timeframe M1 `
  -From "2022-01-01 00:00" `
  -To "2026-06-27 23:59" `
  -Preset professional `
  -Horizons "30,60,120" `
  -EnableNeuralChallenger `
  -NeuralMinRows 8000 `
  -OpenAfter
```

The neural model is only a challenger. It is not accepted as knowledge unless it survives the same out-of-sample and gap controls as the simpler models.

Antifragile outputs:

```text
Common\Files\astro_ml\antifragile_memory\<ASSET>\<TIMEFRAME>\<RUN_ID>\
  ANTIFRAGILE_LEARNING_REPORT.md
  antifragile_learning_report.xlsx
  antifragile_mind.json
  antifragile_model_gate.csv
  antifragile_principles.csv
  stable_concepts.csv
  feature_to_concept_map.csv
```
