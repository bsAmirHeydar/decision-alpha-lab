# Main Atomic No-Sample Unification for H4/H5

This release moves the no-sample / live-style contract into the main M0004 and M0005 experts.

## Contract

The main reports now default to atomic raw M0001 event replay:

- no `DALM0002BranchSample` sequence is built by the official main report path
- no M0002 branch-sample collector is called by the official main report path
- regime order is based on the candle/time at which raw M0001 events become knowable
- raw events known on the same candle are treated as simultaneous
- mixed reversal/continuation batches are marked ambiguous and skipped from transition/path statistics by default

## M0004

`M0004_BranchRegimeClustering.mq5` now calls `DAL_M0004RunAtomicNoSampleReport()` by default.

Official audit line:

```text
DAL_M0004_MAIN_ATOMIC_SANITY
DAL_D0010_AUDIT
DAL_D0010_ATOMIC_TRANSITION
DAL_D0010_ATOMIC_RUNS
DAL_D0010_ATOMIC_PERM_STRESS
```

The legacy sample-based report remains available only if explicitly enabled:

```text
InpPrintLegacySampleReport = true
```

Default is false.

## M0005

`M0005_DirectionalMemory.mq5` now calls `DAL_M0005RunAtomicNoSampleReplay()` by default.

Official audit lines:

```text
DAL_M0005_MAIN_ATOMIC_SANITY
DAL_D0009_AUDIT
DAL_D0009_SUMMARY_ALL
DAL_D0009_SUMMARY_REVERSAL
DAL_D0009_SUMMARY_CONTINUATION
```

Continuation R is explicit in the main expert and defaults to ATR risk:

```text
InpH5AtomicContinuationRisk = DAL_D0009_CONT_RISK_ATR
InpH5AtomicAtrPeriod = 14
InpH5AtomicAtrMultiplier = 4.0
```

The old structural path report remains available only if explicitly enabled:

```text
InpPrintLegacySampleReport = true
```

Default is false.

## Why

The old reports could create fake regime sequencing when multiple highs/lows became knowable on the same candle. The atomic path removes this by grouping same-known-time events into one batch before calculating transitions or replaying H5 candidates.
