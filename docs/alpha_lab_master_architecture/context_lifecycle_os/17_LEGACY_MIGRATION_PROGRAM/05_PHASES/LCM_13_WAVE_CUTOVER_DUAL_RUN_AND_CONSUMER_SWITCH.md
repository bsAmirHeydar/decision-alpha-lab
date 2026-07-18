---
title: "LCM-13 — Wave Cutover, Dual Run and Consumer Switch"
status: proposed-reference
version: 1.1.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration, implementation-phase]
phase_id: LCM-13
---
# LCM-13 — Wave Cutover, Dual Run and Consumer Switch

Migrate consumers family by family under dual-run parity, without big-bang changes or mixed ownership of external side effects.

## Claim ceiling

`CONTROLLED_CUTOVER_REFERENCE_ONLY`

## Phase entry contract

- exact prior-phase handoff and digest;
- current baseline plus all approved amendments;
- phase authority permit and named reviewers;
- closed registries and schemas;
- explicit UNKNOWN for missing evidence.

## Work packages

### WP-13.1 Wave readiness

Verify all identities in the wave have owners, packages, traces, parity, performance, documentation and rollback.

### WP-13.2 Dual-run deployment

Run old and new implementations on identical events with separate namespaces. One declared path owns side effects.

### WP-13.3 Mismatch triage

Classify hard semantic, environment, data, instrumentation, visual-only and accepted-version differences.

### WP-13.4 Consumer switch plan

Switch includes/imports, expert hosts, reports and docs in bounded commits.

### WP-13.5 Observation window

Monitor restart, session transitions, data gaps, performance, object lifecycle and request intent after switch.

### WP-13.6 Cutover decision

Issue APPROVE, HOLD, ROLLBACK or SPLIT_WAVE with reason codes.

## Repository-specific target paths

- `lab/11_strategy_factory/migration/waves/<wave_id>/`
- `reports/lcm/cutover/<wave_id>/`

## Mandatory verification

- legacy/canonical trace comparison
- consumer reference scan
- clean clone compile/test
- rollback rehearsal
- side-effect single-owner assertion
- post-cutover event and performance monitoring

## Hostile-review focus

- mixed old/new state
- one consumer left on legacy path
- dual execution
- environment differences misclassified as semantic
- too-large wave

## Commit and patch boundaries

The phase is delivered as the smallest safe vertical patch. Inventory, move-only, semantic refactor, cutover, quarantine and deletion operations remain separate commits. The patch includes root-relative file index, hashes, inventory, manifest, QA, documentation and rollback. Staging uses `git add --pathspec-from-file`; broad staging is forbidden.

## Acceptance gate

The wave has zero unresolved hard mismatch, all consumers are accounted for, rollback is tested and cutover approval is independent.

## Failure and rollback

A failed check leaves the migration state unchanged. Partial output is discarded or quarantined. Rollback restores the exact phase input and verifies its manifest; it may not reconstruct lost behavior from prose.

## Handoff

The handoff records source and output digests, completed gates, unresolved blockers, allowed next actions, forbidden actions, owner approvals and residual risk. No downstream phase may infer a missing approval or convert UNKNOWN to PASS.
