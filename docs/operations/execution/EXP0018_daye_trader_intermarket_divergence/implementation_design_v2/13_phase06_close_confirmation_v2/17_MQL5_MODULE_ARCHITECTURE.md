---
id: EXP0018-P06-MODULES
title: "P06 MQL5 Module Architecture"
type: implementation-note
status: implemented
project: EXP0018
phase: P06
version: 2.0.0
created: 2026-07-10
updated: 2026-07-10
tags:
  - exp0018
  - p06
  - confirmation
---

# Modules

| Module | Responsibility |
|---|---|
| `DAYE_ConfirmationTypes` | schema and enums |
| `DAYE_HostCloseClock` | exact two-symbol host bars |
| `DAYE_ConfirmationStateMachine` | pure candidate and outcome logic |
| `DAYE_ConfirmationStore` | mutable state owner |
| `DAYE_ConfirmationCheckpoint` | restart persistence |
| `DAYE_ConfirmationEvents` | deterministic event construction |
| `DAYE_ConfirmationDiagnostics` | human-readable output |
| `DAYE_ConfirmationAudit` | optional CSV adapter |
| `DAYE_ConfirmationSelfTest` | embedded pure tests |
| `DAYE_ConfirmationEngine` | orchestration |
| Expert | inputs, timer, lifecycle |
