# EXP0016 Astro Meta Learner

## Professional Operating Manual for Self-Healing, Human-Learning, Antifragile Astro ML

EXP0016 is the machine-learning research layer for the mechanical astrology system in Decision Alpha Lab. Its purpose is to learn how astro states actually map to market behavior instead of forcing fixed symbolic rules such as `Jupiter = buy` or `Saturn = sell`.

The experiment asks a more serious question:

```text
Given the mechanical astro state at candle t,
what did the market actually do after t,
and which astro principles survived out-of-sample testing?
```

The system is designed as a skeptical learning machine. It fetches or builds its own data, creates causal labels, trains multiple models, evaluates them chronologically, stores reusable memory, and then reduces what it learned into stable principles.

The antifragile thinking doctrine is documented here:

```text
docs/evidence/exp0016_antifragile_astro_learning_doctrine/a5f84b716738_ANTIFRAGILE_LEARNING_DOCTRINE.md
```

---

## 1. Core goal

The goal is not to create a complicated predictor that memorizes fragile patterns. The goal is to build a learning system that can distinguish between:

- true directional pressure,
- clean path potential,
- volatility and spike risk,
- bull-trap risk,
- bear-trap risk,
- no-edge regimes,
- unstable patterns that should be rejected.

This is why the system trains multiple targets instead of forcing every astro condition into a binary buy/sell decision.

---

## 2. High-level architecture

```text
Asset / Symbol / Timeframe / Date Range
        |
        v
Self-Healing Data Layer
        |
        +-- resolves existing price CSV
        +-- fetches missing MT5 candles
        +-- resolves existing astro feature CSV
        +-- builds missing astro feature store from project builder
        |
        v
Causal Dataset Builder
        |
        +-- future returns
        +-- MFE / MAE
        +-- direction labels
        +-- clean long labels
        +-- clean short labels
        +-- spike labels
        +-- bull-trap labels
        +-- bear-trap labels
        |
        v
Dataset Audit
        |
        +-- missing-value checks
        +-- label-distribution checks
        +-- time-gap checks
        +-- leakage-name checks
        +-- constant-column checks
        |
        v
Model Suite
        |
        +-- baseline
        +-- interpretable tree/forest models
        +-- walk-forward validation
        +-- optional neural challenger
        |
        v
Cognitive Memory
        |
        +-- case memory
        +-- concept memory
        +-- skeptical rule memory
        |
        v
Antifragile Learning Layer
        |
        +-- concept abstraction
        +-- principle mining
        +-- model gate
        +-- accepted principles
        +-- rejected fragile patterns
        |
        v
Reusable Astro Mind
```

---

## 3. Design principles

### 3.1 Causality first

A feature at candle `t` may only use information available at `t`. Outcome labels are computed after `t` and must never leak back into the input feature set.

### 3.2 Time-aware testing

Random train/test splits are not sufficient for market data. EXP0016 uses chronological splits and supports walk-forward validation with embargo.

### 3.3 Multi-outcome thinking

The market does not only go up or down. The same astro condition may create:

- directional continuation,
- reversal,
- spike,
- hunt,
- noisy range,
- trap,
- clean path,
- no edge.

Therefore EXP0016 learns multiple targets.

### 3.4 Principle-first abstraction

Detailed astro columns are compressed into broader concept families before final interpretation. The learner first asks whether a broad principle is stable. Only then should it inspect fine details.

Examples of concept families:

```text
benefic_expansion
malefic_pressure
mars_impulse
lunar_timing
mercury_noise
pluto_extreme
uranus_shock
neptune_fog
natal_activation
aspect_tension
aspect_harmony
house_context
market_quality
directional_bias
```

### 3.5 Reductive skepticism

The system must not keep adding conditions until something fits the past. A pattern is rejected unless it survives out-of-sample and remains simple enough to be useful.

---

## 4. Main operating mode: one-command human-learning protocol

From the project root:

```powershell
cd "C:\Users\ABN\AppData\Roaming\MetaQuotes\Terminal\4769098028DB821E4654DC6D5C533078\MQL5\Shared Projects\decision-alpha-lab"
```

Run a quick sanity protocol:

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

This is the preferred operational command because it is self-healing. It checks for missing data and creates what it needs.

---

## 5. What the one-command protocol does

The protocol executes the full research chain:

1. **Resolve price data.** It searches existing Common Files and the `astro_ml\prices` archive.
2. **Fetch price data if missing.** It uses the local MetaTrader 5 terminal through the Python `MetaTrader5` package.
3. **Resolve astro data.** It searches existing astro feature CSVs in Common Files and known astro archives.
4. **Build astro data if missing.** It calls the project astro feature builder and uses natal defaults or user-provided natal overrides.
5. **Create causal ML dataset.** It merges astro features with future market outcomes.
6. **Audit dataset.** It checks label balance, missing values, time gaps, constant columns, and suspicious leakage names.
7. **Train models.** It trains configured targets with chronological train/test splits.
8. **Run walk-forward if requested.** It evaluates stability over rolling future windows.
9. **Build cognitive memory.** It stores cases, concepts, and skeptical rules.
10. **Build antifragile memory.** It abstracts features into principles and rejects unstable patterns.
11. **Write reports and manifests.** It records exactly where each input came from and what was produced.

Professional preset now treats the dataset audit as a hard gate by default. A professional run can stop before training if the dataset is too small, lacks a usable time column, has leakage-like columns inside the usable feature set, or has targets that are too imbalanced to trust. Use sanity mode for small plumbing checks.

---

## 6. Self-healing data protocol

You do not need to manually prepare Excel files. You only provide:

```text
Asset
Symbol
Timeframe
From
To
```

The runner resolves the rest.

### 6.1 Normal self-healing run

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

### 6.2 Force rebuilding the input layer

```powershell
.\tools\astro_ml\run_astro_human_learning_protocol_common.ps1 `
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

Use this after changing broker history, symbol naming, natal assumptions, or astro builder settings.

### 6.3 Natal override example

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

---

## 7. Professional multi-year protocol

A few days of data can test the pipeline, but it cannot prove edge. For serious research, use multiple years:

```powershell
.\tools\astro_ml\run_astro_human_learning_protocol_common.ps1 `
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

Walk-forward validation is the most important evidence source. It asks whether a learned astro principle survives after the training period ends.

The walk-forward layer now reports mean edge, worst-fold edge, edge standard deviation, and negative-edge fold count against the majority baseline. The embargo is applied as a real time gap between the training window and the test window.

---

## 8. Neural challenger protocol

EXP0016 can optionally train a neural challenger. This should be used only with enough rows.

```powershell
.\tools\astro_ml\run_astro_human_learning_protocol_common.ps1 `
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

The neural challenger is rejected if it fails the same antifragile gate as simpler models. It is allowed to win only if it provides out-of-sample value after complexity pressure.

---

## 9. Targets and labels

EXP0016 builds labels for multiple horizons such as 30, 60, and 120 bars.

| Target family | Meaning |
|---|---|
| `label_direction_H` | Whether price moved up, down, or flat over horizon `H`. |
| `label_clean_long_H` | Whether the long path was favorable relative to adverse movement. |
| `label_clean_short_H` | Whether the short path was favorable relative to adverse movement. |
| `label_spike_H` | Whether the future window had abnormal range or hunt-like expansion. |
| `label_bull_trap_H` | Whether price first behaved bullishly and later failed. |
| `label_bear_trap_H` | Whether price first behaved bearishly and later reversed. |

This is essential because astro may predict volatility better than direction, or trap risk better than continuation.

---

## 10. Output directories

All outputs are stored under MetaTrader Common Files:

```text
C:\Users\ABN\AppData\Roaming\MetaQuotes\Terminal\Common\Files\astro_ml\
```

Important paths:

```text
astro_ml\prices\<SYMBOL>\<TIMEFRAME>\
astro_ml\reports\<ASSET>\<TIMEFRAME>\
astro_ml\memory\<ASSET>\<TIMEFRAME>\
astro_ml\cognitive_memory\<ASSET>\<TIMEFRAME>\
astro_ml\antifragile_memory\<ASSET>\<TIMEFRAME>\
astro_ml\human_learning_protocols\<ASSET>\<TIMEFRAME>\
```

Key files:

```text
HUMAN_LEARNING_REPORT.md
COGNITIVE_MEMORY_REPORT.md
ANTIFRAGILE_LEARNING_REPORT.md
protocol_report.xlsx
antifragile_learning_report.xlsx
antifragile_mind.json
human_learning_manifest.json
```

---

## 11. How to interpret the reports

### 11.1 HUMAN_LEARNING_REPORT.md

This report tells you what the protocol executed, which files were resolved or created, and where the final outputs were written.

### 11.2 Dataset audit

The audit tells you whether the dataset is usable. Warnings here must be taken seriously. A model trained on a broken dataset is worse than no model.

Important checks:

- row count,
- missing values,
- label distribution,
- constant features,
- time gaps,
- suspicious leakage-like column names.

### 11.3 Model card

The model card summarizes the target, model type, train/test split, metrics, baseline comparison, and feature importance.

### 11.4 Cognitive memory

Cognitive memory stores historical cases and concept-level observations.

Example interpretation:

```text
This setup was seen in 84 historical cases.
The model predicted bull-trap risk.
Actual bull-trap outcome happened in 61% of comparable cases.
The shared signature was high benefic expansion with rising malefic pressure.
```

### 11.5 Antifragile report

The antifragile report is the final skeptical filter. It tells you which principles survived and which were rejected.

A rejected principle is not a failure. It is useful negative knowledge.

---

## 12. Acceptance criteria

A model or principle should not be trusted unless it satisfies most of the following:

1. It beats the majority-class or naive baseline.
2. It survives chronological out-of-sample testing.
3. It has enough sample support.
4. It has acceptable train/test gap.
5. It is not merely a high-complexity artifact.
6. Its important features map to meaningful concept families.
7. It remains useful across multiple periods or regimes.
8. It provides a useful behavior label: direction, clean path, spike, trap, or no-trade filter.
9. It has acceptable probability quality, including Brier/log-loss diagnostics when probability output is available.
10. It survives the final hardening gate without contradiction or condition-creep rejection.

---

## 13. How to decide what was learned

Use the following decision table:

| Result | Interpretation | Next action |
|---|---|---|
| Direction model beats baseline OOS | Astro may contain directional information. | Build a conservative direction filter. |
| Clean-path model beats baseline OOS | Astro may identify smoother movement. | Use as path-quality filter. |
| Trap model beats baseline OOS | Astro may warn against naive continuation. | Use to block bad entries. |
| Spike model beats baseline OOS | Astro may identify volatility windows. | Use for hunt/spike timing, not direction. |
| Only train metrics are good | Likely overfit. | Reject or reduce complexity. |
| No target beats baseline | Current astro feature form has no proven edge. | Change labels, horizon, asset, or feature design. |
| Mean edge is positive but worst-fold edge is negative | Model may be regime-fragile. | Keep as research only. |
| Probability metrics are poor | Model may be overconfident. | Calibrate or reject before production. |
| A principle passes temporal stress but fails contradiction/creep audit | The interpretation is not clean enough. | Reject as hardened knowledge. |

---

## 14. Relationship with the existing astro expert

The existing astro expert is rule-based. It converts astro scores into entry states such as `enter_long` or `enter_short`.

EXP0016 is a learning and audit layer. It is designed to answer questions such as:

```text
Was the rule-based expert confusing risk activation with bullish direction?
Did Jupiter/Venus support actually produce continuation or bull traps?
Did Saturn/Mars pressure predict sell direction or only noisy path?
Did natal activation help direction, volatility, or path quality?
```

The long-term plan is not to replace the expert blindly. The plan is to let EXP0016 discover stable principles, then export them back into simpler, more robust rule layers.

---

## 15. Files added by EXP0016

Main Python tools:

```text
tools/astro_ml/fetch_mt5_rates.py
tools/astro_ml/resolve_astro_feature_store.py
tools/astro_ml/build_astro_ml_dataset.py
tools/astro_ml/astro_ml_audit_dataset.py
tools/astro_ml/train_astro_meta_learner.py
tools/astro_ml/evaluate_walk_forward.py
tools/astro_ml/explain_astro_model.py
tools/astro_ml/build_cognitive_astro_memory.py
tools/astro_ml/build_antifragile_astro_learning.py
tools/astro_ml/run_astro_human_learning_protocol.py
```

Windows wrappers:

```text
tools/astro_ml/*_common.ps1
```

MQL5 support:

```text
mql5/Scripts/AstroML/ExportRatesForAstroML.mq5
```

Documentation:

```text
lab/03_experiments/EXP0016_astro_meta_learner/README.md
docs/evidence/exp0016_antifragile_astro_learning_doctrine/a5f84b716738_ANTIFRAGILE_LEARNING_DOCTRINE.md
tools/astro_ml/README.md
```

---

## 16. Practical workflow checklist

1. Apply the latest patch.
2. Install Python dependencies.
3. Make sure MT5 is open and logged in if you want automatic candle fetching.
4. Run the one-command human-learning protocol with `-Preset sanity`.
5. Open the report and verify that price and astro data were resolved correctly.
6. Check dataset audit warnings.
7. Run `-Preset professional` on a larger period.
8. Run walk-forward validation.
9. Inspect `antifragile_mind.json` and `ANTIFRAGILE_LEARNING_REPORT.md`.
10. Only promote stable, simple principles to future execution logic.

---

## 17. The most important warning

Do not accept a pattern just because it looks intelligent. Market data can produce convincing illusions. EXP0016 is intentionally built to be skeptical.

The correct scientific outcome may be:

```text
This feature family does not produce a stable edge.
```

That is valuable. It prevents the project from building fragile rules on top of noise.


## Final Fragility Audit and Hardening Layer

The human-learning protocol now runs an additional hardening layer after the antifragile learner. This layer audits the learner's own thinking failures instead of training yet another model.

It tests:

- temporal fold survival of accepted principles;
- sensitivity to small numeric perturbations;
- sensitivity to random feature dropout;
- dependence on a single concept family;
- contradictions across direction/path/trap targets;
- condition creep and rule proliferation.

The output is stored under:

```text
Common\Files\astro_ml\antifragile_fragility_audits\<ASSET>\<TIMEFRAME>\<RUN_ID>\
```

Important files:

```text
FRAGILITY_AUDIT_REPORT.md
fragility_audit_report.xlsx
hardened_principles.csv
fragility_flags.csv
temporal_principle_stress.csv
perturbation_stress.csv
concept_dependency_stress.csv
antifragile_decision_memory.json
```

### Operational Meaning

The system now distinguishes between three levels of knowledge:

| Level | Meaning | Can be used in production logic? |
| --- | --- | --- |
| Pattern | Interesting in one sample | No |
| Candidate principle | Passed the first antifragile gate | Not yet |
| Hardened principle | Survived time folds, perturbation, dependency, contradiction, and simplicity gates | Yes, as a filter or research-backed principle |

### Standalone Fragility Audit Command

If a dataset and antifragile memory already exist, run:

```powershell
.\tools\astro_ml\build_antifragile_fragility_audit_common.ps1 `
  -DatasetCsv "astro_ml\reports\NAS100\M1\astro_ml_dataset_NAS100_M1_2022_to_2026.csv" `
  -Asset NAS100 `
  -Timeframe M1 `
  -OpenAfter
```

### Strict Mode

For a stricter antifragile audit:

```powershell
.\tools\astro_ml\build_antifragile_fragility_audit_common.ps1 `
  -DatasetCsv "astro_ml\reports\NAS100\M1\astro_ml_dataset_NAS100_M1_2022_to_2026.csv" `
  -Asset NAS100 `
  -Timeframe M1 `
  -Folds 10 `
  -MinSurvivalRate 0.70 `
  -MinMedianLift 1.08 `
  -MinWorstLift 1.00 `
  -MaxPerturbDrop 0.035 `
  -MaxRulesPerTarget 8 `
  -OpenAfter
```

This makes the learner more skeptical. It will accept fewer principles, but the surviving principles should be more robust.
