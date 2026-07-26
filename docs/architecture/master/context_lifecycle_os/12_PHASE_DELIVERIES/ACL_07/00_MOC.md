---
title: ACL-07 — Map of Content
status: accepted-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, acl-07, validation]
---
# ACL-07 — Map of Content

## Purpose

This note specifies map of content for the accepted ACL-07 reference implementation. It is written as an operational Obsidian artifact rather than a superficial code summary.

## Contract

The artifact is identity-bound, schema-validated, digest-protected, deterministic and non-promotional. Missing or ambiguous evidence does not become a permissive default.

## Engineering requirements

- Preserve ACL-06 evidence byte-for-byte.
- Apply only registered gate semantics.
- Record explicit PASS, FAIL, UNKNOWN or NOT_APPLICABLE.
- Keep Diagnostic candidates non-selectable.
- Publish reason codes, lineage and residual risk.
- Deny order submission and capital activation.

## Verification

Unit, contract, negative, replay and delivery tests must exercise this concern. Passing reference tests proves mechanics only.

## Navigation

- [[00_MOC]]
- [[01_PHASE_CHARTER]]
- [[02_RESPONSIBILITY_BOUNDARY]]
- [[03_UPSTREAM_HANDOFF]]
- [[04_AUTHORITY_PERMIT]]
- [[05_INPUT_INTEGRITY]]
- [[06_POLICY_SNAPSHOT]]
- [[07_GATE_REGISTRY]]
- [[08_GATE_STATUS]]
- [[09_DATA_LEAKAGE]]
- [[10_DIAGNOSTIC_ISOLATION]]
- [[11_MINIMUM_SUPPORT]]
- [[12_EFFECT_SIZE]]
- [[13_BINOMIAL_EVIDENCE]]
- [[14_WILSON_BOUND]]
- [[15_FDR_CONTROL]]
- [[16_BASELINE_DOMINANCE]]
- [[17_TEMPORAL_GENERALIZATION]]
- [[18_OVERFIT_CONTROL]]
- [[19_TAIL_ROBUSTNESS]]
- [[20_EXECUTION_ECONOMICS]]
- [[21_OOD_ABSTENTION]]
- [[22_PROSPECTIVE_EVIDENCE]]
- [[23_INDEPENDENT_REPLICATION]]
- [[24_CANDIDATE_GATE_VECTOR]]
- [[25_DECISION_POLICY]]
- [[26_REASON_CODE_CATALOG]]
- [[27_MULTIPLE_TESTING_REPORT]]
- [[28_INTEGRITY_REPORT]]
- [[29_SECURITY_BOUNDARY]]
- [[30_EVENT_LEDGER]]
- [[31_PROVENANCE_GRAPH]]
- [[32_ATOMIC_PUBLICATION]]
- [[33_OUTPUT_MANIFEST]]
- [[34_VALIDATION_RECEIPT]]
- [[35_ACL08_HANDOFF]]
- [[36_OBSIDIAN_PROJECTION]]
- [[37_CLI]]
- [[38_REPLAY_VALIDATION]]
- [[39_STATIC_VALIDATION]]
- [[40_UNIT_TESTS]]
- [[41_CONTRACT_TESTS]]
- [[42_SECURITY_NEGATIVE_TESTS]]
- [[43_MUTATION_TESTS]]
- [[44_GOLDEN_REPLAY]]
- [[45_CLEAN_OVERLAY_TEST]]
- [[46_MIGRATION_POLICY]]
- [[47_ROLLBACK_PLAN]]
- [[48_THREAT_MODEL]]
- [[49_HOSTILE_REVIEW]]
- [[50_RESIDUAL_RISK]]
- [[51_DEFINITION_OF_DONE]]
- [[52_HANDOFF_CHECKLIST]]
