---
id: UCPS-A338F4D4647A
title: "Authority, Ownership and Change Control"
type: governance
status: canonical
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-23
updated: 2026-07-23
tags:
  - consolidation
  - platform-seal
---
# Authority, Ownership and Change Control

## Required ownership roles

- Platform architecture owner
- Kernel and contract owner
- Market-truth owner
- Context Factory owner
- Research and evidence owner
- Runtime and execution owner
- MQL5 and terminal owner
- Documentation authority owner
- Security reviewer
- Independent migration reviewer

One person may perform multiple implementation tasks, but acceptance of destructive deletion, security controls and final seal requires separation of duties.

## Change classes

| Class | Example | Required control |
|---|---|---|
| Move-only | `git mv` with import rewrite | stage packet and regression |
| Compatible refactor | implementation replacement with same contract | characterization and differential tests |
| Contract addition | optional field or extension port | ADR and conformance tests |
| Breaking platform change | identity, lifecycle or authority change | architecture ADR, migration and explicit approval |
| Destructive deletion | removal of old source or docs | preservation certificate, zero consumers, recovery proof |

## Waivers

Waivers are narrow, expiring and non-transitive. A waiver cannot authorize order execution, bypass known-time controls, excuse unknown consumers or permit deletion without recoverability.
