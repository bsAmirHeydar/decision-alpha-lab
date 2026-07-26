---
title: "Family Dependency Graph"
status: proposed-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration, project-decision]
---
# Family Dependency Graph

```mermaid
flowchart LR
    K[ACL-OS / Strategy Factory Platform] --> T[Shared Time Session Data Contracts]
    T --> I[Intermarket and Structural Primitives]
    I --> M[M-Series and Read-Only Contexts]
    I --> D[EXP0018 Daye Trader]
    T --> D
    I --> C[EXP0015/16/17]
    D --> F[EXP0019 Faerie Protocol]
    C --> F
    T --> N[Flag / Zone / Hook / NDS]
    I --> N
    M --> E[Execution Adapter Wave]
    C --> E
    F --> E
    N --> E
    E --> R[Documentation Root Cleanup]
```

## Dependency decisions

- Shared time/session/known-time primitives precede all session-based families.
- Intermarket reference and divergence primitives precede EXP0017, EXP0018 and EXP0019 consolidation.
- EXP0019 depends on stable shared cores and must not fork them during migration.
- Flag/NDS/Hook/Zone requires its own sub-wave graph because Zone, Hook validity, NDS entitlement, treatment and broker request layers are distinct.
- Execution adapters are last because they consume canonical Context, Setup and Treatment outputs.
- Documentation/root cleanup waits for all active successor paths.
