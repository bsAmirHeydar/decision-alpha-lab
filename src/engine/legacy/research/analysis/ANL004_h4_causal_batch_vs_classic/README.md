# ANL004 — H4 Classic vs Causal Batch Analysis

## Question

How much did same-candle fake sequencing inflate H0004 regime memory?

---

## Key finding

Causal batching reduced the reported memory but did not eliminate it.

Classic sequence:

- samePct: 72.82%,
- sameLift: 19.80 percentage points,
- lag1Corr: 0.4214.

Causal known-candle pure batches:

- samePct: 65.61%,
- sameLift: 11.98 percentage points,
- lag1Corr: 0.2584.

---

## Interpretation

The old report was too optimistic, but not entirely fake. Roughly speaking, part of the effect was sequencing artifact, and part remained after removing same-time ambiguity.

---

## Research decision

Classic H4 should remain as a historical/debug reference only. Official H4 claims should use atomic no-sample known-time batches.
