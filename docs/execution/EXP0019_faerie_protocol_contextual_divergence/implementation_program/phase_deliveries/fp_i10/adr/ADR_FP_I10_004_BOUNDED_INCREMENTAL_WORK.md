---
tags: [exp0019, fp-i10, adr]
status: accepted
---
# Use bounded incremental work after initial backfill

## Decision

Use bounded incremental work after initial backfill.

## Rationale

Avoids accidental full-history loops and UI stalls.

## Consequences

The decision is contract-versioned, testable, observable, and may only change through a new configuration/output version and migration plan.
