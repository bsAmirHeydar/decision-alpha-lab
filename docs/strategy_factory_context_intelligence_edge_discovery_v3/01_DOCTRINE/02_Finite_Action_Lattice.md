---
title: Finite Action Lattice
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v3
- doctrine
---

# Thesis

Advanced AI is allowed to reason deeply only inside a compiler-approved finite action lattice; open-ended action invention is prohibited at decision time.

## Architectural design

### Candidate lattice

A treatment is a typed composition of payoff profile, entry mechanism, trigger, stop, exit, trail, management, expiry, and risk-eligibility atoms.

### Compatibility compiler

Static rules remove nonsensical or unsupported combinations before any model sees them.

### Versioned expansion

New atoms enter through an ADR, counterfactual replay support, economics support, MQL5 feasibility, and a new universe version.

## Machine contracts

- `treatment_universe_id`
- `treatment_candidate_id`
- `compatibility_reason`
- `runtime_feasibility`
- `dominance_status`

## Validation and evidence

- Every selected action belongs to the signed universe.
- The Skip action is always present.
- Candidate count and search budget are declared before final-test access.

## Failure modes and mandatory response

- **Dynamic action invention:** Hard reject the model output.
- **Unsupported atom combination:** Compiler error; candidate never enters training.
- **Universe mutation during a tournament:** Invalidate the tournament and restart under a new version.

## UCEE handoff

All outputs bind to exact upstream context, feature, data-role, treatment-universe, and economics hashes. Promotion and runtime authority remain in UCEE I12–I18.

## Related notes

- [[Treatment_Lattice_Compiler]]
- [[Capability_Tier_Policy]]
