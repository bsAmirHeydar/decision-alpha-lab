---
title: Atomic Parameter Edges
phase: V4-07
status: implemented
version: 1.0.0
created: '2026-07-15'
updated: '2026-07-15'
tags: [saed-v4, v4-07, action-lattice, implementation]
---

# Atomic Parameter Edges

## Purpose

Atomic Parameter Edges defines the institutional implementation boundary for SAED V4-07. The phase converts the finite exact-versioned Treatment DSL from [[V4_06_Bounded_V4_07_Handoff]] into a deterministic, fully accounted structural action lattice suitable for the downstream [[V4_08_Executable_Path_Outcome_Cube]].

## Design decision

The implementation uses explicit finite parameter domains, Cartesian candidate enumeration under hard budgets, frozen constraint evaluation, deterministic pruning, content-addressed feasible nodes, adjacent one-parameter edges and mandatory fail-closed fallback edges. Structural monotonic order is used only to make adjacency deterministic; it is never interpreted as economic superiority.

## Contract

This capability is additive and consumes only immutable V4-06 package and handoff identities. Every accepted object is exact-versioned, content-addressed, deterministic under canonical serialization and rejected when an unknown field, unsupported operator, stale lineage, prohibited identifier, authority leak or budget breach is detected.

## Invariants

- Candidate enumeration is finite before solving begins.
- Skip and Abstain remain first-class, non-executing actions.
- Constraint evaluation uses only frozen declarative structure and known-time-safe references.
- Deferred feature predicates are carried forward; they are never guessed, backfilled or converted into feasibility from future information.
- Lattice edges encode adjacency or fallback only. They do not encode preference, expected return, probability, model score, capital allocation or execution permission.
- Complete exposure accounting covers feasible and pruned candidates.
- Python is the deterministic reference implementation; MQL5 remains a diagnostic mirror until actual MetaEditor evidence exists.

## Failure behavior

The implementation fails closed. It raises a typed contract, domain, constraint, budget or integrity error and emits no partial executable artifact. No nearest-value substitution, domain widening, silent constraint drop, dynamic code loading, network lookup, outcome-based ranking or trading fallback is permitted.

## Verification

Verification combines closed JSON-schema validation, exact golden reproduction, negative and mutation tests, authority-boundary AST scanning, deterministic replay, hash-ledger validation, Obsidian-link validation and diagnostic-only MQL5 static checks. External reproduction, MetaEditor compilation and production authorization remain explicitly pending.

## Operations

Operators first verify V4-06 package and handoff hashes, then validate the V4-07 policy, domain registry and solver request. The solver must complete inside deterministic count budgets. Any mismatch quarantines the request. Rollback removes the indexed patch files and restores the previous pyproject and commit message from version control.

## Evidence classification

The accepted claim is limited to a reference implementation of bounded structural solving and lattice construction. It is not evidence of real alpha, prospective performance, treatment value, policy quality, broker parity, runtime parity or live readiness.

## Review questions

1. Is every input identity immutable and hash verified?
2. Can any candidate be generated outside the approved domain registry?
3. Are all pruned candidates represented in the exposure and pruning ledgers?
4. Can any edge be misconstrued as a score, recommendation or order instruction?
5. Are external, MetaEditor and production claims still separated from static evidence?

## Navigation

- Phase map: [[00_MOC_V4_07_Constraint_Solver_And_Action_Lattice]]
- Previous: [[24_Action_Node_Contract]]
- Next: [[26_Fallback_Edges]]
