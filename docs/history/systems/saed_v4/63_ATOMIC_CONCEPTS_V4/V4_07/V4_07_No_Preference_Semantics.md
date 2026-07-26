---
title: No Preference Semantics
phase: V4-07
status: implemented
version: 1.0.0
created: '2026-07-15'
updated: '2026-07-15'
tags: [saed-v4, v4-07, atomic-concept]
---

# No Preference Semantics

## Definition

No Preference Semantics is an atomic SAED V4-07 concept used by the deterministic bounded constraint solver and action lattice. Its meaning is fixed by [[00_MOC_V4_07_Constraint_Solver_And_Action_Lattice]] and cannot be widened by an adapter, model, runtime or operator convenience.

## Identity

The concept is represented by a closed contract, exact version and canonical content hash. Identity-affecting fields are serialized in sorted canonical JSON. Missing fields, unknown fields, unstable randomness and mutable external state are prohibited.

## Allowed use

The concept may support finite candidate construction, structural feasibility, audit, replay, diff, partitioning or the bounded [[57_V4_08_Outcome_Cube_Handoff]]. It may not imply treatment preference, expected value, model score, position size, capital allocation, runtime activation or order placement.

## Known-time rule

Only information available at or before the declared `known_as_of` boundary may be attached. Feature predicates that require path evaluation remain deferred. Future suffixes, realized outcomes and post-decision labels are rejected rather than masked.

## Failure rule

Any identity mismatch, unsupported value, missing lineage, budget overflow or authority leak causes fail-closed rejection and quarantine. No default executable action is synthesized. Skip and Abstain remain available only as explicit non-executing fallback nodes.

## Verification

The corresponding Python implementation is covered by golden, negative, mutation and deterministic replay tests. The MQL5 representation is diagnostic-only and cannot trade. Review the evidence in [[62_Test_Evidence]] and limitations in [[56_Limitations_And_Residual_Risk]].

## Related concepts

- [[V4_07_Bounded_Candidate]]
- [[V4_07_Action_Node]]
- [[V4_07_Action_Lattice_DAG]]
- [[V4_07_Lattice_Integrity_Receipt]]
- [[V4_07_V4_08_Handoff]]
