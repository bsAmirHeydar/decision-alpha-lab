# Astro ML Training Quickstart

This is the shortest reliable path to start training the astro ML stack.

## What is ready

The astro stack is ready for training when these are true:

- the astro feature builder is producing `astro_feature_schema_v4`
- the dataset audit passes without critical gates
- chronological train/test is enabled
- walk-forward is enabled for serious runs
- fragility audit is enabled if you want hardened principles instead of raw research output

The project is now wired so professional runs prefer all of the above by default.

## Recommended command

Run this from the project root:

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
  -ForceBuildAstro `
  -OpenAfter
```

## What this does

This one command will:

- resolve or fetch price data
- rebuild astro features if needed
- require a usable training dataset
- train the core targets
- run walk-forward validation
- build antifragile memory
- run the final fragility audit
- write reports into `Common\Files\astro_ml\...`

## Where to look after the run

Start with these outputs:

- `HUMAN_LEARNING_REPORT.md`
- `protocol_manifest.json`
- `dataset_audit.json`
- `walkforward_report.json`
- `ANTIFRAGILE_LEARNING_REPORT.md`
- `FRAGILITY_AUDIT_REPORT.md`
- `antifragile_decision_memory.json`

## How to read the result

Use this order:

1. `dataset_audit.json`
Check whether the dataset is usable and whether any critical gate failed.

2. `walkforward_report.json`
Check `mean_edge_balanced_accuracy`, `worst_edge_balanced_accuracy`, and `negative_edge_folds`.

3. `ANTIFRAGILE_LEARNING_REPORT.md`
Check whether any principles survived the first antifragile reduction gate.

4. `FRAGILITY_AUDIT_REPORT.md`
Check whether any principle was actually hardened.

5. `antifragile_decision_memory.json`
Check `production_gate`.

If `production_gate` is `research_only`, the run is useful for learning but not for trusted downstream use.

## If you only want a plumbing check

Use a short run:

```powershell
.\tools\astro_ml\run_astro_human_learning_protocol_common.ps1 `
  -Asset NAS100 `
  -Symbol NAS100 `
  -Timeframe M1 `
  -From "2026-06-22 00:00" `
  -To "2026-06-27 23:59" `
  -Preset sanity `
  -Horizons "30,60,120" `
  -ForceBuildAstro `
  -OpenAfter
```

This is good for smoke testing the pipeline, not for claiming stable learned knowledge.
