# VAL0011 — Main Atomic No-Sample Unification

Purpose: make the main H4 and H5 experts use live-style atomic raw-event reports by default.

Expected main report evidence:

```text
sampleCalls=0
branchSamplesBuilt=0
m0002Calls=0
sequenceOrder=known_time_batch_sequence
sameKnownTimeEventsAreSimultaneous=1
```

H4 official lines:

```text
DAL_M0004_MAIN_ATOMIC_SANITY
DAL_D0010_AUDIT
DAL_D0010_ATOMIC_TRANSITION
```

H5 official lines:

```text
DAL_M0005_MAIN_ATOMIC_SANITY
DAL_D0009_AUDIT
DAL_D0009_SUMMARY_REVERSAL
DAL_D0009_SUMMARY_CONTINUATION
```

Legacy sample/path reports are opt-in only through `InpPrintLegacySampleReport=true`.
