# Astro ML Tools

This directory contains the operational tooling for EXP0016, the Astro Meta Learner and Antifragile Astro Learning protocol in Decision Alpha Lab.

The purpose of these tools is not to hard-code astrological trading rules. The purpose is to turn mechanical astro features into causal learning datasets, attach them to real market outcomes, train skeptical models, test them chronologically, store reusable memory, and extract principles that survive out-of-sample pressure.

The full experiment manual is here:

```text
contexts/legacy/lab_experiments/EXP0016_astro_meta_learner/README.md
```

The antifragile learning doctrine is here:

```text
docs/evidence/exp0016_antifragile_astro_learning_doctrine/a5f84b716738_ANTIFRAGILE_LEARNING_DOCTRINE.md
```

---

## 1. What this toolkit does

The toolkit automates this pipeline:

```text
Symbol + timeframe + date range
        |
        v
Self-healing data resolver
        |
        +-- price candles from local MetaTrader 5 if missing
        +-- astro feature CSV from archive or deterministic builder if missing
        |
        v
Causal dataset builder
        |
        +-- future returns
        +-- MFE / MAE
        +-- clean path labels
        +-- spike labels
        +-- bull-trap and bear-trap labels
        |
        v
Dataset audit
        |
        +-- missing values
        +-- time gaps
        +-- label distributions
        +-- leakage-name checks
        +-- constant columns
        |
        v
Model training and evaluation
        |
        +-- chronological train/test
        +-- walk-forward evaluation
        +-- baseline comparison
        +-- feature importance
        |
        v
Human-learning memory
        |
        +-- case memory
        +-- concept memory
        +-- skeptical rule memory
        |
        v
Antifragile learning layer
        |
        +-- broad concept abstraction
        +-- simple principles first
        +-- complexity penalty
        +-- optional neural challenger
        +-- accepted and rejected principles
```

---

## 2. Installation

Run once from the project root:

```powershell
cd "C:\Users\ABN\AppData\Roaming\MetaQuotes\Terminal\4769098028DB821E4654DC6D5C533078\MQL5\Shared Projects\decision-alpha-lab"

python -m pip install -r .\src\engine\legacy\research\astro_ml\requirements.txt
```

If your environment does not install optional packages automatically, install the common stack manually:

```powershell
python -m pip install pandas numpy scikit-learn joblib openpyxl MetaTrader5
```

`MetaTrader5` is only required for direct candle fetching from the local MT5 terminal. If you already have price CSVs, the rest of the pipeline can run without direct MT5 fetching.

---

## 3. Recommended one-command workflow

Use the human-learning protocol. It is self-healing: it checks whether the required price and astro files already exist, and if they do not, it attempts to create them.

```powershell
.\src\engine\legacy\research\astro_ml\run_astro_human_learning_protocol_common.ps1 `
  -Asset NAS100 `
  -Symbol NAS100 `
  -Timeframe M1 `
  -From "2026-06-22 00:00" `
  -To "2026-06-27 23:59" `
  -Preset sanity `
  -Horizons "30,60,120" `
  -OpenAfter
```

This command does the following:

1. Looks for an existing price CSV.
2. If no valid price CSV is found, fetches candles from the local MT5 terminal.
3. Looks for an existing astro feature CSV.
4. If no valid astro CSV is found, builds one using the project astro feature builder and the configured natal defaults.
5. Builds a causal ML dataset.
6. Runs dataset audit.
7. Trains the configured models.
8. Builds cognitive memory.
9. Builds the antifragile learning layer.
10. Writes reports, manifests, and reusable memory files under `Common\Files\astro_ml`.

In `professional` preset the dataset audit is a gate, not just a report. Critical data-quality failures stop the protocol before training unless `--allow-audit-warnings` is explicitly used.

---

## 4. Force a full rebuild

Use this when you want to ignore cached files and rebuild everything from scratch:

```powershell
.\src\engine\legacy\research\astro_ml\run_astro_human_learning_protocol_common.ps1 `
  -Asset NAS100 `
  -Symbol NAS100 `
  -Timeframe M1 `
  -From "2026-06-22 00:00" `
  -To "2026-06-27 23:59" `
  -Preset sanity `
  -Horizons "30,60,120" `
  -ForceFetchPrice `
  -ForceBuildAstro `
  -OpenAfter
```

Use `-ForceFetchPrice` when MT5 has better candles than the existing archive. Use `-ForceBuildAstro` when you changed natal assumptions, astro builder settings, or the feature schema.

---

## 5. Professional multi-year protocol

Use this for serious research, not for a small sanity check:

```powershell
.\src\engine\legacy\research\astro_ml\run_astro_human_learning_protocol_common.ps1 `
  -Asset NAS100 `
  -Symbol NAS100 `
  -Timeframe M1 `
  -From "2022-01-01 00:00" `
  -To "2026-06-27 23:59" `
  -Preset professional `
  -Horizons "30,60,120" `
  -RunWalkForward `
  -TrainDays 120 `
  -TestDays 20 `
  -StepDays 20 `
  -EmbargoBars 120 `
  -OpenAfter
```

The walk-forward test is the most important part. It forces the learner to make predictions on later data that was not part of the training window.

Walk-forward reports now include mean balanced edge, worst-fold edge, edge standard deviation, and negative-edge fold count versus the majority baseline. Embargo bars are converted into a real time gap between train and test windows.

---

## 6. Neural challenger mode

The neural model is intentionally not treated as an oracle. It is a challenger. It must beat simpler models out-of-sample after complexity penalties. If it only looks good in training, it is rejected.

```powershell
.\src\engine\legacy\research\astro_ml\run_astro_human_learning_protocol_common.ps1 `
  -Asset NAS100 `
  -Symbol NAS100 `
  -Timeframe M1 `
  -From "2022-01-01 00:00" `
  -To "2026-06-27 23:59" `
  -Preset professional `
  -Horizons "30,60,120" `
  -RunWalkForward `
  -EnableNeuralChallenger `
  -NeuralMinRows 8000 `
  -OpenAfter
```

The default philosophy remains principle-first and reductionist: a simple stable rule is preferred over a complex fragile model.

Model cards now include baseline edge and probability-quality diagnostics. A model with apparent accuracy but poor edge or poor Brier/log-loss quality remains research-only.

---

## 7. Main tool files

| File | Purpose |
|---|---|
| `fetch_mt5_rates.py` | Fetches OHLC candles from the local MetaTrader 5 terminal. |
| `resolve_astro_feature_store.py` | Finds an existing astro feature CSV or builds one through the project astro builder. |
| `build_astro_ml_dataset.py` | Joins astro features with price outcomes and creates causal labels. |
| `astro_ml_audit_dataset.py` | Audits the generated dataset before training. |
| `train_astro_meta_learner.py` | Trains interpretable supervised models with chronological splits. |
| `evaluate_walk_forward.py` | Runs walk-forward validation with embargo support. |
| `explain_astro_model.py` | Produces feature importance and rule-level explanations. |
| `build_cognitive_astro_memory.py` | Creates case memory, concept memory, and skeptical rules. |
| `build_antifragile_astro_learning.py` | Compresses features into broad concepts and tests stable principles. |
| `build_antifragile_fragility_audit.py` | Hardens accepted principles against temporal, perturbation, dependency, contradiction, and condition-creep fragility. |
| `query_astro_memory.py` | Queries persistent memory, lessons, and decision-memory production gates. |
| `predict_with_astro_memory.py` | Applies a saved model and annotates each prediction with target-aware gate and hardened-principle support/conflict. |
| `export_astro_knowledge_pack.py` | Exports model memory, model cards, decision memories, and hardened principles into a portable pack. |
| `run_astro_human_learning_protocol.py` | One-command orchestrator for self-healing data, training, memory, and antifragile learning. |

Every `.py` script has a matching `_common.ps1` wrapper for the Windows/MetaTrader workflow.

---

## 8. Output directories

All operational outputs are written under MetaTrader Common Files:

```text
C:\Users\ABN\AppData\Roaming\MetaQuotes\Terminal\Common\Files\astro_ml\
```

Important subdirectories:

```text
astro_ml\prices\<SYMBOL>\<TIMEFRAME>\
astro_ml\reports\<ASSET>\<TIMEFRAME>\
astro_ml\memory\<ASSET>\<TIMEFRAME>\
astro_ml\cognitive_memory\<ASSET>\<TIMEFRAME>\
astro_ml\antifragile_memory\<ASSET>\<TIMEFRAME>\
astro_ml\human_learning_protocols\<ASSET>\<TIMEFRAME>\
```

The most important reports are:

```text
HUMAN_LEARNING_REPORT.md
COGNITIVE_MEMORY_REPORT.md
ANTIFRAGILE_LEARNING_REPORT.md
protocol_report.xlsx
antifragile_learning_report.xlsx
antifragile_mind.json
antifragile_decision_memory.json
```

---

## 9. How to read the results

Do not ask only whether the model predicts `UP` or `DOWN`. The system is multi-outcome by design.

A useful astro signal may appear as:

- direction edge,
- clean long path,
- clean short path,
- spike risk,
- bull-trap risk,
- bear-trap risk,
- hardened support for one outcome with low conflict,
- no-trade/no-edge regime.

The most useful result is not always a trade direction. Sometimes the best learned knowledge is:

```text
This astro condition does not predict direction, but it reliably warns that long continuation is fragile.
```

or:

```text
This condition does not create clean trend, but it raises spike/hunt probability.
```

When using `predict_with_astro_memory.py`, the extra trust fields matter:

- `production_gate` tells you whether the latest target-aware hardening layer passed.
- `hardened_support_count` tells you how many hardened principles support the predicted label on that row.
- `hardened_conflict_count` shows whether hardened principles disagree with the prediction.
- `trust_tier` compresses that state into `research`, `candidate`, or `hardened_candidate`.

---

## 10. Acceptance standard

A learned pattern is not accepted because it is beautiful in training. It is accepted only when it survives:

1. enough support,
2. chronological out-of-sample test,
3. baseline comparison,
4. train/test stability,
5. complexity penalty,
6. concept-level interpretability.

Rejected patterns are valuable. They are stored so that the system remembers what not to believe.


## Antifragile Fragility Audit

The Astro ML toolkit includes a final audit layer that hardens the learner's beliefs.

Run it directly:

```powershell
.\src\engine\legacy\research\astro_ml\build_antifragile_fragility_audit_common.ps1 `
  -DatasetCsv "astro_ml\reports\NAS100\M1\astro_ml_dataset_NAS100_M1_2022_to_2026.csv" `
  -Asset NAS100 `
  -Timeframe M1 `
  -OpenAfter
```

Or let the self-healing human-learning protocol run it automatically:

```powershell
.\src\engine\legacy\research\astro_ml\run_astro_human_learning_protocol_common.ps1 `
  -Asset NAS100 `
  -Symbol NAS100 `
  -Timeframe M1 `
  -From "2022-01-01 00:00" `
  -To "2026-06-27 23:59" `
  -Preset professional `
  -RunWalkForward `
  -OpenAfter
```

The audit is designed to catch model-thinking fragilities:

- single-split luck;
- condition creep;
- fragile sample support;
- noisy neural confidence;
- overdependence on one concept family;
- contradiction between multiple labels;
- perturbation sensitivity.

The most important file is:

```text
hardened_principles.csv
```

Only this file should be considered a candidate for conversion into production filters or MQL rules.
