---
tags: [exp0019, fp-i09, adr]
status: accepted
---
# Use append-only hash-chained semantic events

## Decision

Use append-only hash-chained semantic events.

## Rationale

Mutable rows cannot prove replay history or detect silent rewrites.

## Consequences

The behavior is versioned, tested, observable, and may only change through a new context configuration hash and migration plan.
