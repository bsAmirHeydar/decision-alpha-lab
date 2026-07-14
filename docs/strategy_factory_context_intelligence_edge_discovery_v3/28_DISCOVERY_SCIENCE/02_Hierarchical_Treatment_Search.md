---
title: Hierarchical Treatment Search
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: core-production
tags:
  - saed-v3
---

# Mission

Search the treatment lattice in stages so entry, payoff, stop, exit, and management effects are identified without an uncontrolled Cartesian explosion.

## Why this component exists

- None declared.

## Authority and safety boundary

- This component may estimate, rank, simulate, challenge, or recommend only inside a declared research scope.
- It cannot create canonical Context truth, modify protected evidence roles, sign promotion, change portfolio risk, activate runtime generations, access live credentials, or place orders.
- Unsupported, stale, contradictory, OOD, hash-mismatched, uncalibrated, or incomplete paths resolve to **Skip**, **Abstain**, **Manual fallback**, **Reject**, or **Quarantine**.
- Every result is subordinate to UCEE I12 promotion admission, I13 authority/fallback, I14 immutable runtime, I17 portfolio/risk, and I18 release qualification.

## Input contracts

- Frozen treatment lattice.
- Search hierarchy.
- Stage budgets.

## Output contracts

- Stage-wise shortlist.
- Search path ledger.
- Joint finalist set.

## Algorithmic design

- Stage 1 tests Context eligibility and simple fixed treatments.
- Stage 2 compares entry mechanisms within payoff profiles.
- Stage 3 compares stop geometry for supported entries.
- Stage 4 compares fixed versus path-dependent exits.
- Stage 5 performs bounded joint search on shortlisted candidates.
- Use multi-fidelity evaluation and early rejection, not optimistic pruning.


## Data and known-time semantics

- None declared.

## Anti-overfit and model-risk controls

- All stages and budgets predeclared.
- Pruned candidates remain in multiplicity universe.
- Shortlist thresholds selected inside inner validation only.

## Measurement system

- Search compression ratio.
- False prune rate.
- Stage stability.
- Compute per finalist.

## Scalability and operating model

- None declared.

## Adversarial failure modes

- Winner from early noisy estimate monopolizes budget.
- Stage order chosen after results.
- Pruned failures omitted.

## UCEE integration

- None declared.

## Required tests and evidence

- Stage-order permutation.
- Budget sensitivity.
- No-prune benchmark.
- Shortlist reproducibility.

## Implementation slices

- None declared.

## Decision record

- None declared.

## Acceptance gate

The component is accepted only when its contracts are closed and versioned, all lineage and role boundaries are reconstructible, protected evaluation remains unexposed, negative and mutation tests pass, simpler baselines remain available, and an independent reviewer can reproduce the decision-equivalent result from immutable hashes.

## Related notes

- [[Treatment_DSL_And_Constraint_Solver]]
- [[Multi_Fidelity_Experiment_Scheduling]]
