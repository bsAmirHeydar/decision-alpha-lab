---
title: "Testing and Quality Master Plan"
tags:
  - strategy-factory
  - implementation-roadmap
  - alpha-lab
status: canonical
doc_version: 1.0.0
---

# Testing and Quality Master Plan

## Test Pyramid

### Unit Tests

Pure functions, serializers, policy geometry, cost conversion, utility functions, cache invalidation, and risk calculations.

### Contract Tests

Every plugin implementation must satisfy the same behavioral contract. Cross-language fixtures prove Python/MQL5 equivalence.

### Property Tests

Use generated data to assert invariants:

- stop geometry never reverses risk direction;
- known time never exceeds decision inputs;
- candidate identity is stable;
- duplicate intents are idempotently rejected;
- exposure never exceeds configured caps;
- adding cost never improves net return.

### Integration Tests

Run complete event-to-outcome and event-to-paper paths.

### Golden Replay Tests

Frozen historical examples with exact expected events, features, candidates, decisions, and traces.

### Differential Tests

Compare old strategy implementation with Factory adapter during migration.

### Chaos Tests

Missing feed, stale feature, broker rejection, duplicate event, delayed acknowledgement, model file corruption, clock skew, partial fill, disconnect, restart, and recovery.

### Performance Tests

Startup compilation time, event decision latency, allocations, cache hit ratio, throughput, and memory growth.

## Quality Gates

A phase cannot merge unless:

- required unit tests pass;
- contract fixtures pass;
- static checks pass;
- documentation and ADRs are updated;
- phase artifacts are generated;
- no unresolved critical ambiguity remains.
