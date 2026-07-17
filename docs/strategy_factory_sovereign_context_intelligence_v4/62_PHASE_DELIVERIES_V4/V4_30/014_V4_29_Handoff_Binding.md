---
title: V4-30 V4 29 Handoff Binding
status: accepted-reference
version: 1.0.0
phase: SAED_V4_30
section: Upstream Integrity
created: '2026-07-16'
updated: '2026-07-16'
tags: [saed-v4, v4-30, independent-replication, upstream-integrity]
---

# V4 29 Handoff Binding

## Purpose

This note defines the **V4 29 Handoff Binding** boundary inside SAED V4-30 independent and multi-lab replication. The implementation is deterministic, additive, closed-contract, synthetic-reference-only, and subordinate to the existing UCEE authority model.

## Authoritative inputs

- Frozen V4-29 certificate and handoff.
- Frozen V4-30 replication protocol and package identity.
- Registered synthetic laboratory, environment, assignment and preregistration identities.
- Known-time timestamps, append-only chain position and exact content hashes.

## Contract

The producer must emit a versioned JSON object with no unknown fields. Every identity is derived from canonical JSON and SHA-256. Every reference points to an immutable upstream identity. Missing, stale, reordered, duplicated, post-dated or mutated evidence fails closed.

## Invariants

1. No future-suffix information may affect an accepted-prefix result.
2. No laboratory may receive more than one assignment or execute more than one run.
3. Raw protected rows, hidden labels, candidate identity and custody material remain unavailable.
4. Cross-lab evidence is aggregate-only and bound to package, protocol, environment and preregistration identities.
5. Any disagreement produces quarantine; it cannot be overridden into promotion or runtime authority.
6. All authority flags remain false.

## Failure behavior

Unknown fields, identity collisions, shared independence dimensions, timing inversion, mutable environments, retries, semantic mismatch, metric tolerance breach, broken ledger links or unauthorized disclosure raise a typed failure and terminate the reference run without partial acceptance.

## Evidence and QA

Evidence is represented by exact golden artifacts, closed JSON schemas, positive, negative and mutation tests, deterministic replay, MQL5 static mirrors, Obsidian link checks, status validation, a file index, artifact inventory and SHA-256 ledger. Static evidence is not MetaEditor compile evidence and synthetic replication is not external institutional reproduction.

## Non-goals

This slice does not authorize model promotion, runtime compilation, risk allocation, order submission, production deployment, online adaptation or live trading. It does not claim real laboratory independence or real alpha.

## Related

- [[MOC|V4-30 Phase Delivery MOC]]
- [[../../60_IMPLEMENTATION_PROGRAM_V4/V4_30_Independent_And_Multi_Lab_Replication|Canonical V4-30 roadmap]]
