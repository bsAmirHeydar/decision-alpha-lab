---
title: "State Transition Parity"
status: implemented-reference
version: 1.0.0
updated: 2026-07-19
tags: [acl-os, lcm, lcm-06, migration-framework]
phase_id: LCM-06
claim_ceiling: MIGRATION_FRAMEWORK_REFERENCE_ONLY
framework_run_id: FRAMEWORK_066C5FA5795AA4C283B17271E4478751
---
# State Transition Parity

## Purpose

Compares state before and state after for every event.

## Contract

This control is bound to framework run `FRAMEWORK_066C5FA5795AA4C283B17271E4478751` and upstream topology `TOPOLOGY_F28766C555330F0B89CC662DA8129220`. Equivalent labels with different transition ordering remain a mismatch.

## Invariants

- source behavior and source bytes remain unchanged;
- UNKNOWN remains blocking;
- target paths remain proposals only;
- hard mismatch cannot be waived as soft;
- adapters and reports cannot acquire execution authority;
- all persistent identities and digests are deterministic.

## Evidence

The reference package stores the applicable registry, contract, fixture, validation result, report, event and provenance artifacts under `registry/legacy_context_migration/frameworks/FRAMEWORK_066C5FA5795AA4C283B17271E4478751/`.

## Failure semantics

A failed requirement stops publication or marks the affected fixture as blocked. The framework does not infer ownership, security approval, equivalence or parity.

## Verification

Run the LCM-06 package verifier, schema-instance validation, static policy scan, direct tests and LCM-05 through LCM-00 plus ACL-15 regression suites.

## Related

- [[LCM_06_MIGRATION_FRAMEWORK_AND_COMPATIBILITY_LAYER_MIGRATION]]
- [[MIGRATION_FRAMEWORK_ARCHITECTURE]]
