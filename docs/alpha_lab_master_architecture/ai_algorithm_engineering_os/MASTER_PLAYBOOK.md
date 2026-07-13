---
title: "Master Playbook"
type: playbook
status: active
version: 2.0.0
created: 2026-07-10
updated: 2026-07-10
---
# Master Playbook v2

## Phase 0 — Establish Authority

Identify the architect/domain owner, policy precedence, active versions, and non-negotiable rules. Stop on unresolved authority conflicts.

## Phase 1 — Discover and Observe

Capture raw intent, observable facts, examples, counterexamples, timing assumptions, current behavior, and cost of failure. Do not code from ambiguity.

## Phase 2 — Formalize

Define ontology, entities, states, events, transitions, invariants, causal-time semantics, inputs, outputs, errors, budgets, non-goals, and Done criteria.

## Phase 3 — Design and Architect

Compare alternatives. Define ownership, dependency direction, contracts, schema versions, online/batch behavior, reconstruction, idempotency, and failure recovery.

## Phase 4 — Prepare a Vertical Patch

Create identity, exact files, preserved invariants, tests, compatibility, migration, rollback, installation, and commit plan. Keep scope reversible.

## Phase 5 — Implement

Inspect exact code, implement only approved behavior, use language standards, and rebuild after every bounded change.

## Phase 6 — Verify

Compile, static scan, unit/invariant/scenario tests, historical replay, visual checks, performance budgets, schema/lineage checks, and hostile review. Compilation alone is not verification.

## Phase 7 — Research and Validate

Create outcome evidence, baselines, fixed OOS folds, leakage audit, calibration/error analysis, stability, model cards, and reproducible run identity.

## Phase 8 — Promote Decisions

A human-approved versioned gate converts evidence into a production decision contract. Reports/models remain non-executable until this gate.

## Phase 9 — Execute Safely

Paper mode first. Enforce risk, idempotency, broker reconciliation, fail-closed inputs, monitoring, kill switch, and rollback.

## Phase 10 — Release and Learn

Package atomic patches/releases, update registries/changelog/Obsidian, monitor behavior, record incidents, retire invalid knowledge, and improve the operating system.

## Durable Artifact Rule

At every phase ask: **What committed artifact makes this decision independent of the original conversation?** If none exists, the work is not durable.
