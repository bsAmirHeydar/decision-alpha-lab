---
title: "ADR — Budgets Fail Closed"
status: accepted
date: 2026-07-13
phase: UCE-I11
---
# Budgets Fail Closed

## Decision

Any exceeded trial, wall, memory, CPU/GPU, retry, artifact, seed, fold, candidate, or per-candidate ceiling denies work.

## Context

Soft oversubscription would make cost and search breadth host-dependent and could hide multiplicity.

## Consequences

- Assess before reserve.
- Carry policy hash into trial identity.
- A policy change requires recompilation.


## Rejected alternatives

- Runtime inference of missing semantics.
- Mutable manifest fields after any trial begins.
- Best-effort cache acceptance.
- Removing failed/rejected attempts from evidence.

## Verification

- Contract and schema tests reject the prohibited state.
- Golden compilation is deterministic.
- Failure injection produces explicit scheduler and ledger evidence.
- Delivery validation checks that the ADR-linked invariant remains present.

## Rollback

Rollback removes the I11 implementation and restores the UCE-I10 handoff state. It must not rewrite or delete any completed I11 evidence that was already used by a downstream decision.
