# Article — Structural Regime Memory Without Samples

## Abstract

A central question of Decision Alpha Lab is whether structural market regimes have memory. Early reports suggested that reversal and continuation labels cluster: a reversal label is more likely to be followed by another reversal, and a continuation label is more likely to be followed by another continuation.

A key flaw was then identified: several labels may become knowable on the same candle. If those labels are sorted into a sequence, the report can create transitions that never existed in live time.

This article documents the move from sample sequencing to atomic known-time regime batching.

---

## The problem with sample order

Branch samples are convenient. They compress a market event into one object with entry, exit, outcome, and label fields.

The problem is that the sample is only complete after the event has already resolved. Sorting completed samples by outcome or entry may be useful for retrospective analysis, but it is not automatically a live-valid regime sequence.

A sample sequence can answer:

> In what order did completed labels appear inside the report array?

It cannot necessarily answer:

> What was the latest regime known to the trader before the next entry?

---

## The same-candle sequencing flaw

Suppose two labels become knowable at the close of the same candle:

- label A: reversal,
- label B: continuation.

A classic sort must choose an order. It may use entry index, outcome index, or ID. But any order is artificial because the trader receives both labels at the same time.

The correct representation is not a transition. It is an ambiguous batch.

---

## Atomic known-time batches

The atomic method replaces sample order with known-time batches.

For every closed candle:

1. collect raw events that become knowable on that candle,
2. group them into one batch,
3. classify the batch as pure reversal, pure continuation, or ambiguous,
4. compute transitions only between separate known-time batches,
5. skip ambiguous batches from transition and run statistics unless explicitly studying ambiguity.

This removes fake same-candle transitions.

---

## Why this matters

Regime memory is an especially sensitive claim because its entire meaning depends on order.

If the order is fake, the memory is fake.

If the order is causal and the memory remains, the result is much more valuable.

---

## The current standard

For H0004, the official standard is:

- no M0002 sample construction for live claims,
- raw M0001 event replay,
- known-time batch ordering,
- simultaneous same-time events,
- ambiguous batch skipping by default,
- permutation and run-shuffle stress tests on the batch sequence.

This is the difference between a descriptive label sequence and a live-valid regime memory test.
