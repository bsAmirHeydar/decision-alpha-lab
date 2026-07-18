---
title: "LCM-10 — Treatment and Execution Separation"
status: proposed-reference
version: 1.1.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration, implementation-phase]
phase_id: LCM-10
---
# LCM-10 — Treatment and Execution Separation

Extract payoff and management semantics from Setup logic and place broker capability behind explicit adapters.

## Claim ceiling

`TREATMENT_AND_EXECUTION_SEPARATION_REFERENCE_ONLY`

## Phase entry contract

- exact prior-phase handoff and digest;
- current baseline plus all approved amendments;
- phase authority permit and named reviewers;
- closed registries and schemas;
- explicit UNKNOWN for missing evidence.

## Work packages

### WP-10.1 Treatment atom inventory

Catalog entry, limit/market choice, stop, target, cancellation, expiry, partial, breakeven, trailing and risk-sizing semantics.

### WP-10.2 Treatment packages

Create versioned treatment contracts and bind them to eligible Setup variants.

### WP-10.3 Normalized request intent

Define side-aware entry/stop/target/volume/spread/expiry/rejection records independent of broker API.

### WP-10.4 Execution adapter isolation

Move direct OrderSend/CTrade/position operations behind capability guards. Context and Setup code may not include these APIs.

### WP-10.5 Dry/paper parity

Compare request intent and lifecycle with submission disabled.

### WP-10.6 Safety controls

Verify duplicate-decision guard, exposure caps, reconciliation, kill switch, stale quote, invalid volume and stop-distance rejection.

## Repository-specific target paths

- `lab/11_strategy_factory/treatments/<treatment_id>/`
- `lab/11_strategy_factory/adapters/mql5/<adapter_id>/`
- `mql5/Include/AlphaLab/ContextOS/Treatments/`
- `mql5/Include/AlphaLab/ContextOS/Adapters/`

## Mandatory verification

- forbidden API scan outside adapters
- dry request golden parity
- long/short symmetry where intended
- spread and tick alignment
- duplicate request denial
- live authority false

## Hostile-review focus

- order router re-evaluating Context
- legacy volume assumptions
- side-dependent stop errors
- paper adapter accidentally calling broker
- capital boundary bypass

## Commit and patch boundaries

The phase is delivered as the smallest safe vertical patch. Inventory, move-only, semantic refactor, cutover, quarantine and deletion operations remain separate commits. The patch includes root-relative file index, hashes, inventory, manifest, QA, documentation and rollback. Staging uses `git add --pathspec-from-file`; broad staging is forbidden.

## Acceptance gate

Treatment semantics are versioned and broker-neutral; all order-capable paths are isolated, dry by default and security-reviewed.

## Failure and rollback

A failed check leaves the migration state unchanged. Partial output is discarded or quarantined. Rollback restores the exact phase input and verifies its manifest; it may not reconstruct lost behavior from prose.

## Handoff

The handoff records source and output digests, completed gates, unresolved blockers, allowed next actions, forbidden actions, owner approvals and residual risk. No downstream phase may infer a missing approval or convert UNKNOWN to PASS.
