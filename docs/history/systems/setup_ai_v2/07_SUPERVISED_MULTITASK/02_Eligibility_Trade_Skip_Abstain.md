---
title: Eligibility, Trade, Skip and Abstain
status: canonical
version: 2.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v2
- core-production
---

# Purpose

Estimate whether any treatment is worth considering while preserving skip and abstain as economically measured actions.

## Capability tier

**Core Production**

## System design

### Eligibility target

Defined at occurrence level using the best admissible treatment only inside training roles, with nested estimation to avoid optimistic labels.

### Selective decision

Trade is allowed only when lower-bound utility clears profile and risk thresholds.

### Skip economics

Skipped opportunities retain opportunity cost and avoided-loss attribution.

### Abstention distinction

Abstain means insufficient support or knowledge; skip means supported evidence favors no trade.

## Input contracts

- `OccurrenceFeatures`
- `CandidateSummary`
- `SupportFeatures`

## Output contracts

- `EligibilityProbability`
- `TradeSkipDecision`
- `AbstentionReason`

## Measurement framework

- Selective risk.
- Coverage.
- Avoided loss.
- Missed utility.
- Calibration by context and regime.

## Adversarial questions

- Is the eligibility label built using final-test treatment outcomes?
- Does coverage collapse to inflate accuracy?
- Are skip and abstain conflated?

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

- [[Conformal_Risk_Control]]
