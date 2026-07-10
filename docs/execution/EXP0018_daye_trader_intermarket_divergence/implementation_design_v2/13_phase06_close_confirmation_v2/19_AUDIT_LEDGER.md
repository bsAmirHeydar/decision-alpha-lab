---
id: EXP0018-P06-AUDIT
title: "P06 Audit Ledger"
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

# Audit

Optional Common Files CSV record types:

- `SUMMARY`;
- `CANDIDATE`;
- `RESULT`;
- `EVENT`.

Audit is append-only. Result rows contain enough geometry and identity for P08 and P12 reconciliation. The checkpoint and audit file serve different purposes and must not be conflated.
