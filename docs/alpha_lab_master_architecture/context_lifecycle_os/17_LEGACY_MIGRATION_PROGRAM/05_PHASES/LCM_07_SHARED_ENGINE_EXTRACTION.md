---
title: "LCM-07 — Shared Engine Extraction"
status: proposed-reference
version: 1.1.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration, implementation-phase]
phase_id: LCM-07
---
# LCM-07 — Shared Engine Extraction

Reduce duplicated primitives only after equivalence is proven, while preserving explicit variants where semantics differ.

## Claim ceiling

`SHARED_ENGINE_EXTRACTION_REFERENCE_ONLY`

## Phase entry contract

- exact prior-phase handoff and digest;
- current baseline plus all approved amendments;
- phase authority permit and named reviewers;
- closed registries and schemas;
- explicit UNKNOWN for missing evidence.

## Work packages

### WP-07.1 Candidate clustering

Use dependency, normalized structure and domain documentation to propose time/session, closed-bar, divergence, reference, state, object, identity and configuration engine candidates.

### WP-07.2 Variance catalog

For every candidate pair record wick/close, equal-high, current-bar, session, DST, consumption, missingness, array indexing and symbol/timeframe differences.

### WP-07.3 Equivalence fixtures

Run the same golden inputs through candidates and require exact parity for claimed-common behavior.

### WP-07.4 Parameterized engine design

Only parameterize true approved variance. Reject giant engines with flags that encode unrelated strategies.

### WP-07.5 Consumer adapters

Replace each consumer incrementally and retain a wrapper for rollback.

### WP-07.6 Shared-engine governance

Assign owner, version, compatibility range and extension contract.

## Repository-specific target paths

- `lab/11_strategy_factory/shared_engines/<engine_id>/`
- `mql5/Include/AlphaLab/ContextOS/Shared/<engine_id>/`

## Mandatory verification

- pairwise parity
- metamorphic boundary cases
- consumer regression
- missing-data fail-closed
- performance and restart
- no domain rule in shared engine

## Hostile-review focus

- premature abstraction
- flag explosion
- subtle current-bar divergence
- consumer-specific side effects
- breaking stable EXP0019 shared-core assumptions

## Commit and patch boundaries

The phase is delivered as the smallest safe vertical patch. Inventory, move-only, semantic refactor, cutover, quarantine and deletion operations remain separate commits. The patch includes root-relative file index, hashes, inventory, manifest, QA, documentation and rollback. Staging uses `git add --pathspec-from-file`; broad staging is forbidden.

## Acceptance gate

Every extracted engine has proven consumers, documented variance and full rollback; non-equivalent candidates remain separate.

## Failure and rollback

A failed check leaves the migration state unchanged. Partial output is discarded or quarantined. Rollback restores the exact phase input and verifies its manifest; it may not reconstruct lost behavior from prose.

## Handoff

The handoff records source and output digests, completed gates, unresolved blockers, allowed next actions, forbidden actions, owner approvals and residual risk. No downstream phase may infer a missing approval or convert UNKNOWN to PASS.
