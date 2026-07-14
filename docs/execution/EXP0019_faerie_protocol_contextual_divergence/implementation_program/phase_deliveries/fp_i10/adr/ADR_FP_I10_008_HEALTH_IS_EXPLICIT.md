---
tags: [exp0019, fp-i10, adr]
status: accepted
---
# Expose READY, DEGRADED, and BLOCKED

## Decision

Expose READY, DEGRADED, and BLOCKED.

## Rationale

Operators and downstream products need machine-readable failure semantics.

## Consequences

The decision is contract-versioned, testable, observable, and may only change through a new configuration/output version and migration plan.
