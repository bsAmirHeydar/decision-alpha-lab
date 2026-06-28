# Phoenix Flag Counting Implementation Ladder V1

This document is part of the implementation ladder for the Phoenix Flag Counting engine. The ladder is intentionally layered so that lower layers become frozen foundations before higher layers are allowed to depend on them.

Global non-negotiables:

- All structural decisions use candle `high` and `low` only.
- `open`, `close`, candle body, candle color, volume, and indicators are not structural inputs.
- Equality is not a break. A level is broken only by a strict pass beyond it.
- The renderer is non-authoritative. It may only draw logical objects emitted by engines.
- Main-chart rendering and audit rendering are separate products.
- Every layer must expose enough audit fields to prove why an object exists.
- A higher layer may never silently repair a lower-layer defect.

# Level 04 — Hook / ND Context Engine

## Purpose

Hook/ND is a context and phase-boundary engine. It is not the primary flag detector and it is not a gray decoration generator. It identifies bounded same-side correction cycles that can seed or explain later F1 starts.

## Owned source module

```text
mql5/Include/FlagCountingPhoenix/FP_HookEngine.mqh
```

Shared types:

```text
FP_Types.mqh
```

## Core concept

A Hook is a bounded context from a same-side cycle boundary to an active/resolve same-side node. Inside that bounded context, internal same-side sequences are extracted.

Low-side Hook:

```text
active LOW -> walk backward through LOW nodes -> stop at nearest older strictly lower LOW
```

High-side Hook:

```text
active HIGH -> walk backward through HIGH nodes -> stop at nearest older strictly higher HIGH
```

The boundary node is the cycle start. It is not necessarily counted as branch number 1.

## ND qualification

A Hook context becomes ND-qualified when at least one internal branch has exactly 3 or 4 counted same-side nodes after adaptive L normalization and retracement is satisfied.

```text
1 counted node  => developing Hook, not ND
2 counted nodes => developing Hook, not ND
3 counted nodes => ND candidate
4 counted nodes => ND candidate
5+ in any branch => reject this Hook context at current L; require higher L compression
```

## Internal branch rule

A Hook may contain unlimited internal sequences. The limit is not the number of sequences. The limit is the number of counted nodes inside each sequence.

## Adaptive L rule

If any branch in the Hook context exceeds 4 counted nodes, the current L view cannot emit that Hook/ND as valid. A higher L view must compress the node field and re-evaluate.

## Cycle retracement rule

The Hook/ND retracement is measured from:

```text
cycle_start -> favorable cycle extreme -> resolve node
```

Default ND threshold is above 50% retracement from the extreme back toward the cycle start unless the config explicitly allows below-threshold ND.

## Cycle start not hit rule

If the cycle start is strictly broken before Hook closure, the Hook is invalid.

Low-side Hook invalidation:

```text
later LOW < cycle_start_LOW
```

High-side Hook invalidation:

```text
later HIGH > cycle_start_HIGH
```

Equality does not invalidate.

## Relationship to F1

Hook/ND may propose F1 root candidates. However:

- it cannot delete all valid flag structures;
- it cannot move F semantic origin incorrectly;
- it must tag whether F1 root came from Hook, ND, opposite endpoint, or fail-open raw origin;
- raw fail-open remains a diagnostic safety net until Hook coverage is proven.

## Main-chart rendering policy

Main chart should draw only Hook/ND arcs that explain a visible F1 or are explicitly enabled for diagnostics.

Audit mode may draw all Hook/ND branches.

## Required fields

```text
hook_id
side
L
cycle_start_node
resolve_node
cycle_extreme_node
has_cycle_start
is_cycle_start_broken
branches[]
max_branch_len
nd_qualified
retracement_ratio
source_mode
seeds_visible_f1
visible
hidden_reason
```

## Acceptance tests

### Test 01 — Two-node branch is not ND

A bounded Hook context with only 2 counted nodes must not emit ND label.

### Test 02 — Five-node branch rejects current L

If any internal branch has 5 counted nodes, the current L Hook must be rejected or marked non-qualified. It must not emit a subset 3/4 branch as if valid.

### Test 03 — Cycle start broken

If low-side cycle start is strictly broken before resolve, Hook invalidates. Equal touch does not invalidate.

### Test 04 — F visibility independence

If no Hook-derived root seeds a visible F1, valid raw flag bodies must still be available through fail-open diagnostic mode. The chart must not become purely gray.

## Failure symptoms

- Chart becomes mostly gray.
- Hook arcs appear without any associated visible F1 in main mode.
- F semantic origin moves to cycle boundary incorrectly.
- ND labels appear on 2-node contexts.
- Hook branch counts exceed 4 at a visible L.

## Freeze condition

Hook/ND is frozen only when it can emit a bounded audit list without any renderer involvement and every Hook can explain its cycle start, resolve node, branch list, retracement, and visibility reason.


## Phoenix Level 04 implementation note

Implemented modules:

```text
mql5/Include/FlagCountingPhoenix/FP_HookAudit.mqh
mql5/Include/FlagCountingPhoenix/FP_HookContext.mqh
mql5/Include/FlagCountingPhoenix/FP_HookEngine.mqh
```

`FP_HookEngine.mqh` is now the facade. It emits Hook branches and fills `FP_HookBuildReport`. `FP_HookAudit.mqh` owns `FP_LEVEL04` and `FP_LEVEL04_SEED` logs. `FP_HookContext.mqh` owns cycle-start break validation and bounded-context helpers.

Default audit lines:

```text
FP_LEVEL04      # per-scale bounded context / branch / rejection audit
FP_LEVEL04_SEED # post-pruning Hook -> visible F1 connection audit
```

Level 04 remains audit-first: Hook/ND can propose phase roots, but it cannot erase valid fail-open F bodies and it cannot create F events directly.
