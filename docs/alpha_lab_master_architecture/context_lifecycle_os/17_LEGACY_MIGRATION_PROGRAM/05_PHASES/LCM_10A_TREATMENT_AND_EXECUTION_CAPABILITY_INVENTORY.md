---
title: "LCM-10A — Treatment and Execution Capability Inventory"
status: proposed-reference
version: 1.0.0
updated: 2026-07-19
tags: [acl-os, lcm, legacy-migration, refined-roadmap]
phase_id: LCM-10A
master_phase: LCM-10
roadmap_id: LCM_ROADMAP_R1_BALANCED_PARTITION
---
# LCM-10A — Treatment and Execution Capability Inventory

## Purpose

Create a complete and authority-sensitive inventory of payoff, risk, order-request and broker-capable logic before extracting any Treatment or moving an execution path.

## Claim ceiling

`LCM_10A_REFERENCE_ONLY`

This subphase can create migration evidence, contracts, reference implementations, adapters, test assets, registries and bounded consumer changes only as explicitly stated. It cannot create promotion, runtime, live-order or capital authority.

## Scope

- Entry models, limit/market choice, stop, target, cancellation, expiry, volume, partial exits, breakeven, trailing, time exits and reconciliation.
- Direct and indirect OrderSend, CTrade, position, file-ledger, network and broker-state paths.
- Treatment assumptions embedded in Setups, Experts and reports.

## Explicit non-goals

- No order-capable code movement.
- No adapter activation.
- No normalization that changes side, price, volume, tick or stop semantics.

## Entry contract

- LCM-09B Setup registry and treatment bindings.
- LCM-01 order, file and network capability surfaces.
- LCM-02 security-restricted classifications.
- LCM-07 shared engine decisions.

In addition, entry requires a clean or explicitly recorded working tree, the exact upstream handoff digest, the approved baseline plus amendments, named owner and reviewer roles, and explicit UNKNOWN for missing evidence. A missing gate is not inferred from earlier success.

## Engineering workstreams

### WS-01 — Treatment atom inventory

- Catalog every treatment atom and its source, defaults, side behavior, expiry clock, cancellation and management lifecycle.
- Separate descriptive outcome studies from executable treatment rules.

### WS-02 — Capability reachability

- Trace direct and wrapped broker calls from entry points.
- Record dry, paper, shadow, tester and live modes separately.

### WS-03 — Authority map

- Identify who can create request intent, submit, modify, cancel, reconcile and close.
- Mark hidden authority and ambiguous mode switches as blockers.

### WS-04 — Risk and broker assumptions

- Capture point/tick conversion, volume step, spread, stop-level, freeze-level, session and duplicate-decision behavior.

## Required repository artifacts

- treatment_atom_registry.json
- execution_capability_registry.json
- broker_api_reachability.json
- authority_boundary_map.json
- risk_assumption_registry.json
- execution_unknown_queue.json
- LCM10A_TO_LCM10B_HANDOFF.json

Every machine artifact must declare schema version, producer, source digests, generated time semantics, deterministic identity, owner, claim ceiling and validation status. Generated artifacts must not be edited as doctrine.

## Patch boundary

- One patch implements this subphase only.
- Move-only, semantic refactor, consumer cutover, quarantine and deletion remain separated unless this subphase explicitly authorizes one of them.
- The patch must contain a root-relative file index, SHA-256 ledger, artifact inventory, patch manifest, QA report, installation instructions, commit message and rollback instructions.
- Staging must use `git add --pathspec-from-file`; broad staging is forbidden.
- A partial or interrupted build is not deliverable. Publication occurs atomically after clean-overlay verification.

## Mandatory verification

- All order-capable paths are reachable from registry or explicit UNKNOWN.
- Treatment atoms have source hashes and Setup bindings.
- Live/paper/tester distinctions are explicit.
- No source behavior changed.

## Hostile review

- Wrapper hiding CTrade.
- File ledger acting as unreviewed entitlement authority.
- Volume defaults differing by symbol.
- Long/short asymmetry.
- Tester mode bypassing safety checks.

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

- Treatment and execution inventory is closed for the baseline.
- Every capability has an owner and authority class.
- Extraction plan is approved without granting submission authority.

## Handoff contract

- Treatment extraction order.
- Execution boundary violations.
- Security-restricted paths.
- Allowed next action: construct packages and disabled adapters only.

The handoff must include source digest, output digest, completed gates, failed/blocked/unknown dimensions, owner approvals, residual risks, allowed next actions and forbidden actions.
