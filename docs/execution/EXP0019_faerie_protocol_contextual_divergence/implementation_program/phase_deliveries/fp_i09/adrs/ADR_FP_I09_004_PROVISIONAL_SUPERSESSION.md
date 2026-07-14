---
tags: [exp0019, fp-i09, adr]
status: accepted
---
# Allow provisional reservation supersession before session seal

## Decision

Allow provisional reservation supersession before session seal.

## Rationale

Late synchronized evidence must converge to batch replay without deleting prior events.

## Consequences

The behavior is versioned, tested, observable, and may only change through a new context configuration hash and migration plan.
