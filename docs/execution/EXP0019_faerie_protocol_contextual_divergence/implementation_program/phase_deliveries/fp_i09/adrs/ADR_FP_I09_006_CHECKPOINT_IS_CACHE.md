---
tags: [exp0019, fp-i09, adr]
status: accepted
---
# Treat checkpoint as rebuildable cache

## Decision

Treat checkpoint as rebuildable cache.

## Rationale

Event stream and deterministic materialization are the source of truth.

## Consequences

The behavior is versioned, tested, observable, and may only change through a new context configuration hash and migration plan.
