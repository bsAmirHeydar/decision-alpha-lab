---
title: "LCM-16B — Recovery Drill, Final Ledger and Program Closure"
status: proposed-reference
version: 1.0.0
updated: 2026-07-19
tags: [acl-os, lcm, legacy-migration, refined-roadmap]
phase_id: LCM-16B
master_phase: LCM-16
roadmap_id: LCM_ROADMAP_R1_BALANCED_PARTITION
---
# LCM-16B — Recovery Drill, Final Ledger and Program Closure

## Purpose

Prove selected recovery paths, publish the final migration ledger and issue an evidence-bounded closure decision that does not imply trading alpha, production readiness or capital authorization.

## Claim ceiling

`LCM_16B_REFERENCE_ONLY`

This subphase can create migration evidence, contracts, reference implementations, adapters, test assets, registries and bounded consumer changes only as explicitly stated. It cannot create promotion, runtime, live-order or capital authority.

## Scope

- Rollback of selected cutovers.
- Restore from quarantine and deletion archive.
- Final registries and residual risk.
- Program closure decision.

## Explicit non-goals

- No additional deletion.
- No live execution.
- No conversion of UNKNOWN to accepted without explicit waiver and impact analysis.

## Entry contract

- LCM-16A evidence handoff.
- Recovery plans and archives.
- Owner/reviewer approvals.

In addition, entry requires a clean or explicitly recorded working tree, the exact upstream handoff digest, the approved baseline plus amendments, named owner and reviewer roles, and explicit UNKNOWN for missing evidence. A missing gate is not inferred from earlier success.

## Engineering workstreams

### WS-01 — Recovery drills

- Restore representative low-risk and high-risk assets from quarantine/archive.
- Reverse and reapply selected consumer cutovers.
- Verify hashes, locators and behavior.

### WS-02 — Final ledger

- Publish every canonical identity, legacy alias, source disposition, package version, parity status, consumer status, quarantine/deletion record and residual risk.

### WS-03 — Self-sufficiency review

- Confirm an engineer can understand, build, test, locate and recover the system without the original chat.

### WS-04 — Closure decision

- Issue CLOSED, CLOSED_WITH_RESIDUAL_RISK or REOPEN_REQUIRED.
- Record decision authority, evidence digest, limitations and allowed future actions.

## Required repository artifacts

- recovery_drill_reports/
- final_migration_ledger.json
- final_locator_snapshot.json
- residual_risk_register.json
- program_self_sufficiency_review.md
- closure_decision.json
- closure_report.md

Every machine artifact must declare schema version, producer, source digests, generated time semantics, deterministic identity, owner, claim ceiling and validation status. Generated artifacts must not be edited as doctrine.

## Patch boundary

- One patch implements this subphase only.
- Move-only, semantic refactor, consumer cutover, quarantine and deletion remain separated unless this subphase explicitly authorizes one of them.
- The patch must contain a root-relative file index, SHA-256 ledger, artifact inventory, patch manifest, QA report, installation instructions, commit message and rollback instructions.
- Staging must use `git add --pathspec-from-file`; broad staging is forbidden.
- A partial or interrupted build is not deliverable. Publication occurs atomically after clean-overlay verification.

## Mandatory verification

- Recovery drills pass for selected scope.
- Final ledger is complete and digest-bound.
- All residual risks have owner and disposition.
- Closure language respects claim ceiling.

## Hostile review

- Closure treated as alpha validation.
- Archive restoration only checked by file existence.
- Open external consumer omitted.
- Compatibility debt left ownerless.

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

- One explicit closure decision is issued.
- Repository and knowledge system are self-sufficient within documented limitations.
- Runtime, order and capital authority remain governed by separate ACL processes.

## Handoff contract

- No downstream LCM phase.
- Reopening requires a new evidence-bound amendment or migration incident.
- Final decision and artifacts remain immutable; corrections require versioned supersession.

The handoff must include source digest, output digest, completed gates, failed/blocked/unknown dimensions, owner approvals, residual risks, allowed next actions and forbidden actions.
