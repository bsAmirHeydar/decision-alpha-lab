# H4 Fast Atomic Main Report

M0004 build 1.07 keeps the official no-sample contract but removes the heavy strict prefix replay from the default main report path.

## Why this was needed

The first atomic no-sample implementation was intentionally strict: for every replay candle it rebuilt the prefix bars, structural nodes, and M0001 events. That is useful as a validator, but it is too heavy for normal reporting because the work grows roughly with `bars * rebuild_cost`.

## New default

The main expert now defaults to:

```text
InpAtomicReportMode = DAL_M0004_ATOMIC_FAST_RAW_EVENT_BATCH
InpAtomicPermutationIterations = 100
InpAtomicWriteCsv = false
```

This mode runs M0001 once on the final closed-bar stream, classifies raw M0001 events by their knowable candle, groups all events with the same `known_time` into one simultaneous batch, and computes transitions only between different known-time batches.

It still does not build M0002 branch samples and it still does not treat same-candle regimes as sequential.

## Strict mode

For small debugging runs only:

```text
InpAtomicReportMode = DAL_M0004_ATOMIC_STRICT_PREFIX_REPLAY
```

Strict mode keeps the old prefix-by-prefix validator behavior and may be slow on large histories.


## Compile sync note (release 1.01)

The main EA now exposes `InpAtomicReportMode` as an integer input (`0=FAST_RAW_EVENT_BATCH`, `1=STRICT_PREFIX_REPLAY`) while the internal config still uses the enum. This avoids MetaEditor input-type errors when the terminal-level Include tree is stale. The installer also syncs `DAL_M0004AtomicNoSample.mqh` into every local MetaQuotes terminal include directory.
