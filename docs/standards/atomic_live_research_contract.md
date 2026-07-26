# Atomic Live Research Contract

This document defines the strict contract used to prevent future leakage, fake sequencing, and non-tradable R statistics.

---

## 1. Decision-time contract

For every decision candle `t`, the engine may only use information derived from closed candles up to `t`.

Forbidden:

- using future-completed branch samples to decide at `t`,
- using a future outcome label before its known candle,
- ordering labels inside the same known candle,
- exiting on a regime change before that regime change is knowable.

Required fields for any live-valid label:

- `known_index`,
- `known_time`,
- `source_event_id` or equivalent raw event reference,
- `energy_label`: reversal, continuation, or ambiguous,
- `direction_label` where applicable,
- `is_ambiguous`.

---

## 2. Same-candle batch contract

All events or labels that become known on the same candle/time form one batch.

A batch can be:

- pure reversal,
- pure continuation,
- ambiguous mixed energy,
- unknown or invalid.

A pure batch may participate in regime transitions. An ambiguous batch must not create a fake transition. It can be reported, counted, and studied, but it cannot be converted into an ordered sequence such as `REVERSAL -> CONTINUATION` if both labels were known at the same time.

---

## 3. No-sample contract

A strict validator or main report must not build `M0002BranchSample` objects when its goal is live regime inference.

Allowed source objects:

- bars,
- structural nodes,
- raw M0001 events,
- live-known event states.

Forbidden source objects for official live claims:

- completed branch samples,
- outcome-sorted sample arrays,
- sample IDs as tie-breaks for regime order,
- branch sample entry/outcome order as a proxy for time.

---

## 4. Entry contract

A candidate can only become eligible after the regime is knowable.

For reversal:

- candidate is a live-visible structural zone,
- entry occurs on later zone touch,
- measurement starts after the touch/fill.

For continuation:

- candidate is a live-visible structural break opportunity,
- entry occurs on later close-break or intrabar-break depending on explicit policy,
- measurement starts after the break entry.

---

## 5. R contract

An R multiple is tradable only when the denominator is a real initial risk.

Valid risk denominators:

- zone-edge stop,
- ATR stop,
- structural invalidation stop,
- explicitly modeled broker stop,
- another documented and executable risk rule.

Invalid as trading R:

- structural path denominator if no stop is actually used,
- regime-change distance after the fact,
- future target distance not known at entry,
- MFE/MAE scaling that was never used as risk.

A report may still print path-normalized R, but it must label it as `STRUCTURAL_PATH_R`, not `TRADABLE_R`.

---

## 6. Report contract

Every report must declare:

- source mode: classic sample, causal sample-batch, or atomic no-sample,
- decision contract,
- entry contract,
- exit contract,
- risk contract,
- same-candle policy,
- ambiguity policy,
- random baseline design.

If these are not declared, the report is exploratory only.
