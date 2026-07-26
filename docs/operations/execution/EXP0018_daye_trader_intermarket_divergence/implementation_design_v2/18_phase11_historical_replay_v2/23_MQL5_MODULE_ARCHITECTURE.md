---
id: EXP0018-P11-23_MQL5_MODULE_ARCHITECTURE
title: "MQL5 module architecture"
project: EXP0018
phase: P11
status: implemented
tags: [exp0018, daye, phase11, replay]
---

# MQL5 module architecture

- `DAYE_ReplayTypes`: schemas and states
- `DAYE_ReplayIdentity`: deterministic IDs and hashes
- `DAYE_ReplayDataLoader`: NY/UTC/broker range and exact source loading
- `DAYE_ReplayReducer`: as-of pipeline, host bars, confirmation, lifecycle
- `DAYE_ReplayAudit`: Common Files ledgers
- `DAYE_ReplaySelfTest`: pure reducer checks
- `DAYE_ReplayEngine`: chunked state owner
- Expert: inputs, timer, progress only
