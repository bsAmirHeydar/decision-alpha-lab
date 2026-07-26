---
title: "LCM-05 — Target Topology and Repository Locator"
status: implemented-reference
version: 2.0.0
updated: 2026-07-19
tags: [acl-os, lcm, legacy-migration, target-topology, repository-locator]
phase_id: LCM-05
claim_ceiling: TARGET_TOPOLOGY_REFERENCE_ONLY
topology_run_id: TOPOLOGY_F28766C555330F0B89CC662DA8129220
---
# LCM-05 — Target Topology and Repository Locator

LCM-05 defines the deterministic destination architecture for every classified repository artifact while preserving all LCM-00 through LCM-04 restrictions. It maps artifacts, identities, root release files, duplicate documentation trees and unresolved identity records without moving, deleting, merging, refactoring or cutting over any source.

## Implemented control plane

- one closed package-root registry;
- one closed dependency-direction policy;
- an authored/generated authority boundary;
- 38,595 artifact target mappings;
- 2,792 identity package mappings;
- 2,040 ambiguity quarantine proposals;
- 1,076 root relocation plans;
- documentation successor records;
- Windows-safe root-relative path validation;
- case-insensitive collision analysis;
- dependency-direction audit over resolved legacy edges;
- immutable receipt, manifest, event ledger, provenance and LCM-06 handoff.

## Claim ceiling

`TARGET_TOPOLOGY_REFERENCE_ONLY`

The phase approves the reference topology contract. It does not approve path materialization, source movement, source deletion, semantic refactoring, duplicate merging, consumer cutover, runtime generation, order submission or capital activation.

## Acceptance state

`REFERENCE_TOPOLOGY_ACCEPTED_MATERIALIZATION_BLOCKED`

The target graph is deterministic, acyclic, root-relative, Windows-safe and collision-free. Materialization remains blocked by human ownership approvals, security review, identity ambiguity resolution, legacy runtime parity, equivalence review and unavailable MetaTrader runtime evidence.

## Handoff

LCM-06 may build reusable migration validators, resolvers, comparators and compatibility interfaces against the immutable LCM-05 package. It may not materialize any proposed path or reinterpret a proposal as a migrated artifact.

## Related

- [[00_MOC]]
- [[LCM05_TO_LCM06_HANDOFF_CONTRACT]]
- [[LCM06_ENTRY_CHECKLIST]]
- [[TARGET_REPOSITORY_TOPOLOGY]]
- [[CURRENT_TO_TARGET_PATH_MAP]]
