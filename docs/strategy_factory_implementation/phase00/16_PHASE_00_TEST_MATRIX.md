---
title: "Phase 00 Test Matrix"
tags: [strategy-factory, phase-00, test-matrix]
status: canonical
---

# Phase 00 Test Matrix

## Automated phase-owned tests

| Requirement | Test | Expected behavior |
|---|---|---|
| Happy path | `test_happy_path_inventory_is_sorted_and_hashed` | all files inventoried in deterministic order with SHA-256 |
| Empty input | `test_empty_file_is_recorded` | zero-byte placeholders remain visible |
| Determinism | `test_scanner_is_deterministic` | repeated scans produce identical records |
| Comment safety | `test_comment_only_tokens_are_not_authority` | documentation/comments do not create false authority findings |
| Capital authority | `test_executable_order_send_is_critical` | executable `mt5.order_send` is classified critical |
| Contract discovery | `test_extracts_public_class_methods` | AST map captures public methods, excludes private methods |
| Version mismatch | `test_version_mismatch_is_rejected` | unsupported schema major fails closed |
| Missing version | `test_missing_version_is_rejected` | unversioned governed documents fail closed |
| Duplicate capability | `test_duplicate_persistence_and_normalization_are_detected` | persistence and normalization overlaps are surfaced |
| Missing repository | `test_missing_repository_root_fails_closed` | incorrect root cannot produce a false audit |
| Integration | `test_full_audit_writes_required_artifacts` | complete required artifact set is generated |
| Duplicate/replay | `test_duplicate_or_replayed_files_have_stable_hashes` | identical content yields identical SHA-256 |

## Roadmap fixture interpretation

The generic roadmap asks every phase for boundary-time and replay fixtures. Phase 00 does not yet own market-time semantics; its boundary equivalent is repository-root and schema-version validation. Market-clock boundary fixtures begin in Phase 07.

## Manual verification

### Authority review

Open `execution_authority_scan.csv`. A header-only file is expected for this snapshot.

### Migration review

Every row in `module_classification.csv` must have:

- non-empty module ID;
- capability;
- action;
- reason;
- current owner;
- target owner;
- risk level.

### Risk ownership review

Every open risk must have exactly one owner phase and a concrete mitigation.

### Test baseline review

The old pytest failure output must be retained in `test_baseline.json`; it must not be replaced by a generic `failed` flag.

## Future regression rule

Any change to scanner rules, authority patterns, module classifications, or risk IDs requires:

1. test update;
2. regenerated artifacts;
3. documentation review;
4. explanation of changed audit counts.
