---
title: Treatment DSL and Constraint Solver
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: core-production
tags:
  - saed-v3
---

# Mission

Compile a finite, valid, explainable treatment lattice from payoff, entry, trigger, stop, exit, trail, management, time, cost, and risk primitives.

## Why this component exists

- None declared.

## Authority and safety boundary

- This component may estimate, rank, simulate, challenge, or recommend only inside a declared research scope.
- It cannot create canonical Context truth, modify protected evidence roles, sign promotion, change portfolio risk, activate runtime generations, access live credentials, or place orders.
- Unsupported, stale, contradictory, OOD, hash-mismatched, uncalibrated, or incomplete paths resolve to **Skip**, **Abstain**, **Manual fallback**, **Reject**, or **Quarantine**.
- Every result is subordinate to UCEE I12 promotion admission, I13 authority/fallback, I14 immutable runtime, I17 portfolio/risk, and I18 release qualification.

## Input contracts

- Versioned primitive registries.
- Context compatibility rules.
- Broker and runtime capability profiles.

## Output contracts

- Canonical treatment IDs.
- Constraint proof or rejection reason.
- Candidate lattice hash.

## Algorithmic design

- Use a typed declarative DSL with closed enums, units, temporal predicates, geometry expressions, and capability requirements.
- Compile constraints through SAT/SMT-style validation or deterministic rule evaluation.
- Canonicalize semantically equivalent treatments.
- Generate Skip and Abstain as first-class actions.

## Formal objective and constraints

```text
treatment_id = SHA256(canonical_json(payoff, entry, trigger, stop, exit, trail, management, time, economics))
```

## Data and known-time semantics

- None declared.

## Anti-overfit and model-risk controls

- No model-generated arbitrary price or risk action.
- Candidate universe freezes before protected evaluation.
- Unsupported broker/runtime treatment rejected at compile time.

## Measurement system

- Lattice size.
- Invalid-combination rejection rate.
- Canonical deduplication.
- Runtime-compatible fraction.

## Scalability and operating model

- None declared.

## Adversarial failure modes

- Combinatorial explosion.
- Equivalent treatments counted as independent.
- Risk or volume embedded in AI output.

## UCEE integration

- None declared.

## Required tests and evidence

- Constraint mutation.
- Unit mismatch.
- Cycle in management state machine.
- Canonical identity stability.

## Implementation slices

- None declared.

## Decision record

- None declared.

## Acceptance gate

The component is accepted only when its contracts are closed and versioned, all lineage and role boundaries are reconstructible, protected evaluation remains unexposed, negative and mutation tests pass, simpler baselines remain available, and an independent reviewer can reproduce the decision-equivalent result from immutable hashes.

## Related notes

- [[Treatment_Lattice_Compiler_Algorithms]]
- [[Hierarchical_Treatment_Search]]
