# VAL0010 — H4 Atomic No-Sample Regime Replay

Purpose: validate H0004 regime clustering without branch samples and without fake same-candle sequences.

## Validation rule

A regime label becomes usable only at its `known_time`. All raw M0001 events that become known on that same candle are simultaneous. They cannot be interpreted as a sequence.

## Pass/fail focus

Use D0010 output:

- `sampleCalls=0`
- `branchSamplesBuilt=0`
- `m0002Calls=0`
- `sameKnownTimeEventsAreSimultaneous=1`
- `ambiguousBatches`
- `sameTimeBatchCount`
- `DAL_D0010_ATOMIC_TRANSITION`
- `DAL_D0010_ATOMIC_PERM_STRESS`

If same-time batches are frequent, old sample-sequence H4 reports were materially affected by fake sequencing. The D0010 transition matrix should be used instead.
