---
title: "LCM-09A — Setup Inventory, Family Registry and Canonical Contract Freeze"
status: proposed-reference
version: 1.0.0
updated: 2026-07-19
tags: [acl-os, lcm, legacy-migration, refined-roadmap]
phase_id: LCM-09A
master_phase: LCM-09
roadmap_id: LCM_ROADMAP_R1_BALANCED_PARTITION
---
# LCM-09A — Setup Inventory, Family Registry and Canonical Contract Freeze

## Purpose

Identify every Setup and embedded opportunity rule, separate semantic variants, and freeze canonical Setup contracts before implementation changes.

## Claim ceiling

`LCM_09A_REFERENCE_ONLY`

This subphase can create migration evidence, contracts, reference implementations, adapters, test assets, registries and bounded consumer changes only as explicitly stated. It cannot create promotion, runtime, live-order or capital authority.

## Scope

- Setup logic in Experts, indicators, includes, decision models, visual suppressors, treatments and execution modules.
- Eligibility, trigger, confirmation, invalidation, cancellation, expiry, abstention and entitlement semantics.
- Setup-to-Context and Setup-to-Treatment relationships.

## Explicit non-goals

- No Setup implementation migration.
- No Setup Factory registration.
- No treatment extraction or consumer switch.
- No merge based only on similar names or outputs.

## Entry contract

- LCM-08C canonical Context registry.
- LCM-01 capability and entry-point survey.
- LCM-02 ownership.
- LCM-03 identities and aliases.
- LCM-04 behavior traces.

In addition, entry requires a clean or explicitly recorded working tree, the exact upstream handoff digest, the approved baseline plus amendments, named owner and reviewer roles, and explicit UNKNOWN for missing evidence. A missing gate is not inferred from earlier success.

## Engineering workstreams

### WS-01 — Embedded Setup discovery

- Locate opportunity decisions hidden in rendering, execution, quota and reporting code.
- Record source function, caller, input Context and output decision.

### WS-02 — Family and variant model

- Separate direction, timeframe, confirmation, continuation/reversal, session, symbol, expiry and entitlement variants.
- Define family relationships without declaring equivalence.

### WS-03 — Contract freeze

- Author context binding, eligibility, trigger, confirmation, invalidation, cancellation, expiry, abstention, entitlement and treatment-binding contracts.
- Make UNKNOWN and no-trade first-class outputs.

### WS-04 — Dependency closure

- Map every active Setup consumer and every Context dependency.
- Block contract acceptance when Context source is non-canonical or ambiguous.

## Required repository artifacts

- setup_inventory.json
- embedded_setup_registry.json
- setup_family_registry.json
- setup_variant_registry.json
- setup_context_binding_registry.json
- setup_contracts/
- setup_unknown_queue.json
- LCM09A_TO_LCM09B_HANDOFF.json

Every machine artifact must declare schema version, producer, source digests, generated time semantics, deterministic identity, owner, claim ceiling and validation status. Generated artifacts must not be edited as doctrine.

## Patch boundary

- One patch implements this subphase only.
- Move-only, semantic refactor, consumer cutover, quarantine and deletion remain separated unless this subphase explicitly authorizes one of them.
- The patch must contain a root-relative file index, SHA-256 ledger, artifact inventory, patch manifest, QA report, installation instructions, commit message and rollback instructions.
- Staging must use `git add --pathspec-from-file`; broad staging is forbidden.
- A partial or interrupted build is not deliverable. Publication occurs atomically after clean-overlay verification.

## Mandatory verification

- Every active Setup decision path is inventoried.
- Variant dimensions are explicit.
- Contract references only canonical Context identities.
- No broker, drawing or quota state is embedded in canonical Setup contract unless approved as Setup entitlement.
- No implementation source changed.

## Hostile review

- Visual suppression mistaken for Setup invalidation.
- Execution quota mistaken for Setup entitlement.
- Confirmation candle drift.
- Legacy default inputs omitted from contract.
- Continuation and reversal variants merged.

The hostile review must attempt to disprove readiness. Aggregate success cannot compensate for a failed non-compensatory gate, and a low-frequency mismatch cannot be discarded merely because overall parity is high.

## Failure semantics

- `FAILED`: a required deterministic gate failed; no handoff may be issued.
- `BLOCKED`: required evidence, owner decision or tool environment is unavailable; affected scope remains unchanged.
- `UNKNOWN`: evidence does not support PASS or FAIL; UNKNOWN is blocking wherever the contract marks the dimension mandatory.
- `PARTIAL`: artifacts exist but acceptance is incomplete; PARTIAL output remains unpublished or is quarantined as diagnostic evidence.
- No failure state authorizes reconstruction of lost behavior from prose.

## Rollback requirements

- Restore the exact upstream input snapshot and verify its manifest.
- Reverse only paths listed in the patch rollback manifest.
- Restore relevant configuration, generated locator, persistent state and compatibility records, not merely source files.
- Re-run the smallest direct verification set after rollback.
- Record rollback outcome and any residual state divergence.

## Acceptance gate

- Setup portfolio is contract-complete or explicitly blocked.
- Each Setup has owner, identity, family, Context binding and contract version.
- Implementation authority is handed to LCM-09B without consumer cutover authority.

## Handoff contract

- Frozen Setup contracts and digests.
- Implementation order and dependency graph.
- Blocked Setup list.
- Allowed actions: implementation, adapter, factory registration in reference mode, parity.

The handoff must include source digest, output digest, completed gates, failed/blocked/unknown dimensions, owner approvals, residual risks, allowed next actions and forbidden actions.
