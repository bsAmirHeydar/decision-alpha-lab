---
title: Fill Hazard and Adverse Selection
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v4
- core-production
---

# Purpose

Model entry feasibility and the economic information carried by being filled, not merely outcomes conditional on ideal execution.

## Capability tier

**Core Production**

## System design

### Competing events

Fill, context expiry, cancellation, breakout-away, adverse move, and session close are competing risks.

### Conditional outcome

Outcome after fill is modelled separately from fill probability and time to fill.

### Adverse selection

Limit fills are compared with matched non-fill opportunities and local path state to quantify whether fills occur when the thesis is deteriorating.

### Opportunity cost

Missed high-quality moves and capital reservation time enter utility.

## Input contracts

- `EntryCandidate`
- `QuotePath`
- `ExpiryPolicy`
- `QueueAssumption`

## Output contracts

- `FillOutcome`
- `FillHazardModelTarget`
- `AdverseSelectionReport`

## Measurement framework

- Calibration of fill probability.
- Time-to-fill concordance.
- Conditional versus unconditional utility.
- Adverse-selection premium.

## Adversarial questions

- Are non-fills dropped?
- Is touch treated as guaranteed fill?
- Does the model use post-fill information in the fill head?

## Mandatory controls

1. Exact upstream hashes and data roles are recorded.
2. Candidate and failure ledgers are complete.
3. Costs, capacity, missingness, censoring, and support are explicit.
4. Validation uses chronological, cluster-aware, purged folds.
5. Advanced outputs cannot bypass manual policy, hard risk, portfolio, or UCEE promotion.
6. Any runtime handoff requires deterministic export, parity, latency, fallback, and revocation evidence.

## Acceptance boundary

Passing research metrics is necessary but never sufficient. The component remains non-authoritative until its evidence is admitted through UCEE I12, compiled by I14, challenged prospectively under I15, bounded by I17, and qualified under I18.

## Related notes

- [[Survival_And_Competing_Risks]]
