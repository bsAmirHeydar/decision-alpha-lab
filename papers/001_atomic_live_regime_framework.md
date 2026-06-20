# Atomic Live Regime Framework

## Abstract

This paper describes a research framework for structural market regimes that avoids a common source of bias: completed-sample sequencing. The framework replaces sample order with raw-event known-time batches and requires every execution statistic to use an explicit risk model.

---

## 1. Motivation

Market research often produces convincing results that cannot be traded. The reason is not always overfitting. Sometimes the report answers the wrong temporal question.

A completed event sample may contain information that was not available when an entry would have been made. If this sample is later used as if it were known in real time, the report becomes subtly biased.

Decision Alpha Lab encountered this problem in regime memory and directional memory research. The solution was to move from sample-centric analysis to atomic live replay.

---

## 2. Structural events

The framework begins with structural nodes and zones. Price creates nodes, revisits them, hunts them, breaks them, and resolves them into observable events.

The aim is not to predict every candle. The aim is to detect whether structural events create measurable state.

---

## 3. Known-time ordering

The core time variable is not the event's entry, exit, or ID. The core time variable is when the event becomes knowable.

If several labels become knowable at the same time, they form one batch. There is no internal order inside that batch.

This matters because regime memory is a statement about sequence. If the sequence is fake, the memory is fake.

---

## 4. Atomic no-sample replay

Atomic replay avoids branch sample construction. At each closed candle it reconstructs only what is currently knowable:

1. bars up to the current candle,
2. confirmed structural nodes,
3. raw M0001 events,
4. newly knowable events,
5. known-time regime batch,
6. live candidates,
7. later entries and measurements.

This prevents future-completed samples from driving decisions.

---

## 5. Reversal and continuation

The framework separates reversal and continuation.

Reversal is a reaction problem. It asks whether structural zones produce tradeable bounces or rejections.

Continuation is a path problem. It asks whether structural breaks in a continuation state create enough path quality to survive explicit risk.

Combining them into one headline hides the true behavior of both.

---

## 6. R multiple discipline

An R multiple is only tradable if the denominator is a real risk.

Path-normalized R may still be useful, but it must be labeled as structural path R. It cannot be treated as a real profit factor.

This distinction was critical in H0005, where continuation path reports looked strong but did not originally use a real initial stop.

---

## 7. Validation

A valid framework should include:

- permutation stress,
- run shuffle stress,
- block order shuffle,
- stratified permutation,
- far-lag placebo,
- matched random entry baselines,
- family-level execution reports.

No single baseline is sufficient.

---

## 8. Conclusion

The atomic live regime framework makes the research harder and often reduces headline edge. That is the point. Any remaining signal is more trustworthy because it survived a stricter temporal contract.
