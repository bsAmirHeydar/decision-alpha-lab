# NDS Hook 86.4 Cycle R1 — Exact Speed Audit

## Intent

Reduce Strategy Tester wall time at unchanged decision accuracy.

## Changed authority

No market or execution authority changed. The patch changes scheduling and evidence lookup only.

## Exactness argument

1. Existing pending orders and fixed-R positions are broker-owned and cannot be altered by rebuilding historical Hook/F graphs.
2. Opposing-F3 events only add F3-family ownership to existing Phase02 sequences. When no otherwise eligible sequence can use that ownership, constructing the F graph cannot change selection.
3. Phase03/04 cannot repair failed pre-closure gates, so processing only prequalified candidates preserves the executable set.
4. Binary lower-bound scanning returns the same first bar whose time is greater than or equal to closure time.
5. Sequence-id indexing is a hint only; full structural identity is revalidated and linear fallback remains.
6. Funnel and selection share the same eligibility predicates and ordering in one pass.

## Deliberately untouched

- central production authority defaults;
- Hook/Node/F doctrine;
- Phase04 closure math;
- entry, stop, TP and sizing;
- one-attempt registry;
- Magic ownership;
- pending cancellation and restart recovery;
- tester symbol, timeframe and tick model.

## Remaining evidence

- clean MetaEditor compile;
- MQL5 contract self-test;
- paired MT5 Strategy Tester result parity with acceleration on/off;
- measured wall-time and CPU improvement on the target Windows agent.
