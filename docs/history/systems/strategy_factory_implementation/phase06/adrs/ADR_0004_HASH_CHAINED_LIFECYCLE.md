# ADR_0004_HASH_CHAINED_LIFECYCLE

## Decision

Hash-chain lifecycle records so replay can detect omission, reordering, or mutation.

## Consequences

The engine gains explicit evidence and regression protection at the cost of stricter versioning and fixture maintenance.
