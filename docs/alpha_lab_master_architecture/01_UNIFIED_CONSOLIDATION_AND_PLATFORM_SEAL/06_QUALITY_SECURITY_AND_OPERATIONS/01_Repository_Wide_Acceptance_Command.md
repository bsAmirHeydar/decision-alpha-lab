---
id: UCPS-38C8BB475C6D
title: "Repository-Wide Acceptance Command"
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
# Repository-Wide Acceptance Command

## Command

The final operator entry point is:

```powershell
alpha verify repository
```

## Required checks

Topology and root allowlist; naming and dependency rules; contracts, schemas and registries; formatting and static analysis; unit, contract, property, mutation, differential, integration, security, recovery and end-to-end tests; MQL5 static analysis, MetaEditor compilation, Strategy Tester and Python/MQL5 parity; generated-file integrity; documentation validation; legacy import and external consumer scans; clean-clone reproduction and Golden Context execution.

## Output

The command publishes a machine-readable acceptance receipt with environment identity, tool versions, each gate result, evidence location and overall non-compensatory decision.

## Scope modes

Targeted developer mode may run a subset. Stage and seal acceptance always run the full governed profile.
