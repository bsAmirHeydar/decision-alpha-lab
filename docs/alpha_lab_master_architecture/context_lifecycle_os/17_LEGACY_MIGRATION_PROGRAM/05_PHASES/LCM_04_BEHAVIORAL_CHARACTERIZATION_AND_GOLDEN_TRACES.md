---
title: "LCM-04 — Behavioral Characterization and Golden Traces"
status: proposed-reference
version: 1.1.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration, implementation-phase]
phase_id: LCM-04
---
# LCM-04 — Behavioral Characterization and Golden Traces

Capture what legacy systems actually do before any semantic refactor. Characterization records both correct and undesirable behavior while keeping intended owner doctrine separate.

## Claim ceiling

`LEGACY_BEHAVIOR_CHARACTERIZATION_ONLY`

## Phase entry contract

- exact prior-phase handoff and digest;
- current baseline plus all approved amendments;
- phase authority permit and named reviewers;
- closed registries and schemas;
- explicit UNKNOWN for missing evidence.

## Work packages

### WP-04.1 Trace schema and emitters

Define stable event, state, time, reason, drawing and dry execution-request records. Add instrumentation without changing decision logic.

### WP-04.2 Golden case catalog

Create positive, negative, no-trade, expiry, invalidation, restart, history expansion, missing bar, DST, session boundary, timeframe change, symbol change, multi-instance and duplicate-tick cases.

### WP-04.3 Legacy observed baseline

Run legacy compile units in controlled environments and preserve raw journals plus normalized traces.

### WP-04.4 Intended-correction register

When legacy behavior conflicts with approved doctrine, record OBSERVED and INTENDED versions separately. Corrections require a new semantic version and later dedicated commit.

### WP-04.5 Known-time audit

Record event time, data availability, bar closure and reference availability for every decision-bearing event.

### WP-04.6 Visual and request intent capture

Capture drawing anchors/object lifecycle and normalized order-request intent with broker submission disabled.

### WP-04.7 Replay stability

Repeat traces after restart and clean environment setup. Non-determinism becomes a blocker or explicit legacy defect.

## Repository-specific target paths

- `lab/11_strategy_factory/migration/packets/<id>/golden/`
- `lab/11_strategy_factory/migration/parity/legacy_traces/`
- `reports/lcm/characterization/`

## Mandatory verification

- same input produces same normalized trace
- event ordering is stable
- future data injection is detected
- restart and history expansion cases preserve state policy
- drawing anchors and dry request fields are captured
- known bugs remain labeled rather than silently corrected

## Hostile-review focus

- instrumentation changing timing
- tester/live differences
- unavailable historical data
- unstable random IDs
- current-bar behavior hidden by visual output

## Commit and patch boundaries

The phase is delivered as the smallest safe vertical patch. Inventory, move-only, semantic refactor, cutover, quarantine and deletion operations remain separate commits. The patch includes root-relative file index, hashes, inventory, manifest, QA, documentation and rollback. Staging uses `git add --pathspec-from-file`; broad staging is forbidden.

## Acceptance gate

All critical paths have owner-reviewed golden cases and replay-stable traces; observed defects and intended corrections are separated; no canonical rewrite has begun.

## Failure and rollback

A failed check leaves the migration state unchanged. Partial output is discarded or quarantined. Rollback restores the exact phase input and verifies its manifest; it may not reconstruct lost behavior from prose.

## Handoff

The handoff records source and output digests, completed gates, unresolved blockers, allowed next actions, forbidden actions, owner approvals and residual risk. No downstream phase may infer a missing approval or convert UNKNOWN to PASS.
