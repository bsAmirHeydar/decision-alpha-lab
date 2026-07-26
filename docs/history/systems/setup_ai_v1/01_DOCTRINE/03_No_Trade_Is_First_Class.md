---
id: SAED-CFDA2ABD9A
title: "No Trade, Skip, Review, and Abstention Are First-Class Actions"
type: architecture
status: canonical
domain: strategy-factory-setup-ai-edge-discovery
version: 1.0.0
created: 2026-07-13
updated: 2026-07-13
tags:
  - strategy-factory
  - setup-factory
  - ai-training
  - doctrine
  - abstention
---

# No Trade, Skip, Review, and Abstention Are First-Class Actions

## Action Taxonomy

- `SKIP_POLICY`: evidence says no candidate clears utility and safety constraints.
- `ABSTAIN_UNCERTAINTY`: the model lacks support or confidence.
- `REVIEW`: optional human review state outside automated execution.
- `FALLBACK_MANUAL`: use the frozen manual baseline.
- `FALLBACK_CONSERVATIVE`: use a simpler certified model/policy.

## Invariant

The trainer is never forced to select a trade. `Skip` appears in every candidate ranking group with declared utility, usually zero or a context-specific opportunity-cost hurdle.

## Evaluation

Report coverage, selective expectancy, false-positive cost, missed-tail cost, disagreement with manual baseline, and performance as the abstention threshold changes.

## Runtime

Unknown feature support, stale Context, missing required views, model/preprocessing mismatch, cost infeasibility and portfolio denial all produce explicit abstention/fallback reasons rather than silent defaults.
