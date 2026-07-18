---
title: "LCM-08 — Context Package Migration"
status: proposed-reference
version: 1.1.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration, implementation-phase]
phase_id: LCM-08
---
# LCM-08 — Context Package Migration

Move domain state and occurrence semantics into canonical ACL-02-compatible Context packages while preserving observed and approved behavior.

## Claim ceiling

`CONTEXT_PACKAGE_MIGRATION_REFERENCE_ONLY`

## Phase entry contract

- exact prior-phase handoff and digest;
- current baseline plus all approved amendments;
- phase authority permit and named reviewers;
- closed registries and schemas;
- explicit UNKNOWN for missing evidence.

## Work packages

### WP-08.1 Context boundary extraction

Identify what belongs to market Context versus Setup, Treatment, visualization and execution.

### WP-08.2 Package authoring

Create manifest, owners, doctrine, glossary, scope, ontology, causal clock, data, state, occurrence, reference, feature, treatment envelope, gates and security profile.

### WP-08.3 Legacy adapter

Translate old input/state representations into canonical ContextObservation records.

### WP-08.4 Context parity

Compare occurrences, state transitions, references, missingness, known-time and reason codes.

### WP-08.5 Context amendment records

Resolve approved corrections as versioned changes; retain the legacy-observed package when audit requires it.

### WP-08.6 ACL-OS onboarding

Run compiler/onboarding gates and publish generated artifacts without enabling Setup or execution authority.

## Repository-specific target paths

- `lab/11_strategy_factory/contexts/<context_id>/`
- `mql5/Include/AlphaLab/ContextOS/Contexts/<context_id>/`

## Mandatory verification

- ACL context completeness
- known-time and state-machine tests
- golden occurrence/reference replay
- missingness and invalid transition
- legacy adapter contract
- no order/drawing APIs in Context core

## Hostile-review focus

- Context boundary absorbing trigger logic
- duplicated session clocks
- future-aware diagnostic contamination
- source doctrine conflicts

## Commit and patch boundaries

The phase is delivered as the smallest safe vertical patch. Inventory, move-only, semantic refactor, cutover, quarantine and deletion operations remain separate commits. The patch includes root-relative file index, hashes, inventory, manifest, QA, documentation and rollback. Staging uses `git add --pathspec-from-file`; broad staging is forbidden.

## Acceptance gate

Context package compiles through ACL onboarding and matches approved legacy traces with no hidden Setup, drawing or execution authority.

## Failure and rollback

A failed check leaves the migration state unchanged. Partial output is discarded or quarantined. Rollback restores the exact phase input and verifies its manifest; it may not reconstruct lost behavior from prose.

## Handoff

The handoff records source and output digests, completed gates, unresolved blockers, allowed next actions, forbidden actions, owner approvals and residual risk. No downstream phase may infer a missing approval or convert UNKNOWN to PASS.
