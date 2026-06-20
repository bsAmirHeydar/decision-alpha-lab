# D0010 — H4 Atomic No-Sample Regime Audit

D0010 is the strict live-style validator for H0004 regime memory.

It removes M0002 branch samples from the H4 validation path:

- no `DALM0002BranchSample`
- no `DAL_M0002CollectBranchSamples`
- no outcome-sorted sample sequence
- no artificial sequencing of regimes that become knowable on the same candle

## Contract

At each replay step, D0010 uses only closed bars available up to that candle:

1. Build confirmed structural nodes from the prefix.
2. Build raw M0001 events from the prefix.
3. Classify only raw events whose `known_index` equals the current decision candle.
4. Treat all events with the same `known_time` as one simultaneous batch.
5. If a batch contains both reversal and continuation labels, mark it ambiguous and skip it from transition/run statistics by default.
6. Compute transition and run memory only between pure batches with different known times.

## Important output lines

- `DAL_D0010_AUDIT`
- `DAL_D0010_ATOMIC_TRANSITION`
- `DAL_D0010_ATOMIC_RUNS`
- `DAL_D0010_ATOMIC_PERM_STRESS`

The audit line must show:

```text
sampleCalls=0
branchSamplesBuilt=0
m0002Calls=0
contract=no_m0002_no_branch_samples_raw_m0001_events_only
sameKnownTimeEventsAreSimultaneous=1
```

## Interpretation

This report is the no-sample H4 regime-memory report. It should be preferred over classic M0004 sample-sequence output when evaluating live-valid regime inertia.

Classic M0004 can still be useful as a historical research report, but D0010 is the stricter contract for live causality.
