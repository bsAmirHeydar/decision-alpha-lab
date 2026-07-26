---
title: "ADR — Rejected Candidates Are Evidence-Only"
status: accepted
date: 2026-07-13
phase: UCE-I11
---
# Rejected Candidates Are Evidence-Only

## Decision

UCE-I10 reject decisions remain in the manifest exclusion evidence but cannot produce trainer or trial nodes.

## Context

Scheduling a rejected model would bypass the non-bypassable deep/classical admission gates and contaminate the experiment universe.

## Consequences

- Keep rejected keys and admission hashes in evidence.
- Do not allocate resources to rejects.
- A later admission requires new evidence and a new manifest.


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
