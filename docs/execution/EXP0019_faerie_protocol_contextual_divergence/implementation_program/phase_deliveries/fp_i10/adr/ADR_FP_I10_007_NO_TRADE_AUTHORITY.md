---
tags: [exp0019, fp-i10, adr]
status: accepted
---
# Keep runtime authority NONE

## Decision

Keep runtime authority NONE.

## Rationale

The Indicator must remain observational and cannot consume quota or mutate broker state.

## Consequences

The decision is contract-versioned, testable, observable, and may only change through a new configuration/output version and migration plan.
