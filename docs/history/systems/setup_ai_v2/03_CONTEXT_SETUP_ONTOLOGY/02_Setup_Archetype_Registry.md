---
title: Setup Archetype Registry
status: canonical
version: 2.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v2
- core-production
---

# Purpose

Create a controlled vocabulary of exploitation hypotheses without hard-coding one strategy per context.

## Capability tier

**Core Production**

## System design

### Hypothesis family

Continuation, reversal, pullback, breakout, reclaim, retest, mean reversion, liquidity rejection, trend participation.

### Eligibility predicate

Context and view conditions required before candidate generation.

### Incompatibility predicate

Conditions that make the archetype structurally meaningless or economically impossible.

### Falsification contract

Observable evidence that would invalidate the archetype independently of P&L.

## Input contracts

- `ContextSpecification`
- `ViewSnapshot`
- `ArchetypeVersion`

## Output contracts

- `EligibleArchetypes`
- `FalsificationRecord`
- `CompatibilityEdges`

## Measurement framework

- Coverage by context family.
- Candidate survival through compatibility compilation.
- Falsification frequency and stability.

## Adversarial questions

- Is the archetype just a renamed outcome bucket?
- Were rules changed after seeing results?
- Does it add information beyond the context itself?

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

- [[Treatment_Lattice_Compiler]]
