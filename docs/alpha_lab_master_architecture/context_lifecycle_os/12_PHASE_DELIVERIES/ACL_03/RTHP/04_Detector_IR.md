---
title: RTHP Detector IR
status: compiled
version: 1.0.2
---
# Detector IR

- Detector digest: `sha256:643d1e6aedaaef33c73de4b04fd23d94ba291af8a0e8f9e9942e73059c9334fb`
- IR version: `1.0.0`
- Execution model: `DECLARATIVE_EVENT_GUARD_IR`
- Generated code allowed: `false`

## State projection

The compiled detector preserves the canonical states:

- `BOTH_SIDES_TOUCHED`
- `DIVERGENCE_CONFIRMED`
- `ONE_SIDE_TOUCHED`
- `REFERENCE_EXHAUSTED`
- `UNCONFIRMED`
- `UNKNOWN`
- `UNTOUCHED_BOTH`

## Guard policy

Each transition is represented as declarative guard text with a stable transition identifier, priority, and unknown-guard policy. The IR cannot execute Python, MQL5 order APIs, network operations, subprocesses, or dynamic code.

## Determinism

The state machine remains single-transition-or-fail. Transition ordering and identity are content-addressed and tied to Context version `1.0.2`.
