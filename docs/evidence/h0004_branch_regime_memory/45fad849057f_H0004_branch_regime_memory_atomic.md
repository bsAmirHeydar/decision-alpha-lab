---
id: H0004
status: active_rebuilt
family: regime_memory
official_contract: atomic_no_sample_known_time_batches
created: 2026-06-20
owner: Decision Alpha Lab
priority: critical
---

# H0004 — Branch Regime Memory

## Research question

Do reversal and continuation branch regimes display persistence beyond random ordering when measured by the time at which the regime became knowable?

---

## Old formulation

The classic formulation used M0002 branch samples and sorted completed labels into a chronological sequence. This was useful for exploration, but it had a serious live-validity risk: several labels could become known on the same candle and still be ordered as if one came before another.

---

## Current formulation

The official H0004 formulation is atomic and no-sample:

1. replay closed candles,
2. build structural nodes and raw M0001 events from the prefix,
3. collect events that become knowable at the current candle/time,
4. group them into one known-time batch,
5. classify the batch as reversal, continuation, or ambiguous,
6. compute transitions only between different known-time batches.

---

## Null hypothesis

After enforcing known-time batching, reversal and continuation labels do not persist beyond what is expected from random label order under appropriate null models.

---

## Alternative hypothesis

After enforcing known-time batching, reversal and continuation labels still display measurable persistence, clustering, and run length beyond random label order.

---

## Key failure mode addressed

If several highs/lows become confirmed or resolved on the same candle, they must not be counted as a sequence.

Same known time means simultaneous.

---

## Evidence required

A valid H0004 report must include:

- sample calls = 0 for official no-sample mode,
- M0002 calls = 0 for official no-sample mode,
- known-time batch count,
- ambiguous batch count,
- same-time event count,
- transition matrix over pure batches,
- run statistics over pure batches,
- permutation stress,
- run shuffle stress,
- optional stratified permutation.

---

## Interpretation

A positive H0004 result does not yet mean an execution edge exists. It means that market state has memory. H0005 and execution EAs must test whether that memory creates usable directional decisions.
