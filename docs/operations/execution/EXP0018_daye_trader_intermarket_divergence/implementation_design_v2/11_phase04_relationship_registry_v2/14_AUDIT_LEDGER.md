---
id: EXP0018-P04-AUDIT
title: "P04 Audit Ledger"
type: ledger-contract
status: active
project: EXP0018
phase: P04
---
# Audit Ledger

Optional Common Files CSV records:

- `REGISTRY`: frozen definition and blocker metadata;
- `SUMMARY`: store-level counts and readiness;
- `RESOLUTION`: current/reference identity, completeness, status, and reason;
- `EVENT`: typed state transitions.

The ledger is append-only for the runtime. It is disabled by default to avoid unnecessary I/O.
