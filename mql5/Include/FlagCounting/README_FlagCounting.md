# MQL5 Flag Counting Module

This include layer is intended to become the reusable MQL5 implementation of the Flag Counting engine.

## Authoritative design

Read these documents first:

- `docs/flag_counting/FLAG_COUNTING_CONCEPT_SPEC_V3.md`
- `docs/flag_counting/FLAG_COUNTING_ALGORITHM_BLUEPRINT.md`
- `docs/flag_counting/FLAG_COUNTING_GLOSSARY.md`

## Module target

The MQL module should not be a loose F-pattern scanner. It should expose a reusable state engine:

- Build multi-scale nodes.
- Maintain parallel sequences.
- Spawn F2 from parent F1 Internal 2.
- Spawn F3 from parent F2 Internal 2.
- Track ND/Hook phases.
- Return queryable current state.
- Render clean body-only drawings.
- Emit detailed logs only when debug is enabled.

## Rendering contract

Default rendering:

- Origin -> Leg1: straight line.
- Leg1 -> Waist -> Leg2: one smooth curve.
- F label and 1/2 numeric labels only.
- Direction and status define four colors.
- Larger scales use thicker lines and slightly larger labels.

## Implementation warning

The old implementation attempts produced blank charts or overdrawn charts because they mixed candidate scanning with sequence state. The next implementation must be sequence-first.
