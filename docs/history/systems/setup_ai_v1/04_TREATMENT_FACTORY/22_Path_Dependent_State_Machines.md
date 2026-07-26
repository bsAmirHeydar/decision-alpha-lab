---
id: SAED-371FD31F54
title: "Path-Dependent Treatment State Machines"
type: architecture
status: canonical
domain: strategy-factory-setup-ai-edge-discovery
version: 1.0.0
created: 2026-07-13
updated: 2026-07-13
tags:
  - strategy-factory
  - setup-factory
  - ai-training
  - treatment
  - state-machine
---

# Path-Dependent Treatment State Machines

## Required States

```text
Declared → Armed → Triggered → Filled → Managed → Exited
              ↘ Expired   ↘ Rejected  ↘ Cancelled
```

Trailing policies add states such as inactive, activated, ratcheting, partial-exited and runner-active.

## Ordering

Every event has a timestamp, source, sequence and side-aware price. Same-bar ambiguity is resolved by the frozen intrabar policy, not hindsight.

## Replay Requirements

- idempotent event application;
- restart snapshot;
- duplicate suppression;
- fill and partial-fill rules;
- gap behavior;
- trail ratchet invariant;
- no retroactive use of bar extremes;
- deterministic serialization.

## Research/Runtime Parity

The same state-machine semantics are used in outcome generation, tester, paper and runtime. A research-only trail is not deployable evidence.
