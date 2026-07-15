---
title: Finite Action Constitution
status: implemented
version: 1.0.0
phase: V4-06
created: '2026-07-15'
updated: '2026-07-15'
capability_tier: core-production-context-plane
tags: [saed-v4, v4-06, treatment-dsl]
---

# Finite Action Constitution

## Purpose

Constrain the Treatment language to a closed institutional registry and bounded program grammar.

## Contract

Every permitted semantic action is represented by an exact primitive key. No free-form code, callback, expression evaluator, remote lookup, dynamic import or arbitrary executable payload is part of the language. This makes the DSL reviewable, reproducible and safe to hand to V4-07.

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

Reject identifiers or fields outside the frozen registry and policy, including syntactically plausible but ungoverned extensions. The implementation returns an explicit rejected or quarantined artifact where applicable. It never substitutes the nearest primitive, widens a range, drops an unknown field, merges Evidence Roles, reuses a stale hash or falls back to an executable default.

## Verification evidence

Evidence is provided through Python unit and adversarial tests, Draft 2020-12 closed-schema validation, deterministic golden fixtures, source-boundary scanning, diagnostic MQL5 static checks, Obsidian link/frontmatter validation, a phase QA report and a complete SHA-256 delivery ledger. Actual MetaEditor and external runtime evidence remain pending and are never inferred from static success.

## Authority boundary

Allowed: finite declaration, exact canonicalization, validation, external descriptor binding, integrity, replay, diff, partitioning, telemetry and bounded handoff. Forbidden: graph mutation, context truth inference, unbounded generation, action-lattice solving, model training, Treatment selection, position sizing, portfolio allocation, runtime activation, broker communication and order submission.

## Navigation

- Previous: [[04_V4_05_Input_Contract]]
- Phase home: [[00_MOC_V4_06_Treatment_DSL]]
- Next: [[06_Primitive_Ontology]]
