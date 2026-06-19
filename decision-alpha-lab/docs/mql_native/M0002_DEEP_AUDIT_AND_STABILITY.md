# M0002 Deep Audit and Stability Suite

## Purpose

This patch hardens the second hypothesis after the H0001/H0002 logic repair.

H0002 does **not** ask whether an event hunted or touched. It asks only:

> At the candle where the exit-gap window is completed, where did the close finish relative to the original node price?

For LOW nodes:

- `close > node_price` => `REVERSAL_AFTER_EXIT`
- `close < node_price` => `CONTINUATION_AFTER_EXIT`

For HIGH nodes:

- `close < node_price` => `REVERSAL_AFTER_EXIT`
- `close > node_price` => `CONTINUATION_AFTER_EXIT`

The measured value is locked to the native M0001 event RTV:

```text
branchRTV = event.rtv
branchLog = log(event.rtv)
```

The branch is only a label. It does not move the volatility window.

## Why m0001Events can be much larger than nodes

`nodes` is the count of confirmed structural pivot nodes.

`m0001Events` is the count of completed touch -> exit-gap cycles produced from those nodes. A single node can generate many M0001 cycles because M0002 previously used a neutral builder. That path is now deprecated; v1.70 uses M0001 consumption, so a consumed node is not recycled into more H0002 events.

Random samples are not counted as `m0001Events`. `InpRandomSamplesPerEvent` only affects the matched null baseline used for each branch sample.

The audit now prints:

- `uniqueNodes`
- `avgPairedEventsPerNode`
- `maxRevisitId`

Use these fields to judge whether the H0002 sample is dominated by repeated cycles from the same structural nodes. The `NONOVERLAP`, `CLUSTER_ROBUST`, and `BLOCK_BOOT` reports are the formal stability checks for this risk.

## Random null engine

The old sine-fraction deterministic random fraction has been replaced with a deterministic 32-bit avalanche hash:

```text
randomEngine=hash32_v2_deterministic_uniform_entry
```

The null selection rule is still intentionally reproducible:

- uniform entry index over valid entries
- same sample length as the real event
- baseline window strictly before the random entry
- entry guarded by analysis start
- multi-sample random baseline averages logRTV across `randomK` windows

The H2 report prints `DAL_M0002_FINAL_RANDOM_ENGINE_AUDIT` so a wrong/old random engine is immediately visible.

## H2 stability suite

Each H2 branch now gets the same stability checks used in H1:

- `STRESS_NULLS` hard matched null: same UTC session, same pre-entry volatility tercile, trend first pass
- `PLACEBO` shifted entries
- `OUTLIER_STRESS` top-tail removal and winsorization
- `NONOVERLAP` dependency stress
- `CLUSTER_ROBUST` day/week cluster-level t diagnostics
- `BLOCK_BOOT` block bootstrap confidence interval
- `HORIZON` fixed-horizon decay checks
- `NEGATIVE_CONTROL` random-vs-random

These lines are printed separately for:

- `REVERSAL_AFTER_EXIT`
- `CONTINUATION_AFTER_EXIT`

The suite can be disabled with:

```text
InpRunH2StressSuite = false
```

but the default is `true` because H0002 is a research hypothesis.


## Logic repair v1.70

H0002 now uses `DAL_M0001ComputeEvents()` directly. Node consumption is preserved exactly as in H0001/M0001; no reversal/continuation calculation is created after a node has been consumed.
