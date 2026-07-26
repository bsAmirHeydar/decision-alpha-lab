---
title: Statistical Adversary Agent
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v4
- core-production
---

# Purpose

Act as an independent red team whose objective is to falsify the candidate and expose selection risk.

## Capability tier

**Core Production**

## System design

### Challenges

Dependence, multiplicity, nulls, placebos, stability, subgroup failures, causal assumptions, and prospective deviations.

### Independence

Uses separate prompts, evidence views, and task identity from the producing agents.

### Counter-report

Produces strongest rejection case, unresolved assumptions, and evidence downgrade.

### Authority

May block or request extension; cannot promote.

## Input contracts

- `CandidateEvidence`
- `TrialLedger`
- `DataRoleMap`

## Output contracts

- `AdversarialReport`
- `BlockingIssues`
- `RequiredTests`

## Measurement framework

- Issue discovery.
- Challenge reproducibility.
- Resolution quality.
- False-confidence reduction.

## Adversarial questions

- Does the adversary share the same model blind spots?
- Are challenge budgets weaker than search budgets?
- Can issues be dismissed without signed resolution?

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

- [[Anti_Overfit_Master_Protocol]]
