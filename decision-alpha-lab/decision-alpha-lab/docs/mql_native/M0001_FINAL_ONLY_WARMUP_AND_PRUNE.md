# M0001 Final-Only Research Report, Warmup, and MQL Prune

## Final-only statistics

Runtime distribution calculations were removed. During live-stream processing the EA only updates a lightweight runtime comment. The node-vs-random logRTV statistics are computed once in `OnDeinit`.

## Warmup input

A new input seeds the live stream with closed historical bars before the test/live stream begins:

```text
InpWarmupHistoricalBars = 5000
```

Warmup bars are used to reconstruct old structural nodes and their consumed/live state. The research sample is filtered by `analysis_start`, which is set to the first newly appended bar after warmup, so final reports include only events whose `entry_time >= analysis_start`.

This allows old nodes to be available for touches inside the test period without contaminating the report with pre-test events.

## Random baseline fairness

Random reference entries are also restricted to the same analysis period, while their before-window can use warmup bars when needed. This keeps the random baseline aligned with the node sample.

## Removed dead MQL files

The following old MQL files were not used by the main EA and were removed:

```text
mql5/Include/DecisionAlphaLab/M0001/DAL_M0001RtvDistribution.mqh
mql5/Include/DecisionAlphaLab/Research/DAL_ExperimentConfig.mqh
mql5/Include/DecisionAlphaLab/Research/DAL_ValidationJournal.mqh
mql5/Scripts/DecisionAlphaLab/M0001/M0001_ExportValidationJournal.mq5
```

## Version

`M0001_LiveVisualLab.mq5` version: `1.56`.
