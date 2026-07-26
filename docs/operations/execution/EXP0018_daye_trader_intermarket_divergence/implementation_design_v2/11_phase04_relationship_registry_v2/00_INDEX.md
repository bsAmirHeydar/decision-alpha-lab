---
id: EXP0018-P04-INDEX
title: "EXP0018 Phase 04 — Declarative 22-Relationship Registry v2"
type: implementation-index
status: implemented-uncompiled
project: EXP0018
phase: P04
version: 2.0.0
owner: Quant Engineering
---
# Phase 04 — Declarative 22-Relationship Registry v2

## Purpose

Convert the twenty-two approved/proposed Daye pairings into a single versioned registry and resolve each registry record against the Phase 03 paired-period store. P04 creates relationship context only. It does not inspect highs/lows for hunts and does not create BUY, SELL, SMT, drawing, or trading decisions.

## Canonical flow

```text
P03 Paired Period Store
  → P04 Canonical Registry
  → selector resolution
  → current/reference completeness gate
  → deterministic relationship opportunity
  → audit/store handoff to P05
```

## Documents

- [[01_SCOPE_AND_AUTHORITY]]
- [[02_CURRENT_AND_DESIRED_BEHAVIOR]]
- [[03_CANONICAL_REGISTRY_CONTRACT]]
- [[04_MAJOR_RELATIONSHIPS]]
- [[05_MINOR_RELATIONSHIPS]]
- [[06_SELECTOR_AND_RESOLUTION_ALGORITHM]]
- [[07_CURRENT_REFERENCE_ELIGIBILITY]]
- [[08_DOCTRINE_BLOCKERS_AND_DISABLED_RECORDS]]
- [[09_IDENTITY_DEDUPLICATION_AND_IDEMPOTENCY]]
- [[10_STATE_EVENTS_AND_STORE]]
- [[11_PARTIAL_DATA_AND_FAIL_CLOSED]]
- [[12_MQL5_MODULE_ARCHITECTURE]]
- [[13_INPUT_OUTPUT_AND_SCHEMA]]
- [[14_AUDIT_LEDGER]]
- [[15_TEST_AND_FIXTURE_PLAN]]
- [[16_RUNTIME_VALIDATION_GUIDE]]
- [[17_PERFORMANCE_AND_DETERMINISM]]
- [[18_SECURITY_AND_NO_EXECUTION_BOUNDARY]]
- [[19_DEFINITION_OF_DONE]]
- [[20_HANDOFF_TO_P05_P06_P11]]
- [[21_ROLLBACK_PLAN]]
- [[22_VALIDATION_REPORT]]
- [[23_OBSIDIAN_GUIDE]]
