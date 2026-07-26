---
title: Causal Identification and Assumptions
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v3
- core-production
---

# Purpose

Distinguish counterfactual simulation, predictive ranking, and causal treatment-effect claims, and require explicit identification assumptions for each.

## Capability tier

**Core Production**

## System design

### Potential outcomes

Each treatment has a potential executable outcome under a declared market path and simulator; observed policy data reveals only selected treatments.

### Identification routes

Randomized historical choice, natural experiments, rich unconfoundedness assumptions, instrumental variables, or simulator-based structural assumptions.

### Support and overlap

Treatment effects are not extrapolated where assignment support is absent.

### Sensitivity analysis

Unmeasured confounding, simulator error, and hidden policy selection are quantified rather than ignored.

## Input contracts

- `TreatmentAssignmentHistory`
- `Covariates`
- `OutcomeCube`
- `IdentificationDeclaration`

## Output contracts

- `CausalAssumptionCard`
- `OverlapReport`
- `SensitivityReport`

## Measurement framework

- Overlap diagnostics.
- Covariate balance.
- Sensitivity bounds.
- Agreement between predictive and causal rankings.

## Adversarial questions

- Is a replayed counterfactual being called causal truth?
- Are historical human selections confounded by unrecorded judgment?
- Does positivity fail for rare treatments?

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

- [[Doubly_Robust_And_Orthogonal_Learners]]
