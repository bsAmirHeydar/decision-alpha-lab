---
title: Entry Mechanism Registry
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v4
- core-production
---

# Purpose

Model breakout, market, and pullback-limit entries as different premiums paid for confirmation, immediacy, or price improvement.

## Capability tier

**Core Production**

## System design

### E1 Breakout / with-move

Buys confirmation; pays worse price, false-break risk, spread expansion, and slippage.

### E2 Immediate market

Buys immediacy and fill certainty; pays lack of price improvement and immediate adverse excursion.

### E3 Pullback / counter-move limit

Buys better geometry; pays non-fill, adverse selection, expiry, and missed-opportunity risk.

### Extended mechanisms

Reclaim, retest, staggered, and hybrid entries are typed submechanisms, not ad hoc rules.

## Input contracts

- `EntryMechanismVersion`
- `BrokerMicrostructureProfile`
- `ContextExpiry`

## Output contracts

- `EntryCandidate`
- `FillModelRequest`
- `EntryEconomics`

## Measurement framework

- Trigger probability.
- Fill probability before expiry.
- Conditional and unconditional utility.
- Adverse-selection and missed-opportunity cost.

## Adversarial questions

- Is non-fill treated as missing instead of an outcome?
- Are stop entries simulated with unrealistic fills?
- Does market entry assume mid-price?

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

- [[Fill_Hazard_And_Adverse_Selection]]
