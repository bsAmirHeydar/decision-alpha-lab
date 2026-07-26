---
title: "Compatibility Adapter Boundary"
status: implemented-reference
version: 1.0.0
updated: 2026-07-19
tags: [acl-os, lcm, lcm-06, migration-framework]
phase_id: LCM-06
claim_ceiling: MIGRATION_FRAMEWORK_REFERENCE_ONLY
framework_run_id: FRAMEWORK_066C5FA5795AA4C283B17271E4478751
---
# Compatibility Adapter Boundary

Compatibility adapters translate legacy observations into canonical observation contracts while preserving known-time semantics, reason codes and state order. Supported reference adapter classes are Context, Setup, Treatment and Visualizer.

Adapters cannot mutate source, expand semantics, acquire execution authority or authorize runtime, live orders or capital. An adapter is a temporary compatibility boundary, not canonical domain truth.

## Evidence

- Framework run: `FRAMEWORK_066C5FA5795AA4C283B17271E4478751`
- Upstream topology: `TOPOLOGY_F28766C555330F0B89CC662DA8129220`
- Acceptance state: `REFERENCE_FRAMEWORK_ACCEPTED_NO_MIGRATION_EXECUTED`

## Non-claims

No source move, deletion, target materialization, semantic refactor, merge, cutover, runtime authority, order authority or capital authority is introduced.

## Related

- [[LCM_06_MIGRATION_FRAMEWORK_AND_COMPATIBILITY_LAYER_MIGRATION]]
- [[00_MOC]]
