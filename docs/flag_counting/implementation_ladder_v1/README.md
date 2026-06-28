# Phoenix Flag Counting Implementation Ladder V1

## Purpose

This package defines a layered implementation plan for the Phoenix Flag Counting engine. It is subordinate to `docs/flag_counting/FLAG_COUNTING_CURRENT_CANON.md`, which is the active source of truth and conflict resolver. It exists because repeated direct code edits created alternating failure modes: one patch fixed visibility but broke Hook ownership; another fixed Hook rendering but starved F structures; another cleaned labels but mixed audit with main-chart behavior.

The solution is not another tactical patch. The solution is a strict implementation ladder.

Each layer has:

- a responsibility boundary;
- source-file ownership;
- input and output contracts;
- forbidden dependencies;
- acceptance tests;
- freeze criteria;
- failure symptoms.

A layer is not allowed to move upward until its acceptance tests pass. A higher layer is not allowed to compensate for a lower-layer bug. If a lower-layer bug appears, implementation returns to that layer, fixes it, updates its tests, and then re-runs all dependent layers.

## Directory

1. `00_GOVERNANCE_AND_FREEZE_PROTOCOL.md` — how the ladder must be used, committed, frozen, and rolled back.
2. `01_LEVEL_01_CANDLE_STREAM_AND_TIMEBASE.md` — bar stream, candle indexing, and time-gap handling.
3. `02_LEVEL_02_NODE_ENGINE.md` — high/low node extraction, plateaus, L, confirmation, and equality.
4. `03_LEVEL_03_NODE_IDENTITY_AND_SCALE.md` — node identity, visual identity, scale identity, and multi-L ownership.
5. `04_LEVEL_04_HOOK_ND_CONTEXT_ENGINE.md` — bounded Hook/ND context, internal sequences, adaptive L, and cycle closure.
6. `05_LEVEL_05_FLAG_BODY_ENGINE.md` — invariant two-leg body: Origin -> Leg1 -> Waist -> Leg2.
7. `06_LEVEL_06_INTERNAL_COUNT_ENGINE.md` — internal 1/2/3/4 after flag body.
8. `07_LEVEL_07_F1_LIFECYCLE_ENGINE.md` — F1 candidate, post-flag, confirmation, invalidation.
9. `08_LEVEL_08_F2_LIFECYCLE_ENGINE.md` — F2 authorization, backfill, size contract, survival after child failure.
10. `09_LEVEL_09_F3_EXTENSION_AND_LOCK_ENGINE.md` — F3 authorization, OR completion, extension, opposite lock.
11. `10_LEVEL_10_SEQUENCE_OWNERSHIP_AND_PHASES.md` — F1 -> F2 -> F3 chain ownership and phase resets.
12. `11_LEVEL_11_CANONICALIZATION_AND_AUDIT.md` — duplicate control, main/audit separation, deterministic winners.
13. `11_5_LEVEL_11_5_RAW_AUDIT_EXPORT.md` — raw audit/export/report contract before renderer trust.
14. `12_LEVEL_12_RENDERER_AND_LABEL_LAYOUT.md` — visual contract, object names, curves, label stacks, debug modes.
15. `13_LEVEL_13_VALIDATION_MATRIX.md` — tests, golden cases, screenshots, regression packs.
16. `14_LEVEL_14_RELEASE_ROLLBACK_AND_DEBUG_PROTOCOL.md` — release process, rollback, MetaTrader cleanup, failure triage.
17. `15_MODULE_INTERFACE_CONTRACTS.md` — module API boundaries and data objects.
18. `16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX.md` — exact build order and acceptance checklist.
19. `17_AMBIGUITIES_TO_RESOLVE_BEFORE_CODE.md` — resolved decision record; no longer an open-blocker list.

## Source modules covered

Target Phoenix modules:

```text
mql5/Include/FlagCountingPhoenix/FP_BarSnapshot.mqh
mql5/Include/FlagCountingPhoenix/FP_TimebaseTypes.mqh
mql5/Include/FlagCountingPhoenix/FP_SeriesContract.mqh
mql5/Include/FlagCountingPhoenix/FP_Timebase.mqh
mql5/Include/FlagCountingPhoenix/FP_Types.mqh
mql5/Include/FlagCountingPhoenix/FP_NodeEngine.mqh
mql5/Include/FlagCountingPhoenix/FP_HookAudit.mqh
mql5/Include/FlagCountingPhoenix/FP_HookContext.mqh
mql5/Include/FlagCountingPhoenix/FP_HookEngine.mqh
mql5/Include/FlagCountingPhoenix/FP_FlagBodyEngine.mqh
mql5/Include/FlagCountingPhoenix/FP_InternalCountEngine.mqh
mql5/Include/FlagCountingPhoenix/FP_SequenceEngine.mqh
mql5/Include/FlagCountingPhoenix/FP_Renderer.mqh
mql5/Include/FlagCountingPhoenix/FP_Audit.mqh
mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5
```

## Core rule

Do not code from screenshots. Screenshots are symptoms. Code from the layer contract and then use screenshots as regression evidence.

## Implementation policy

The next code rewrite must follow this order:

```text
Level 00 -> Level 01 -> Level 02 -> Level 03 -> Level 04 -> Level 05 -> Level 06 -> Level 07 -> Level 08 -> Level 09 -> Level 10 -> Level 11 -> Level 11.5 -> Level 12 -> Level 13 -> Level 14
```

Any patch that touches a higher level must declare which lower-level invariants it assumes. If those lower-level invariants are not tested, the patch is not acceptable.
