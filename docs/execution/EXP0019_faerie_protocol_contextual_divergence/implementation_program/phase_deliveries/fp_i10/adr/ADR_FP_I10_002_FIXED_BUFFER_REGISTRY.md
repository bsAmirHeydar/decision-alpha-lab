---
tags: [exp0019, fp-i10, adr]
status: accepted
---
# Version a fixed twelve-buffer registry

## Decision

Version a fixed twelve-buffer registry.

## Rationale

iCustom consumers and tests require stable channel ordering.

## Consequences

The decision is contract-versioned, testable, observable, and may only change through a new configuration/output version and migration plan.
