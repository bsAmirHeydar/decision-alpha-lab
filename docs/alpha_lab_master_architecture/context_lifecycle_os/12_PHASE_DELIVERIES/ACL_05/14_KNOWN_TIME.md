---
title: ACL-05 — Known-Time Enforcement
status: accepted-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, acl-05, phase-delivery]
---
# Known-Time Enforcement

## Decision

This delivery record fixes the ACL-05 reference behavior for **known-time enforcement**. The canonical implementation is versioned, deterministic and subordinate to the ACL-00 authority model, ACL-03 known-time semantics and ACL-04 candidate behavior.

## Required evidence

- machine-readable closed-schema artifact or explicit code contract;
- stable identity and SHA-256 digest where material;
- positive conformance test and at least one hostile negative test;
- lineage to the exact ACL-04 handoff and, where applicable, ACL-03 context identity;
- explicit denied capabilities for orders, capital, network and secrets;
- Obsidian projection that distinguishes canonical artifacts from explanation.

## Acceptance rule

Acceptance is fail closed. Missing identity, unknown fields, unresolved digest, mutable path, future-derived availability, diagnostic leakage, overlapping split, budget expansion or output partiality rejects the operation. A local pass cannot exceed `RESEARCH_BATCH_FREEZE_REFERENCE_ONLY`.

## Implementation mapping

The behavior is implemented under `tools/strategy_factory/acl_os/acl_05`, registered under `registry/acl_os/acl_05`, tested under `lab/11_strategy_factory/acl_os/tests_acl_05`, mirrored statically under the ACL05 MQL5 include folder and demonstrated by `fixtures/acl_05/reference_batch`.

## Change control

Additive changes require compatible schema/policy versioning and regression evidence. Material or breaking changes require a new Batch identity, migration note and rollback evidence. Generated frozen artifacts are never edited in place.

## Verification questions

1. Is the exact upstream identity bound?
2. Is known-time causality preserved?
3. Can the same material reproduce the same semantic identity?
4. Is every capability narrower than or equal to the upstream permit?
5. Does a mutation trigger a deterministic rejection or new Batch ID?
6. Is the claim ceiling visible in machine and human outputs?

## Related

- [[00_MOC]]
- [[ACL_05_IMMUTABLE_BATCH_AND_STORE]]
- [[IMMUTABLE_RESEARCH_BATCH]]
