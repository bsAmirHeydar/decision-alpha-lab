---
title: "Trace Normalization and Comparison"
status: implemented-reference
version: 1.0.0
updated: 2026-07-19
tags: [acl-os, lcm, lcm-06, migration-framework]
phase_id: LCM-06
claim_ceiling: MIGRATION_FRAMEWORK_REFERENCE_ONLY
framework_run_id: FRAMEWORK_066C5FA5795AA4C283B17271E4478751
---
# Trace Normalization and Comparison

Trace normalization converts timestamps to UTC microsecond form, canonicalizes reason-code ordering, stabilizes numeric drawing anchors and preserves event order. Hard parity dimensions include causal time, bar selection, state transitions, decisions, invalidation, expiry, no-trade, treatment request and drawing anchors.

A hard mismatch blocks migration. Missing required hard evidence becomes `UNKNOWN_EVIDENCE`, not PASS. Soft differences are reported separately and cannot waive hard mismatches.

## Evidence

- Framework run: `FRAMEWORK_066C5FA5795AA4C283B17271E4478751`
- Upstream topology: `TOPOLOGY_F28766C555330F0B89CC662DA8129220`
- Acceptance state: `REFERENCE_FRAMEWORK_ACCEPTED_NO_MIGRATION_EXECUTED`

## Non-claims

No source move, deletion, target materialization, semantic refactor, merge, cutover, runtime authority, order authority or capital authority is introduced.

## Related

- [[LCM_06_MIGRATION_FRAMEWORK_AND_COMPATIBILITY_LAYER_MIGRATION]]
- [[00_MOC]]
