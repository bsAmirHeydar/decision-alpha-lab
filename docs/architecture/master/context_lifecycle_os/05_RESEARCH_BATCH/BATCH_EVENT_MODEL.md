---
title: Batch Event Model
status: accepted-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, acl-05, research-batch]
---
# Batch Event Model

## Purpose

Defines an append-only, deterministic hash chain for the freeze lifecycle.

## Contract model

Events use stable sequence, previous digest, exact payload and denied authority fields. The final ledger digest is bound into the Batch manifest and ACL-06 handoff.

## Failure semantics

Editable audit logs, implicit timestamps and missing prior links are not evidence-grade.

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

[[BATCH_FREEZE_PROTOCOL]], [[BATCH_REPRODUCTION_BUNDLE]], [[RESEARCH_FAILURE_TAXONOMY]]
