---
title: "Migration Framework Architecture"
status: implemented-reference
version: 1.0.0
updated: 2026-07-19
tags: [acl-os, lcm, lcm-06, migration-framework]
phase_id: LCM-06
claim_ceiling: MIGRATION_FRAMEWORK_REFERENCE_ONLY
framework_run_id: FRAMEWORK_066C5FA5795AA4C283B17271E4478751
---
# Migration Framework Architecture

LCM-06 provides reusable migration control-plane machinery. It is subordinate to ACL-OS and cannot become a second operating system. The framework binds the exact LCM-05 topology handoff, validates migration packets, resolves aliases, compares behavior traces, describes adapters, previews path changes and evaluates quarantine/deletion evidence.

The framework has no domain-specific market logic and no execution authority. Every operation is deterministic and preview-only. Migration execution remains owned by later bounded phase commits.

## Evidence

- Framework run: `FRAMEWORK_066C5FA5795AA4C283B17271E4478751`
- Upstream topology: `TOPOLOGY_F28766C555330F0B89CC662DA8129220`
- Acceptance state: `REFERENCE_FRAMEWORK_ACCEPTED_NO_MIGRATION_EXECUTED`

## Non-claims

No source move, deletion, target materialization, semantic refactor, merge, cutover, runtime authority, order authority or capital authority is introduced.

## Related

- [[LCM_06_MIGRATION_FRAMEWORK_AND_COMPATIBILITY_LAYER_MIGRATION]]
- [[00_MOC]]
