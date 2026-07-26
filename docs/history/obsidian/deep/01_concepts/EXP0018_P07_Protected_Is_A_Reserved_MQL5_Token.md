---
id: EXP0018-P07-MQL5-RESERVED-PROTECTED
aliases:
  - P07 reserved protected hotfix
  - DAYE lifecycle compile hotfix
project: EXP0018
phase: P07
status: implemented
---

# EXP0018 P07 — `protected` is a reserved MQL5 token

`protected` may appear in documentation and string values, but it cannot be used as an MQL5 variable or parameter identifier.

The P07 self-test helper uses `protected_symbol` for its local parameter while retaining the canonical domain fields `protected_broker_symbol` and `protected_canonical_symbol`.

Related:
- [[CG_EXP0018_PHASE07_REFERENCE_LIFECYCLE_MOC]]
- [[EXP0018 Reference Lifecycle Is A State Machine]]
