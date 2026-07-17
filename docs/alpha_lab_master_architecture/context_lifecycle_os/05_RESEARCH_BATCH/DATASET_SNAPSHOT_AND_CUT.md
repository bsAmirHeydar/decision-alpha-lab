---
title: Dataset Snapshot and Known-Time Cut
status: accepted-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, acl-05, research-batch]
---
# Dataset Snapshot and Known-Time Cut

## Purpose

Freezes exact dataset bytes, schema, producer, lineage and availability boundary.

## Contract model

Every row must satisfy event_time ≤ available_at ≤ cut_at. The snapshot records timezone, null policy, row count, content digest and source lineage.

## Failure semantics

Late data, revised vendor history and post-cut corrections require a new snapshot and therefore a new Batch.

## Authority boundary

This note describes ACL-05 reference mechanics. It does not establish external data quality, statistical edge, live-market parity, broker correctness, execution authority or capital authorization. Canonical JSON and policy artifacts outrank generated prose.

## Non-negotiable invariants

- Unknown fields, unresolved IDs and digest mismatches fail closed.
- Known-time semantics are inherited and may not be weakened.
- Candidate behavior remains byte- and digest-bound to ACL-04.
- Diagnostic artifacts remain segregated from selection.
- Material changes produce a new Batch identity; no in-place repair exists.
- Publication is all-or-nothing and leaves an attributable event/receipt trail.

## Verification obligations

Verification includes closed-schema validation, byte-digest checks, negative authority tests, known-time mutation tests, deterministic replay, content-addressed store resolution, event-chain validation and clean-checkout delivery checks. Passing these tests proves only the declared reference mechanics.

## Evolution and rollback

Additive compatible changes require a new minor contract version. Breaking semantics require a new major version, migration note and new Batch identity. Before publication, rollback deletes staging. After publication, rollback restores the prior repository commit; frozen artifacts are never rewritten.

## Related

[[LABEL_AND_DATASET_COMPILER]], [[OUTCOME_CUBE_AND_LABEL_MATURITY]], [[SPLIT_AND_CLUSTER_STANDARD]]
