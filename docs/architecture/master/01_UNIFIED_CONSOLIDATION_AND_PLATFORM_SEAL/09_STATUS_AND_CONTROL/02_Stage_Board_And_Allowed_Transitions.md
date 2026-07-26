---
id: UCPS-AD336F9DF166
title: "Stage Board and Allowed Transitions"
type: status
status: active
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-23
updated: 2026-07-23
tags:
  - consolidation
  - platform-seal
---
# Stage Board and Allowed Transitions

| Stage | Status | Allowed next transition |
|---|---|---|
| Documentation foundation | READY | Merge and start UC-01 |
| UC-01 | NOT_STARTED | Execute preservation baseline |
| UC-02 | LOCKED | Requires UC-01 PASS |
| UC-03 | LOCKED | Requires UC-02 PASS |
| UC-04 | LOCKED | Requires UC-03 PASS |
| UC-05 | LOCKED | Requires UC-04 PASS |
| UC-06 | LOCKED | Requires UC-05 PASS |
| UC-07 | LOCKED | Requires UC-06 PASS |

A stage may become `BLOCKED` or `FAILED`; it cannot be manually marked `PASS` without an accepted exit report and evidence digest.
