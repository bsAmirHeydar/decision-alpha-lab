# Astro Signal Validator

This tool audits the astro-only paper journals produced by the execution families.

## Full suite

For phase-8 style batch validation, run the family suite:

```bash
python tools/astro_validation/astro_family_validation_suite.py ^
  --csv lab/03_experiments/EXP0013_astro_feature_store/sample.csv ^
  --out-dir lab/03_experiments/EXP0013_astro_feature_store/validation_suite ^
  --config tools/astro_feature_builder/astro_config.example.json ^
  --families A0001 A0002 A0003 A0004 A0005 A0006 A0007 A0090
```

Suite outputs:

- `journals/*.csv`: one paper journal per family
- `reports/*.json`: one validation report per family
- `suite_manifest.json`: end-to-end run manifest
- `promotion_snapshot.json`: fast promotion / reject-now snapshot

There is also a Common Files PowerShell helper:

```powershell
.\tools\astro_validation\run_astro_family_validation_suite_common.ps1 `
  -CsvName "astro_live_mql.csv" `
  -OutFolder "daily_suite"
```

## Research runner

You can now generate those journals directly from a raw astro feature CSV, without waiting for MT5 execution:

```bash
python tools/astro_validation/astro_paper_family_runner.py ^
  --csv lab/03_experiments/EXP0013_astro_feature_store/sample.csv ^
  --family A0001 ^
  --out-journal lab/03_experiments/EXP0013_astro_feature_store/paper/a0001_journal.csv ^
  --config tools/astro_feature_builder/astro_config.example.json
```

Supported families:

- `A0001` transit trend pulse
- `A0002` natal resonance
- `A0003` friction polarity
- `A0004` sect benefic pressure
- `A0005` moon timing window
- `A0006` angular activation
- `A0007` station transition
- `A0090` live shell doctrine profile in paper form

The runner stays astro-only:

- raw feature CSV in
- pure astro timing stack and score surface
- family gates and state machine
- paper journal out

That journal can then be validated with the validator below.

## Excel entry / exit workbook

You can also build one workbook that merges entry windows, entry bars, and exit events across multiple families directly from the raw astro CSV:

```bash
python tools/astro_validation/astro_family_entry_exit_excel_suite.py ^
  --csv lab/03_experiments/EXP0013_astro_feature_store/sample.csv ^
  --out-xlsx lab/03_experiments/EXP0013_astro_feature_store/reports/astro_family_entries.xlsx ^
  --config tools/astro_feature_builder/astro_config.example.json ^
  --families PURE A0001 A0004 A0005 A0006 A0090 ^
  --also-csv
```

Workbook outputs:

- `RunSummary`
- `FamilyOverview`
- `AllEntryWindows`
- `AllEntryBars`
- `AllExitEvents`
- one summary/window/exit sheet per family

There is also a Common Files helper:

```powershell
.\tools\astro_validation\build_family_entry_exit_excel_common.ps1 `
  -CsvName "astro_live_mql.csv" `
  -OutName "astro_family_entries.xlsx" `
  -AlsoCsv
```

## Final entry report

You can also compress all family votes into one final astro-only decision workbook:

```bash
python tools/astro_validation/astro_final_entry_report.py ^
  --csv lab/03_experiments/EXP0013_astro_feature_store/sample.csv ^
  --out-xlsx lab/03_experiments/EXP0013_astro_feature_store/reports/astro_final_entry_report.xlsx ^
  --config tools/astro_feature_builder/astro_config.example.json ^
  --families A0001 A0002 A0003 A0004 A0005 A0006 A0007 ^
  --profile pure_strict ^
  --also-csv
```

Report outputs:

- `FinalSummary`
- `FamilyWeights`
- `BarConsensus`
- `FinalEntryWindows`

The strict profile keeps the final signal more astro-pure:

- default family set excludes `A0090`
- veto reasons are written per bar
- minute exhaustion, macro/meso/micro timing weakness, and direction conflict can all block an entry

There is also a Common Files helper:

```powershell
.\tools\astro_validation\build_final_entry_report_common.ps1 `
  -CsvName "astro_live_mql.csv" `
  -OutName "astro_final_entry_report.xlsx" `
  -Profile "pure_strict" `
  -AlsoCsv
```

## Finalization suite

For a full end-to-end astro finalization pass on one real CSV:

```bash
python tools/astro_validation/astro_finalization_suite.py ^
  --csv data/astro/astro_NAS100_M1_20260622_to_now_nasdaq100_natal_mql.csv ^
  --out-dir lab/03_experiments/EXP0013_astro_feature_store/finalization ^
  --config tools/astro_feature_builder/astro_config.example.json
```

Suite outputs:

- `family_validation/`: family journals, reports, promotion snapshot
- `finalization_manifest.json`: final cross-profile summary

If you only want purity calibration recommendations:

```bash
python tools/astro_validation/astro_purity_calibrator.py ^
  --csv data/astro/astro_NAS100_M1_20260622_to_now_nasdaq100_natal_mql.csv ^
  --out-json lab/03_experiments/EXP0013_astro_feature_store/finalization/purity_calibration.json ^
  --config tools/astro_feature_builder/astro_config.example.json
```

There is also a Common Files helper:

```powershell
.\tools\astro_validation\run_astro_finalization_suite_common.ps1 `
  -CsvName "astro_live_mql.csv" `
  -OutFolder "astro_finalization"
```

## What it checks

- doctrine and schema stability
- phase / action distribution
- direction and regime balance
- macro / meso / micro / minute timing averages
- hold-duration profile
- threshold sensitivity grid
- shuffled baseline on the action stream

## Example

```bash
python tools/astro_validation/astro_signal_validator.py ^
  --journal lab/03_experiments/EXP0013_astro_feature_store/paper/a0001_journal.csv ^
  --out-json lab/03_experiments/EXP0013_astro_feature_store/validation/a0001_report.json
```

The output is a JSON report so each family can be reviewed, promoted, or rejected without mixing in discretionary interpretation.
