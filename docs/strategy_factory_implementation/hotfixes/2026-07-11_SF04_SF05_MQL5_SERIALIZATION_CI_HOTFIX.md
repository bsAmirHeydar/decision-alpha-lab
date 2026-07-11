---
title: "SF04/SF05 MQL5 Serialization CI Hotfix"
status: implemented
scope: strategy-factory
hotfix_id: SF-HF-2026-07-11-001
---

# SF04/SF05 MQL5 Serialization CI Hotfix

## Failure

The repository Engineering Policy job failed in the MQL5 compatibility step because Phase 04 and Phase 05 introduced `LongToString(...)` in MQL5 source. The repository compatibility policy explicitly requires the compiler-tested `IntegerToString(...)` serialization pattern for both integer and long values.

## Remediation

This hotfix changes only serialization calls. It does not alter contract identity fields, event semantics, generation semantics, sink ordering, or execution authority.

- Replaced all Phase 04 `LongToString(...)` calls with `IntegerToString(...)`.
- Replaced all Phase 05 `LongToString(...)` calls with `IntegerToString(...)`.
- Preserved the same canonical field order and delimiters.
- Preserved no-send authority boundaries.

## Validation

The exact GitHub Actions Engineering Policy commands were reproduced against the cumulative repository state:

```text
validate_alpha_lab_policy.py: PASS
validate_vault.py: PASS
check_mql5_compatibility.py: PASS — errors=0 warnings=0
audit_repository_layout.py: PASS — missing=0
```

## Ownership

This hotfix applies to Phase 04 and Phase 05 files only. Phase 06 is distributed separately with the same compatibility correction already applied.
