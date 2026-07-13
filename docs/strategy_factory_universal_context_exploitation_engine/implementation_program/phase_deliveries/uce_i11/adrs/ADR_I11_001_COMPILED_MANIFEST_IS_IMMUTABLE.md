---
title: "ADR — Compiled Manifest Is Immutable"
status: accepted
date: 2026-07-13
phase: UCE-I11
---
# Compiled Manifest Is Immutable

## Decision

Once compiled, nodes, edges, trial identities, resource claims, compiler version, scheduler version, and excluded candidates are immutable.

## Context

Allowing runtime mutation would make executed multiplicity differ from declared multiplicity and would invalidate cache and reproducibility evidence.

## Consequences

- Recompile from a new declaration for any semantic change.
- Record the old manifest as superseded; do not edit it.
- Scheduler may change status only, never node semantics.


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
