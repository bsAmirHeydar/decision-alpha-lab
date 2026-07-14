---
title: "Reference Line Projection"
tags: [exp0019, faerie-protocol, fp-i11, indicator, visual-projection, obsidian]
status: implemented
experiment: EXP0019
context_id: FP-CONTEXT-001
phase_id: FP-I11
phase_version: 1.0.0
last_updated: 2026-07-13
language: en
---

# Reference Line Projection

## Purpose

Projects symbol-local high and low reference levels with source window, symbol, side, state, and reference identity preserved in tooltip and object naming.

## Normative rules

1. Semantic state is accepted only from FP-I03 through FP-I10 contracts.
2. The visual layer may choose geometry, style, visibility, and retention, but may not alter semantic identity or eligibility.
3. Every visible object is instance-scoped, deterministic, reason-coded, and traceable to one semantic ID.
4. Confirmed or terminal evidence is immutable under the same semantic identity.
5. Repeated identical input must produce an unchanged dirty set and must not recreate chart objects.
6. Missing or incompatible evidence fails closed and is surfaced through health/diagnostic state.

## Implementation

- Python reference modules: `phase_i11/python/fp_i11_visual`.
- MQL5 implementation: `mql5/Include/AlphaLab/EXP0019/FaerieProtocol/I11`.
- Production entry point: `EXP0019_FaerieProtocol_Context.mq5`.
- Visual test entry point: `EXP0019_FP_I11_VisualSelfTest.mq5`.
- Projection version: `1.0.0`.
- Runtime authority: `NONE`.
- Visual authority: `CHART_OBJECTS_ONLY`.

## Verification

- Contract validation and deterministic hash tests.
- Dirty-set CREATE/UPDATE/DELETE/NOOP tests.
- Immutable-object negative tests.
- Multi-instance namespace tests.
- Audit suppression visibility tests.
- Object-budget and no-recreate performance tests.
- Static MQL5 authority and entry-point checks.

## Failure behavior

Any conflict between semantic truth and an existing immutable chart object is rejected as `FP_VIS_IMMUTABLE_OBJECT_CHANGED`. The renderer does not silently repaint historical truth.

## Related

- [[../fp_i10/51_HANDOFF_TO_FP_I11|FP-I10 handoff]]
- [[../../phases/FP_I11_INDICATOR_VISUAL_PROJECTION_SESSIONS_REFERENCES_HUNTS_SIGNALS_WW_AND_SUPPRESSION|Program phase]]
- [[55_HANDOFF_TO_FP_I12|FP-I12 handoff]]
