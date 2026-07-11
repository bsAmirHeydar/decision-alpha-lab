---
title: "Program Governance and Commit Protocol"
tags:
  - strategy-factory
  - implementation-roadmap
  - alpha-lab
status: canonical
doc_version: 1.0.0
---

# Program Governance and Commit Protocol

## Work Packet Rule

Every phase is implemented through small work packets. A work packet contains:

- objective;
- scope;
- explicit exclusions;
- files to add or change;
- contracts affected;
- tests;
- artifacts;
- acceptance criteria;
- rollback plan.

## Commit Rule

One coherent contract or behavior per commit. Avoid commits combining schema changes, migration, models, and execution behavior.

Recommended commit pattern:

```text
feat(strategy-factory): add canonical anatomy event contract
feat(strategy-factory): add plugin capability registry
feat(strategy-factory): add purged walk-forward splitter
fix(strategy-factory): reject stale context snapshots
```

## ADR Rule

Create an Architecture Decision Record whenever changing:

- contract semantics;
- ownership boundary;
- time semantics;
- runtime authority;
- storage format;
- plugin protocol;
- promotion criteria.
