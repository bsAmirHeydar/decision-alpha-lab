---
id: UCPS-DEFFF8E1EF89
title: "Dependency Direction and Module Boundaries"
type: standard
status: canonical
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-23
updated: 2026-07-23
tags:
  - consolidation
  - platform-seal
---
# Dependency Direction and Module Boundaries

## Allowed direction

```text
kernel
  ↑
market
  ↑
context / treatment
  ↑
research / evidence
  ↑
policy / capital / portfolio
  ↑
runtime
  ↑
execution / monitoring
```

Adapters point inward through public ports. Contexts depend on public Context and market contracts. The kernel knows no Context ID and no broker.

## Forbidden dependencies

- runtime importing training implementation;
- research importing broker execution;
- Context importing private execution modules;
- shared engine branching on a specific Context slug;
- documentation generation mutating source contracts;
- MQL5 source redefining canonical authority semantics;
- registry records executing business logic.

## Enforcement

Static import rules, package boundary tests and architectural dependency graphs run in CI. A new exception requires an ADR with expiry and migration plan.
