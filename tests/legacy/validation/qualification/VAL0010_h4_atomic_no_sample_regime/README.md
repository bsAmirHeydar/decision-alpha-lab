# VAL0010 — H4 Atomic No-Sample Regime Validation

## Purpose

Validate H0004 without using M0002 branch samples.

---

## Contract

```text
No M0002 samples.
No sample sorting.
No fake same-candle transitions.
Raw M0001 events only.
Known-time batches only.
Ambiguous mixed-energy batches are skipped from transition/run stats by default.
```

---

## Main expected log lines

```text
DAL_D0010_AUDIT
DAL_D0010_ATOMIC_TRANSITION
DAL_D0010_ATOMIC_RUNS
DAL_D0010_ATOMIC_PERM_STRESS
```

---

## Required audit fields

```text
sampleCalls=0
branchSamplesBuilt=0
m0002Calls=0
contract=no_m0002_no_branch_samples_raw_m0001_events_only
sequenceOrder=known_time_batch_sequence
sameKnownTimeEventsAreSimultaneous=1
mixedEnergyBatchPolicy=ambiguous_skip_from_transition
```

---

## Interpretation

If D0010 still shows positive same-lift, lag-1 correlation, and run persistence after this contract, H0004 becomes much stronger than the old classic report.

If the effect disappears, the old regime memory was mostly an artifact of completed-sample sequencing.
