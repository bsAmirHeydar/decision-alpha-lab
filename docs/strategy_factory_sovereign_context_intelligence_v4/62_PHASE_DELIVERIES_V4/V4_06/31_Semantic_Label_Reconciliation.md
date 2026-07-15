---
title: Semantic Label Reconciliation
status: implemented
version: 1.0.0
phase: V4-06
created: '2026-07-15'
updated: '2026-07-15'
capability_tier: core-production-context-plane
tags: [saed-v4, v4-06, treatment-dsl]
---

# Semantic Label Reconciliation

## Purpose

Require declared labels to agree across graph descriptors, primitives and programs.

## Contract

The reference binding reconciles payoff_profile=P3, entry_mechanism=breakout and path_dependent=true. Labels are closed evidence for compatibility; they are not model outputs or performance claims.

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

Reject contradictory, missing or type-incompatible labels; do not choose a nearest match. The implementation returns an explicit rejected or quarantined artifact where applicable. It never substitutes the nearest primitive, widens a range, drops an unknown field, merges Evidence Roles, reuses a stale hash or falls back to an executable default.

## Verification evidence

Evidence is provided through Python unit and adversarial tests, Draft 2020-12 closed-schema validation, deterministic golden fixtures, source-boundary scanning, diagnostic MQL5 static checks, Obsidian link/frontmatter validation, a phase QA report and a complete SHA-256 delivery ledger. Actual MetaEditor and external runtime evidence remain pending and are never inferred from static success.

## Authority boundary

Allowed: finite declaration, exact canonicalization, validation, external descriptor binding, integrity, replay, diff, partitioning, telemetry and bounded handoff. Forbidden: graph mutation, context truth inference, unbounded generation, action-lattice solving, model training, Treatment selection, position sizing, portfolio allocation, runtime activation, broker communication and order submission.

## Navigation

- Previous: [[30_Descriptor_Binding]]
- Phase home: [[00_MOC_V4_06_Treatment_DSL]]
- Next: [[32_State_Machine_Declaration]]
