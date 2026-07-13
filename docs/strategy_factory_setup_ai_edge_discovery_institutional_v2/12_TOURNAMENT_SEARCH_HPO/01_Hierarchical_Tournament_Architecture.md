---
title: Hierarchical Tournament Architecture
status: canonical
version: 2.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v2
- core-production
---

# Purpose

Control combinatorial search by testing semantic decisions in stages before a bounded joint tournament.

## Capability tier

**Core Production**

## System design

### Stage 1

Context eligibility and simple manual/naive baselines.

### Stage 2

Payoff profile comparison with canonical treatment atoms.

### Stage 3

Entry mechanism and trigger comparison inside each viable profile.

### Stage 4

Stop, exit, trail, and management refinement.

### Stage 5

Model-family tournament and bounded joint shortlist.

### Stage 6

Locked validation, causal challenge, and prospective paper.

## Input contracts

- `ContextProgram`
- `TreatmentUniverse`
- `SearchBudget`

## Output contracts

- `StageResults`
- `ShortlistManifest`
- `TournamentLedger`

## Measurement framework

- Candidates per stage.
- Survival rate.
- Selection regret.
- Search-adjusted performance.

## Adversarial questions

- Did early pruning remove rare convex winners unfairly?
- Did later stages reuse locked evidence?
- Is the joint shortlist declared before final evaluation?

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

- [[Search_Space_Governance]]
