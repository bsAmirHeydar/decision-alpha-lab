---
title: "Event Ledger"
status: implemented-reference
version: 1.0.0
updated: 2026-07-19
tags: [acl-os, lcm, lcm-05, target-topology]
phase_id: LCM-05
claim_ceiling: TARGET_TOPOLOGY_REFERENCE_ONLY
---
# Event Ledger

## Purpose

Provides deterministic hash-linked phase events with all execution authorities denied.

## Contract

This control is bound to topology run `TOPOLOGY_F28766C555330F0B89CC662DA8129220`. It is a deterministic planning and governance artifact. It does not authorize path materialization, source movement, source deletion, semantic refactoring, merging, consumer cutover, runtime generation, order submission or capital activation.

## Invariants

- upstream LCM-04 hashes and handoff remain unchanged;
- every missing approval remains blocking;
- every target is root-relative and Windows-safe;
- generated projections cannot become canonical authority;
- protected ACL-OS and platform assets remain protected;
- a proposed path is not evidence of behavioral parity;
- all persistent IDs and digests are deterministic.

## Evidence

The machine package contains the relevant registry, map, audit, report, event, provenance, receipt and output-manifest records. Large inventories are stored as JSONL and CSV to preserve exact machine review and human inspection.

## Failure semantics

Integrity mismatch, unknown registry value, unsafe path, unreported collision, cyclic layer graph or authority escalation terminates publication. Partial output is discarded. No fallback guesses a target or approval.

## Verification

Run the LCM-05 package verifier, schema validation, static policy validation, direct tests and LCM-04 through LCM-00 plus ACL-15 regression suites.

## Related

- [[LCM_05_TARGET_TOPOLOGY_AND_REPOSITORY_LOCATOR_MIGRATION]]
- [[TARGET_REPOSITORY_TOPOLOGY]]
- [[CURRENT_TO_TARGET_PATH_MAP]]
