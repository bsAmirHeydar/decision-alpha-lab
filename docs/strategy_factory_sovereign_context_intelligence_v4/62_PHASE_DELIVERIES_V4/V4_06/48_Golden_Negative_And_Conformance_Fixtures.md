---
title: Golden Negative And Conformance Fixtures
status: implemented
version: 1.0.0
phase: V4-06
created: '2026-07-15'
updated: '2026-07-15'
capability_tier: core-production-context-plane
tags: [saed-v4, v4-06, treatment-dsl]
---

# Golden Negative And Conformance Fixtures

## Purpose

Provide reproducible accepted artifacts and targeted rejection cases.

## Contract

Golden fixtures include registry, policy, profile, one ordinary program, Skip, Abstain, package, validation, binding, integrity, replay, diff, telemetry, partition, exposure, conformance and V4-07 handoff. Negative fixtures exercise unknown primitives/parameters, range errors, cycles, binding mismatches, role conflicts and system-action violations.

## Engineering invariants

- Every semantic dependency is exact-versioned, content-addressed and reconstructible from immutable inputs.
- Unknown fields, unknown primitive keys, unsupported capabilities, over-budget payloads and authority expansion fail closed.
- Evidence Role and known-as-of boundaries are inherited from the V4-05 graph/handoff and cannot be widened by V4-06.
- Input ordering, process scheduling, cache location, host identity and runtime timestamps are not semantic inputs.
- A valid declaration remains non-executing: it cannot train, rank, allocate, activate or trade.

## Deterministic processing

1. Verify the upstream graph and handoff identities and hashes.
2. Validate the exact registry, institutional policy and diagnostic capability profile.
3. Parse the closed source contract with no field repair or implicit coercion.
4. Run static semantic, type, capability, state and authority analysis.
5. Canonicalize only accepted programs and derive content identities.
6. Bind any external descriptor by exact graph membership and semantic agreement.
7. Emit lineage, integrity, replay, diff, partition and exposure evidence.

## Failure behavior

A negative fixture passes only when it is rejected for the intended invariant. The implementation returns an explicit rejected or quarantined artifact where applicable. It never substitutes the nearest primitive, widens a range, drops an unknown field, merges Evidence Roles, reuses a stale hash or falls back to an executable default.

## Verification evidence

Evidence is provided through Python unit and adversarial tests, Draft 2020-12 closed-schema validation, deterministic golden fixtures, source-boundary scanning, diagnostic MQL5 static checks, Obsidian link/frontmatter validation, a phase QA report and a complete SHA-256 delivery ledger. Actual MetaEditor and external runtime evidence remain pending and are never inferred from static success.

## Authority boundary

Allowed: finite declaration, exact canonicalization, validation, external descriptor binding, integrity, replay, diff, partitioning, telemetry and bounded handoff. Forbidden: graph mutation, context truth inference, unbounded generation, action-lattice solving, model training, Treatment selection, position sizing, portfolio allocation, runtime activation, broker communication and order submission.

## Navigation

- Previous: [[47_Closed_Schema_Catalog]]
- Phase home: [[00_MOC_V4_06_Treatment_DSL]]
- Next: [[49_Test_Strategy_And_Mutation_Coverage]]
