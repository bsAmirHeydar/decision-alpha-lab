---
id: AIEOS2-819C6A2A73C8
title: "Alpha Lab Code Style Standard"
type: standard
status: active
domain: engineering
version: 2.0.0
created: 2026-07-10
updated: 2026-07-10
tags:
  - ai-engineering
  - alpha-lab
  - engineering
---
# Alpha Lab Code Style Standard

## Core Style

Code must optimize for correctness, causal clarity, auditability, deterministic replay, and bounded change—not terseness.

### Required

- Explicit names that encode domain meaning.
- One responsibility per function/module boundary.
- Pure functions for calculations where practical.
- A single owner for mutable state.
- Guard clauses for invalid or unavailable input.
- Deterministic IDs for persistent artifacts.
- Stable ordering for outputs and serialized rows.
- Explicit timezone, symbol, timeframe, and availability semantics.
- Error messages that identify operation, entity, timestamp, and expected recovery.

### Prohibited

- Magic numbers without named meaning.
- Boolean parameter clusters that obscure modes.
- Hidden global mutation.
- Silent exception swallowing.
- Implicit conversions at schema boundaries.
- Repeated copy-paste business rules across modules.
- Large aesthetic refactors inside bug fixes.
- Comments that restate syntax while omitting rationale/invariants.

## Function Design

A function should have a verifiable contract:

```text
preconditions
inputs
outputs
state mutation
failure behavior
complexity expectation
```

Long functions are not banned by line count alone, but a function that mixes validation, state mutation, I/O, rendering, and decision logic must be decomposed.

## Naming

- Types/classes: `PascalCase`.
- Functions/methods: language convention, consistently applied per module.
- Constants: explicit project convention; avoid ambiguous single letters outside mathematical/local loops.
- Boolean names: positive predicates such as `is_ready`, `has_history`, `can_execute`.
- IDs: `<DOMAIN>-<TYPE>-<SEQUENCE_OR_HASH>` with documented stability source.
- Time fields include basis: `_utc`, `_ny`, `_broker`, `_bar_open`, `_confirmed_at`.
- Price fields include role: `reference_high`, `clean_stop_price`, `hunter_current_low`.

## Comments and Documentation

Comments explain why, constraints, causal-time assumptions, ownership, and non-obvious compatibility behavior. Public contracts and exported schemas require documentation. A workaround must include the triggering compiler/runtime condition and removal criterion.

## Complexity Budgets

Each algorithm records expected time and memory complexity, maximum history/read size, maximum object count, and failure behavior when the budget is exceeded. Performance optimization cannot change semantics without a separate approved patch.
