---
id: SAED-F39FE8FE1F
title: "Payoff and Entry Style System"
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
  - styles
  - moc
---

# Payoff and Entry Style System

## Axes

```mermaid
flowchart TD
  C[Context Occurrence] --> A[Setup Archetype]
  A --> P[Payoff Profile]
  A --> E[Entry Mechanism]
  A --> T[Trigger Philosophy]
  P --> S[Stop Geometry]
  P --> X[Exit Architecture]
  E --> G[Entry Geometry]
  T --> G
  S --> B[Complete Treatment]
  X --> B
  G --> B
```

## Mandatory Axes

1. Payoff profile.
2. Entry mechanism.
3. Trigger philosophy.
4. Entry geometry.
5. Stop geometry.
6. Exit architecture.
7. Management/re-entry.
8. Expiry and time policy.
9. Cost/execution profile.
10. Risk eligibility, not final sizing.

## Search Discipline

The system does not cross every value with every other value. A compatibility graph removes semantically invalid, causally impossible, broker-infeasible, cost-infeasible, dominated and unsupported combinations before training.
