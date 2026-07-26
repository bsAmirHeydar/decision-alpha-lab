---
title: "FP Context Architect and Code-Readiness Review Checklist v2"
tags: [exp0019, faerie-protocol, contextual-divergence, obsidian]
status: template
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# FP Context Architect and Code-Readiness Review Checklist v2


## Decision Freeze

- [ ] `fp_owner_decisions.v2.json` validates.
- [ ] Exactly fourteen decisions are owner-confirmed.
- [ ] `FP-DEC-012` is the only open decision.
- [ ] Live execution is disabled while quota consumption is unset.

## Architecture

- [ ] Shared cores are reused without context-specific forks.
- [ ] FP relation/window/policy modules are isolated.
- [ ] M1-only first-sweep is enforced in live and historical modes.
- [ ] Host chart timeframe is resolved and hashed at initialization.
- [ ] New York DST/week/session boundaries pass golden tests.

## Detection

- [ ] All seven relation codes have bullish/bearish fixtures.
- [ ] Calendar-day offsets do not compress missing days.
- [ ] Same-M1 dual touch cannot become ordered divergence.
- [ ] Confirmation at/after session end expires.
- [ ] Protected-touch consumption is side-specific and future-only.

## WW

- [ ] WW is both gate and direct setup.
- [ ] Second-symbol touch neutralizes active WW.
- [ ] Newest active confirmed WW wins.
- [ ] Valid no-WW allows both directions.
- [ ] Weekly data incomplete blocks execution.

## Quota and Execution

- [ ] One pair-global winner per A/L/N session.
- [ ] Earliest M1 hunt is primary ranking.
- [ ] Reservation is atomic.
- [ ] All losers remain visible and ledgered.
- [ ] SELL stop adds one spread before risk sizing.
- [ ] Q12 policy is explicit before live order calls are enabled.

## Evidence

- [ ] Reason-code registry covers every suppressed/invalid state.
- [ ] Drawings rebuild from ledger and never store state.
- [ ] Restart/replay identity parity passes.
- [ ] Traceability has no orphan owner decisions or requirements.

## Navigation

- [[00_EXP0019_MOC|EXP0019 Master MOC]]
- [[38_OWNER_DECISION_FREEZE_V2|Owner Decision Freeze v2]]
- [[33_AMBIGUITY_AND_DECISION_REGISTER|Decision Register]]
- [[40_NORMATIVE_ALGORITHM_SPECIFICATION|Normative Algorithm Specification]]
- [[44_ACCEPTANCE_GATE_FOR_CODING|Acceptance Gate for Coding]]
