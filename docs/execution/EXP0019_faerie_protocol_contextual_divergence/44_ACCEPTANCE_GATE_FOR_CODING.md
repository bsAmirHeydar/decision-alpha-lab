---
title: "44 - Acceptance Gate for Coding"
tags: [exp0019, faerie-protocol, contextual-divergence, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# 44 - Acceptance Gate for Coding


## Gate Summary

### Ready to Code Now

- Shared-core compatibility harness.
- V2 contracts and enums.
- Context manifest and configuration hashing.
- New York time/session/week providers.
- M1 window aggregation and data coverage.
- Relation registry and calendar-day N selector.
- Reference lifecycle and protected-touch consumption.
- AL/AN/LN/NA/NL/NN/WW detection.
- Host-chart closed-candle projection.
- Strict same-session confirmation.
- WW neutralization, direct setup, and newest-active gate.
- Always-visible reason-coded drawing.
- Signal identity, ledger, and deterministic restart.
- Pair-global earliest-hunt arbitration and atomic reservation.
- SELL stop plus one spread and risk sizing.
- Paper execution with an explicitly selected test consumption profile.

### Not Canonically Ready for Live

- Permanent session-quota consumption and release after order lifecycle events (`FP-DEC-012`).

## Entry Criteria for Phase 1 Code

- [ ] V2 owner decision JSON validates.
- [ ] Context manifest v2 validates.
- [ ] All shared-core versions are identified.
- [ ] Compatibility tests for existing divergence contexts are available.
- [ ] Relation and reason-code registries are frozen.
- [ ] Golden M1 fixtures exist for all seven relations.

## Exit Criteria for Detection Engine

- [ ] Historical/live M1 replay parity.
- [ ] Calendar-day weekend behavior proven.
- [ ] Same-M1 dual-touch behavior proven.
- [ ] Strict session-close behavior proven.
- [ ] Protected-touch lifecycle proven.
- [ ] WW newest-active resolution proven.
- [ ] Restart rebuild yields identical IDs/events.

## Exit Criteria for Live Execution

- [ ] Owner answers Q12.
- [ ] Decision-set and manifest versions increment.
- [ ] Reservation/consumption/release tests pass.
- [ ] Broker rejection, pending order, partial fill, cancellation, and timeout cases are reason-coded.
- [ ] SELL spread snapshot and risk parity pass in backtest/paper/live diagnostics.

## Coding Prohibitions

- Do not use tick ordering to resolve first sweep.
- Do not compress calendar-day lookback.
- Do not confirm after session boundary.
- Do not hide suppressed signals.
- Do not treat chart objects as state.
- Do not allow live orders when quota consumption is unset.

## Authority Classification

| Classification | Meaning |
|---|---|
| `OWNER_CONFIRMED` | Explicitly selected by the owner in the 15-question decision response. |
| `SOURCE_CONFIRMED` | Directly present in the original Faerie Protocol source package or owner narrative. |
| `ARCHITECTURAL_DERIVATION` | Required to make the confirmed behavior deterministic, modular, testable, or compatible with shared cores. |
| `LEGACY_OBSERVATION` | Behavior observed in `FP 101.mq5`; not automatically canonical. |
| `OPEN_DECISION` | Must not be silently hard-coded. |

Canonical priority is: `OWNER_CONFIRMED` > `SOURCE_CONFIRMED` > reviewed `ARCHITECTURAL_DERIVATION` > `LEGACY_OBSERVATION`.

## Navigation

- [[00_EXP0019_MOC|EXP0019 Master MOC]]
- [[38_OWNER_DECISION_FREEZE_V2|Owner Decision Freeze v2]]
- [[33_AMBIGUITY_AND_DECISION_REGISTER|Decision Register]]
- [[40_NORMATIVE_ALGORITHM_SPECIFICATION|Normative Algorithm Specification]]
- [[44_ACCEPTANCE_GATE_FOR_CODING|Acceptance Gate for Coding]]
