---
tags: [exp0019, fp-i10, adr]
status: accepted
---
# Scope identity to chart, terminal, pair, epoch, and config

## Decision

Scope identity to chart, terminal, pair, epoch, and config.

## Rationale

Prevents multi-instance collisions while preserving deterministic restart identity.

## Consequences

The decision is contract-versioned, testable, observable, and may only change through a new configuration/output version and migration plan.
