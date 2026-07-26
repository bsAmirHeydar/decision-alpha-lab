---
title: Outcome Cube and Label Maturity
status: accepted-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, acl-05, research-batch]
---
# Outcome Cube and Label Maturity

## Purpose

Separates research outcomes, diagnostic path measures and the time at which each becomes knowable.

## Contract model

A label cannot be consumed before its horizon and availability delay. Diagnostic path information is never promoted into candidate selection by ACL-05.

## Failure semantics

Future path leakage can create a false research edge even when the candidate itself is known-time safe.

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

[[LABEL_AND_DATASET_COMPILER]], [[SPLIT_AND_CLUSTER_STANDARD]], [[COMPLETE_SEARCH_EXPOSURE]]
