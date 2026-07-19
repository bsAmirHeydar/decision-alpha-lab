---
title: "LCM-06 Security and Authority Model"
status: implemented-reference
version: 1.0.0
updated: 2026-07-19
tags: [acl-os, lcm, lcm-06, migration-framework]
phase_id: LCM-06
claim_ceiling: MIGRATION_FRAMEWORK_REFERENCE_ONLY
framework_run_id: FRAMEWORK_066C5FA5795AA4C283B17271E4478751
---
# LCM-06 Security and Authority Model

The authority permit is bound to the exact LCM-05 handoff digest and topology run. Source movement, deletion, target materialization, semantic refactor, merge, cutover, runtime, live order and capital capabilities are all denied.

Path traversal, absolute paths, Windows-reserved names, symlinks, dynamic execution, network calls and order APIs are rejected or statically scanned. Security-sensitive packets remain blocked until explicit security review.

## Evidence

- Framework run: `FRAMEWORK_066C5FA5795AA4C283B17271E4478751`
- Upstream topology: `TOPOLOGY_F28766C555330F0B89CC662DA8129220`
- Acceptance state: `REFERENCE_FRAMEWORK_ACCEPTED_NO_MIGRATION_EXECUTED`

## Non-claims

No source move, deletion, target materialization, semantic refactor, merge, cutover, runtime authority, order authority or capital authority is introduced.

## Related

- [[LCM_06_MIGRATION_FRAMEWORK_AND_COMPATIBILITY_LAYER_MIGRATION]]
- [[00_MOC]]
