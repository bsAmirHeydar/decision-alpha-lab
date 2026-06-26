# EXP0016 Astro Meta Learner

This module learns from mechanical astrology features and actual future market outcomes.
It is not a rule-script that assumes `Jupiter = buy` or `Saturn = sell`. It builds a causal dataset:

```text
features at candle t -> future outcome after t
```

Then it trains interpretable models, stores model memory, extracts rules, and evaluates out-of-sample using chronological walk-forward tests.

## What it learns

Targets are generated for every configured horizon, for example 30, 60, 120 M1 bars:

- `label_direction_H`: `UP`, `DOWN`, `FLAT`
- `label_clean_long_H`: clean long path or not
- `label_clean_short_H`: clean short path or not
- `label_spike_H`: volatility expansion / spike
- `label_bull_trap_H`: upward excursion that later closes bearish
- `label_bear_trap_H`: downward excursion that later closes bullish

This separation is important. A benefic activation may mean participation or expansion, not necessarily buy direction.

## Memory contract

Every train run writes persistent memory to:

```text
Common\Files\astro_ml\memory\<ASSET>\<TIMEFRAME>\runs\<RUN_ID>\
```

A run stores:

- `model.joblib`
- `metadata.json`
- `metrics.json`
- `feature_importance.csv`
- `test_predictions.csv`
- `training_report.xlsx`
- `knowledge_base.json`

The cumulative memory files are:

```text
Common\Files\astro_ml\memory\<ASSET>\<TIMEFRAME>\memory_index.csv
Common\Files\astro_ml\memory\<ASSET>\<TIMEFRAME>\knowledge_memory.jsonl
Common\Files\astro_ml\memory\<ASSET>\<TIMEFRAME>\latest_run.txt
```

This is the reusable knowledge layer. It allows later code to query what the model learned and reuse a trained model on a new out-of-sample dataset.

## Step 0 - install dependencies

From project root:

```powershell
python -m pip install -r .\tools\astro_ml\requirements.txt
```

## Step 1 - export price candles from MT5

The astro feature CSV usually contains sky state, not OHLC. To learn what happened after each sky state, export price candles from MT5:

Compile and run:

```text
mql5/Scripts/AstroML/ExportRatesForAstroML.mq5
```

Example inputs:

```text
InpSymbol      = NAS100
InpTimeframe   = PERIOD_M1
InpFrom        = 2026.06.22 00:00
InpTo          = 2026.06.27 23:59
InpOutputName  = astro_ml_prices_NAS100_M1_20260622_to_now.csv
InpUseCommonFiles = true
```

Output:

```text
C:\Users\ABN\AppData\Roaming\MetaQuotes\Terminal\Common\Files\astro_ml_prices_NAS100_M1_20260622_to_now.csv
```

## Step 2 - build ML dataset

```powershell
cd "C:\Users\ABN\AppData\Roaming\MetaQuotes\Terminal\4769098028DB821E4654DC6D5C533078\MQL5\Shared Projects\decision-alpha-lab"

.\tools\astro_ml\build_astro_ml_dataset_common.ps1 `
  -AstroCsvName "astro_NAS100_M1_20260622_to_now_nasdaq100_natal_mql.csv" `
  -PriceCsvName "astro_ml_prices_NAS100_M1_20260622_to_now.csv" `
  -Asset NAS100 `
  -Timeframe M1 `
  -Horizons "30,60,120" `
  -OutName "astro_ml_dataset_NAS100_M1_20260622_to_now.csv" `
  -OpenAfter
```

Output:

```text
Common\Files\astro_ml\reports\NAS100\M1\astro_ml_dataset_NAS100_M1_20260622_to_now.csv
```

## Step 3 - train a direction model

```powershell
.\tools\astro_ml\train_astro_meta_learner_common.ps1 `
  -DatasetCsv "astro_ml\reports\NAS100\M1\astro_ml_dataset_NAS100_M1_20260622_to_now.csv" `
  -Target "label_direction_60" `
  -Asset NAS100 `
  -Timeframe M1 `
  -ModelType extra_trees `
  -TestFraction 0.25 `
  -OpenAfter
```

Train other targets:

```powershell
.\tools\astro_ml\train_astro_meta_learner_common.ps1 -DatasetCsv "astro_ml\reports\NAS100\M1\astro_ml_dataset_NAS100_M1_20260622_to_now.csv" -Target "label_clean_short_60" -Asset NAS100 -Timeframe M1 -OpenAfter
.\tools\astro_ml\train_astro_meta_learner_common.ps1 -DatasetCsv "astro_ml\reports\NAS100\M1\astro_ml_dataset_NAS100_M1_20260622_to_now.csv" -Target "label_bull_trap_60" -Asset NAS100 -Timeframe M1 -OpenAfter
.\tools\astro_ml\train_astro_meta_learner_common.ps1 -DatasetCsv "astro_ml\reports\NAS100\M1\astro_ml_dataset_NAS100_M1_20260622_to_now.csv" -Target "label_spike_60" -Asset NAS100 -Timeframe M1 -OpenAfter
```

## Step 4 - walk-forward validation

Use this for serious evaluation. Do not trust random split.

```powershell
.\tools\astro_ml\evaluate_walk_forward_common.ps1 `
  -DatasetCsv "astro_ml\reports\NAS100\M1\astro_ml_dataset_NAS100_M1_20260622_to_now.csv" `
  -Target "label_direction_60" `
  -Asset NAS100 `
  -Timeframe M1 `
  -TrainDays 120 `
  -TestDays 20 `
  -StepDays 20 `
  -EmbargoBars 120 `
  -OpenAfter
```

For short date ranges, reduce `TrainDays` and `TestDays`. For real research, use multi-year data.

## Step 5 - explain a saved model

Get the latest run id:

```powershell
Get-Content "$env:APPDATA\MetaQuotes\Terminal\Common\Files\astro_ml\memory\NAS100\M1\latest_run.txt"
```

Then:

```powershell
$RunId = Get-Content "$env:APPDATA\MetaQuotes\Terminal\Common\Files\astro_ml\memory\NAS100\M1\latest_run.txt" -Raw
$RunId = $RunId.Trim()
$RunDir = "astro_ml\memory\NAS100\M1\runs\$RunId"

.\tools\astro_ml\explain_astro_model_common.ps1 `
  -RunDir $RunDir `
  -PositiveLabel UP `
  -OpenAfter
```

## Step 6 - query model memory

```powershell
.\tools\astro_ml\query_astro_memory_common.ps1 `
  -Asset NAS100 `
  -Timeframe M1 `
  -OpenAfter
```

Filter memory by concept:

```powershell
.\tools\astro_ml\query_astro_memory_common.ps1 -Asset NAS100 -Timeframe M1 -Contains saturn -OpenAfter
```

## Step 7 - apply memory/model to a new out-of-sample dataset

Build a new dataset for a period that was not in training, then:

```powershell
.\tools\astro_ml\predict_with_astro_memory_common.ps1 `
  -RunDir $RunDir `
  -DatasetCsv "astro_ml\reports\NAS100\M1\astro_ml_dataset_NAS100_M1_new_oos.csv" `
  -OutCsv "astro_ml\reports\NAS100\M1\NAS100_M1_new_oos_predictions.csv" `
  -OpenAfter
```

## Research discipline

Use at least these comparisons:

- astro-only vs random/majority baseline
- astro-only vs time-of-day baseline
- astro-only vs price-only baseline
- train period vs validation period vs untouched test period
- walk-forward performance stability
- feature family ablation

Never accept a model because a single backtest looked good. Accept only if the behavior survives outside the training window.
