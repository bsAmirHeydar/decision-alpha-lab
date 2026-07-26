---
tags: [exp0019, faerie-protocol, fp-i08, fp-i09, handoff]
status: normative
phase: FP-I08
version: 1.0.0
last_updated: 2026-07-13
language: en
---
# Handoff to FP-I09

## Contracts FP-I09 may consume

- `WWContext`
- `WWTransitionRecord`
- `WWActiveStack`
- `WWStackEntry`
- `DirectionGateDecision`
- `WWEngineSnapshot`
- `WWCheckpoint`
- `WWRevisionImpact`
- FP-I07 `ConfirmedSignal`

## Semantics FP-I09 must not reinterpret

- The previous completed week is the WW reference source.
- The current week is the WW check interval.
- First-sweep order is M1-authoritative.
- Confirmation is closed-host-candle-authoritative through FP-I07.
- Protected-symbol second touch neutralizes the corresponding confirmed WW.
- Newest active confirmed WW wins.
- Complete data plus no active WW allows both directions.
- Incomplete weekly data fails closed.
- WW is a directly tradeable setup.
- Suppression is an audit decision and never deletes a signal.

## FP-I09 responsibility

FP-I09 owns the unified signal ledger, cross-phase deduplication, pair-session arbitration,
checkpoint composition, deterministic restart, and quota reservation records. It may attach a
WW gate decision to a signal but must not mutate the FP-I08 context or signal evidence.

## Entry conditions

- FP-I08 Python/static gates pass.
- Clean-baseline patch replay passes.
- The two FP-I08 MQL5 entry points compile locally in MetaEditor.
- `FP-DEC-012` remains explicitly unresolved and must not be guessed.

## Navigation

- [[00_FP_I08_DELIVERY_MOC|FP-I08 Delivery MOC]]
- [[42_ACCEPTANCE_GATE|Acceptance Gate]]
- [[../../phases/FP_I09_SIGNAL_LEDGER_DEDUPLICATION_PAIR_SESSION_ARBITRATION_CHECKPOINTS_AND_RESTART|FP-I09 Program Phase]]
