---
title: "LCM-16A — Full Regression, MQL5 Matrix, Parity and Security Audit"
status: implemented-reference
version: 1.0.0
updated: 2026-07-23
tags: [acl-os, lcm, legacy-migration, refined-roadmap]
phase_id: LCM-16A
master_phase: LCM-16
roadmap_id: LCM_ROADMAP_R1_BALANCED_PARTITION
---
# LCM-16A — Full Regression, MQL5 Matrix, Parity and Security Audit

## Purpose

Run the complete closure evidence matrix across registries, Python, schemas, MQL5, replay, cross-language parity, documentation and authority boundaries without overstating unavailable tool evidence.

## Claim ceiling

`LCM_16A_REFERENCE_ONLY`

This subphase can create migration evidence, contracts, reference implementations, adapters, test assets, registries and bounded consumer changes only as explicitly stated. It cannot create promotion, runtime, live-order or capital authority.

## Scope

- All active canonical packages and consumers.
- Quarantine, deprecation, deletion and locator registries.
- Clean checkout/build/test environments.

## Explicit non-goals

- No new migration or deletion.
- No production or capital authorization.
- No PASS inferred from unavailable MetaEditor, MT5, broker or external environment.

## Entry contract

- LCM-15C clean-clone handoff.
- Final active inventory and closure test matrix.

In addition, entry requires a clean or explicitly recorded working tree, the exact upstream handoff digest, the approved baseline plus amendments, named owner and reviewer roles, and explicit UNKNOWN for missing evidence. A missing gate is not inferred from earlier success.

## Engineering workstreams

### WS-01 — Registry and architecture audit

- Validate identity uniqueness, locator completeness, dependency direction, authored/generated boundaries and unresolved legacy status.

### WS-02 — Python and schema regression

- Compile and run direct, migration and ACL regression suites.
- Validate JSON/YAML/schema and deterministic manifests.

### WS-03 — MQL5 evidence matrix

- Compile approved modules in available MetaEditor environments, run tester/golden replay where available and record exact environment.
- Mark unavailable evidence UNKNOWN.

### WS-04 — Parity

- Run final known-time, state, event, decision, request and visual parity samples across representative/high-risk families.

### WS-05 — Security and authority

- Scan forbidden APIs, capability guards, secrets, network paths, runtime generation and order/capital authority.

### WS-06 — Documentation integrity

- Validate canonical navigation, links, redirects, release lookup and self-sufficiency.

## Required repository artifacts

- closure_test_matrix.json
- registry_conformance_report.json
- python_regression_report.json
- schema_validation_report.json
- mql5_compile_matrix.json
- strategy_tester_matrix.json
- cross_language_parity_report.json
- security_authority_audit.json
- documentation_integrity_report.json
- LCM16A_TO_LCM16B_HANDOFF.json

Every machine artifact must declare schema version, producer, source digests, generated time semantics, deterministic identity, owner, claim ceiling and validation status. Generated artifacts must not be edited as doctrine.

## Patch boundary

- One patch implements this subphase only.
- Move-only, semantic refactor, consumer cutover, quarantine and deletion remain separated unless this subphase explicitly authorizes one of them.
- The patch must contain a root-relative file index, SHA-256 ledger, artifact inventory, patch manifest, QA report, installation instructions, commit message and rollback instructions.
- Staging must use `git add --pathspec-from-file`; broad staging is forbidden.
- A partial or interrupted build is not deliverable. Publication occurs atomically after clean-overlay verification.

## Mandatory verification

- All available required tests pass.
- Unavailable evidence explicitly UNKNOWN with impact.
- Zero active unresolved legacy source unless accepted residual.
- No hidden runtime/order/capital authority.
- Closure evidence reproducible from clean checkout.

## Hostile review

- Claiming MQL5 parity from static mirror.
- Skipping high-risk families because low-risk samples pass.
- Compatibility wrapper excluded from forbidden API scan.
- Residual external consumer ignored.

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

- Closure evidence set is complete enough for decision.
- Failures and UNKNOWNs are mapped to closure impact.
- No automatic closure.

## Handoff contract

- Signed closure evidence digest.
- Residual risk and blocker list.
- Allowed next action: recovery drill and human closure decision.

The handoff must include source digest, output digest, completed gates, failed/blocked/unknown dimensions, owner approvals, residual risks, allowed next actions and forbidden actions.
## Implementation status — 2026-07-23

LCM-16A is implemented as audit package `CLOSUREAUDIT_5EEC97304039BFF3AAAFB57605961BA2`. The package validates the exact LCM-15C handoff, records a 242-path AIEOS baseline amendment against the 2,168-path lock set, orchestrates 60 governed regression suites, validates repository JSON/YAML/schema definitions, inventories 2,559 MQL5 source files, and publishes parity, security, documentation, hostile-review, determinism, rollback and handoff evidence.

Current deterministic result: 3,975 tests passed and zero deterministic product failures in the supplied source-archive environment. Three LCM-12A evidence tests remain environment-blocked because two Git LFS objects are pointers rather than materialized objects. Real MetaEditor compilation, Strategy Tester/golden replay, terminal-compiled parity and out-of-repository external-consumer reachability remain mandatory `UNKNOWN/BLOCKED`. Therefore the LCM-16A implementation package is valid, while the closure decision is `BLOCKED`; automatic Legacy Migration Program closure is forbidden.

