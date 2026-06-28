# Phoenix Flag Counting Validation Cases

This folder stores Level 13 validation baselines for the Phoenix flag-counting engine.

Level 13 does not invent expected counts. The workflow is:

1. Pick a case id from `docs/flag_counting/VALIDATION_CASE_REGISTRY.md`.
2. Pin broker symbol, timeframe, bar count/range, MT5 build, Phoenix inputs, and source commit.
3. Run `FlagCountingPhoenixExperiment.mq5` with export and validation enabled.
4. Save the generated CSV files from `MQL5/Files/FlagCountingPhoenix/` next to the case report.
5. Copy the accepted counts into the EA validation expected-min/max inputs for regression runs.

Recommended case artifact names:

```text
FC-GC-001_node_plateau_report.md
FC-GC-001_node_plateau_validation.csv
FC-GC-001_node_plateau_events.csv
FC-GC-001_node_plateau_hooks.csv
FC-GC-001_node_plateau_summary.csv
FC-GC-001_node_plateau_manifest.csv
FC-GC-001_node_plateau.png
```

A case is not frozen until it has a broker-valid range, expected counts, export files, screenshot, and notes explaining any intentional deviation from the previous baseline.

## Level 14 operational profiles

Before baselining a case, choose one profile explicitly:

```text
normal       -> manual visual/run check
clean_main   -> screenshot baseline
audit_export -> CSV-only audit
validation   -> regression with expected ranges
debug_max    -> noisy investigation
render_off   -> headless CSV check
safe_rollback-> cleanup/recovery only
```

For validation cases, prefer:

```text
InpReleaseProfile = FP_RELEASE_PROFILE_VALIDATION
InpValidationEnabled = true
InpExportAuditFiles = true
```
