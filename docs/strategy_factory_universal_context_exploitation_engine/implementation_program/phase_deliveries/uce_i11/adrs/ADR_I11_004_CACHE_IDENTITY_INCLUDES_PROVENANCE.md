---
title: "ADR — Cache Identity Includes Provenance"
status: accepted
date: 2026-07-13
phase: UCE-I11
---
# Cache Identity Includes Provenance

## Decision

Cache key includes namespace, artifact kind, producer/schema versions, ordered input hashes, and provenance hash.

## Context

Payload hash alone cannot distinguish fold, seed, transform, dependency, or producer semantics.

## Consequences

- Reject stale, incompatible, and corrupt records.
- Log cache hit/refusal in event and ledger evidence.
- Never repair provenance by editing metadata.


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
