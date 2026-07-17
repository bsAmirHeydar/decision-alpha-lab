---
title: Label and Dataset Contract Compiler
status: accepted-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, acl-05, research-batch]
---
# Label and Dataset Contract Compiler

## Purpose

Compiles dataset and label declarations into closed, content-addressed contracts.

## Contract model

Primary labels are selection-safe; path diagnostics are explicitly segregated. Horizon, availability-after, null behavior and dataset binding are mandatory.

## Failure semantics

A label expression without maturity semantics or a dataset without availability time is unusable.

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

[[DATASET_SNAPSHOT_AND_CUT]], [[OUTCOME_CUBE_AND_LABEL_MATURITY]], [[RESEARCH_FAILURE_TAXONOMY]]
