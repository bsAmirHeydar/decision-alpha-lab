---
tags: [exp0019, fp-i10, adr]
status: accepted
---
# Treat checkpoints as caches

## Decision

Treat checkpoints as caches.

## Rationale

Exact validation or deterministic rebuild is safer than partial trust.

## Consequences

The decision is contract-versioned, testable, observable, and may only change through a new configuration/output version and migration plan.
