---
title: "Reference Fixture Strategy"
status: implemented-reference
version: 1.0.0
updated: 2026-07-19
tags: [acl-os, lcm, lcm-06, migration-framework]
phase_id: LCM-06
claim_ceiling: MIGRATION_FRAMEWORK_REFERENCE_ONLY
framework_run_id: FRAMEWORK_066C5FA5795AA4C283B17271E4478751
---
# Reference Fixture Strategy

LCM-06 exercises the framework with synthetic valid, ambiguous, missing-owner, future-aware and security-sensitive migration packets. It also includes exact, soft-mismatch and hard-mismatch traces, adapter contracts, move previews, redirect previews, quarantine cases and deletion cases.

Fixtures prove framework mechanics only. They do not prove any real Context migration, MQL5 parity or semantic equivalence.

## Evidence

- Framework run: `FRAMEWORK_066C5FA5795AA4C283B17271E4478751`
- Upstream topology: `TOPOLOGY_F28766C555330F0B89CC662DA8129220`
- Acceptance state: `REFERENCE_FRAMEWORK_ACCEPTED_NO_MIGRATION_EXECUTED`

## Non-claims

No source move, deletion, target materialization, semantic refactor, merge, cutover, runtime authority, order authority or capital authority is introduced.

## Related

- [[LCM_06_MIGRATION_FRAMEWORK_AND_COMPATIBILITY_LAYER_MIGRATION]]
- [[00_MOC]]
