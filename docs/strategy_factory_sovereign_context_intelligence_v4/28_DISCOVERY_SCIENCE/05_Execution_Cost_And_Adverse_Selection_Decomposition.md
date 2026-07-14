---
title: Execution Cost and Adverse-Selection Decomposition
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: core-production
tags:
  - saed-v4
---

# Mission

Decompose apparent setup edge into directional information, price improvement, fill selection, spread, slippage, impact, financing, and missed-opportunity components.

## Why this component exists

- None declared.

## Authority and safety boundary

- This component may estimate, rank, simulate, challenge, or recommend only inside a declared research scope.
- It cannot create canonical Context truth, modify protected evidence roles, sign promotion, change portfolio risk, activate runtime generations, access live credentials, or place orders.
- Unsupported, stale, contradictory, OOD, hash-mismatched, uncalibrated, or incomplete paths resolve to **Skip**, **Abstain**, **Manual fallback**, **Reject**, or **Quarantine**.
- Every result is subordinate to UCEE I12 promotion admission, I13 authority/fallback, I14 immutable runtime, I17 portfolio/risk, and I18 release qualification.

## Input contracts

- Outcome cube.
- Quote/trade path.
- Order and fill states.

## Output contracts

- Per-treatment economic attribution.
- Cost sensitivity surface.

## Algorithmic design

- Estimate market, limit, and breakout entry premiums separately.
- For limits, model fill probability and outcome conditional on fill.
- Separate mechanical spread from adverse selection and timing decay.
- Estimate utility across size using impact and capacity curves.

## Formal objective and constraints

```text
EU_limit = P(fill)*E[U|fill] + P(no_fill)*U_missed - costs - adverse_selection
```

## Data and known-time semantics

- None declared.

## Anti-overfit and model-risk controls

- Costs frozen before protected evaluation.
- No zero-cost headline metric.
- Vendor/broker transport uses conservative profile.

## Measurement system

- Net/gross edge ratio.
- Adverse-selection share.
- Fill-adjusted utility.
- Capacity-adjusted utility.
- Cost break-even.

## Scalability and operating model

- None declared.

## Adversarial failure modes

- High limit performance caused by selective fills.
- Market impact ignored.
- One broker profile presented universal.

## UCEE integration

- None declared.

## Required tests and evidence

- Cost multiples.
- Missed fill.
- Delayed fill.
- Broker profile swap.
- Size ramp.

## Implementation slices

- None declared.

## Decision record

- None declared.

## Acceptance gate

The component is accepted only when its contracts are closed and versioned, all lineage and role boundaries are reconstructible, protected evaluation remains unexposed, negative and mutation tests pass, simpler baselines remain available, and an independent reviewer can reproduce the decision-equivalent result from immutable hashes.

## Related notes

- [[Market_Microstructure_Fill_Impact_Model]]
- [[Broker_And_Feed_Transport_Lab]]
