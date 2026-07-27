---
id: UCPS-AD336F9DF166
title: "Stage Board and Allowed Transitions"
type: status
status: active
domain: unified-consolidation-platform-seal
version: 1.1.0
created: 2026-07-23
updated: 2026-07-27
tags:
  - consolidation
  - platform-seal
---
# Stage Board and Allowed Transitions

| Stage | Status | Allowed next transition |
|---|---|---|
| Documentation foundation | ACCEPTED | Historical authority only |
| UC-01 — Preserve and Baseline | ACCEPTED | Preserve immutable baseline |
| UC-02 — Authority and Standardization | ACCEPTED | Preserve authority freeze |
| UC-03 — Physical Reorganization | ACCEPTED | Preserve canonical topology |
| UC-04 — Semantic and Logic Unification | IN_PROGRESS | Execute UC04-W1 after W0 PASS |
| UC-05 — Platform Mechanization | LOCKED | Requires accepted UC-04 exit |
| UC-06 — Migration and Cutover | LOCKED | Requires accepted UC-05 exit |
| UC-07 — Delete and Seal | LOCKED | Requires accepted UC-06 exit and explicit deletion authority |

## Current wave board

| Wave | Status | Authority |
|---|---|---|
| UC04-W0 — Foundation and Recovery | ACCEPTED | Recovery only; no semantic merge |
| UC04-W1 — Deterministic MQL5 Formatting Primitive | AUTHORIZED | Characterization and bounded implementation |
| Later UC04 waves | LOCKED | Require prior-wave PASS and candidate registration |

A stage or wave may become `BLOCKED` or `FAILED`; it cannot be manually marked accepted without an evidence-bound exit decision.
