---
tags: [exp0019, fp-i10, adr]
status: accepted
---
# Use one composition root

## Decision

Use one composition root.

## Rationale

Prevents product entrypoints from bypassing or duplicating upstream semantics.

## Consequences

The decision is contract-versioned, testable, observable, and may only change through a new configuration/output version and migration plan.
