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

# Level 03 — Node Identity and Scale

## Purpose

This layer defines identity across L-scales. Phoenix failed repeatedly because structures with different `node_id` values but the same visible geometry were treated as independent main-chart structures. This layer separates semantic identity, visual identity, and audit identity.

## Owned source modules

```text
mql5/Include/FlagCountingPhoenix/FP_Types.mqh
mql5/Include/FlagCountingPhoenix/FP_Audit.mqh
```

Consumed by:

```text
FP_HookEngine.mqh
FP_FlagBodyEngine.mqh
FP_SequenceEngine.mqh
FP_Renderer.mqh
```

## Identity classes

### 1. Structural node identity

Unique node identity at one L view:

```text
side + L + anchor_index + price + plateau_span
```

Used for audit and exact engine replay.

### 2. Visual node identity

Node identity as seen on chart:

```text
side + anchor_index + normalized_price
```

Used for main-chart duplicate merging across L.

### 3. Phase identity

The market phase or context that owns structures:

```text
symbol + timeframe + direction + phase_start_anchor + phase_boundary_anchor
```

Used by sequence ownership.

### 4. Chain identity

A specific F1 -> F2 -> F3 sequence:

```text
phase_id + root_event_id
```

### 5. Audit identity

Full trace identity:

```text
engine + generation_pass + source_mode + structural_node_ids + config_hash
```

## Scale policy

Multiple L values may describe the same visual structure. The audit layer keeps them. The main chart must pick one canonical visible version.

## Canonical winner preference

When two candidates are visually equivalent:

1. prefer non-fail-open over fail-open;
2. prefer phase-boundary/Hook-derived root over raw root;
3. prefer higher lifecycle maturity: locked F3 > completed F3 > confirmed F2 > confirmed F1 > post_flag;
4. prefer lower/local L if semantic quality is equal;
5. prefer earlier phase ownership if still valid;
6. use deterministic event id only as final tie-breaker.

## Forbidden behavior

- Using only `node_id` to detect visual duplicates.
- Using only geometry to merge objects that belong to different phases.
- Hiding an event without storing the hidden reason.
- Letting L-scale variants all reach the main chart by default.

## Required fields in every emitted object

```text
structural_id
visual_id
phase_id
chain_id
source_L
source_mode
is_fail_open
canonical_rank_score
visible
hidden_reason
```

## Acceptance tests

### Test 01 — Same visible body across L

Two F1 bodies with identical O/A/W/B anchors but different L must produce one main-chart visible object and at least one audit-hidden duplicate.

### Test 02 — Different phase same geometry

If two objects have similar geometry but belong to different phase ownership windows, they must not be merged automatically.

### Test 03 — Hidden descendant propagation

If a root F1 loses canonical visibility, its F2/F3 descendants must not remain on main chart as orphans.

## Failure symptoms

- Multiple F1 labels stacked in the same movement.
- F2/F3 visible without visible parent.
- Large high-L umbrella structure dominates local structures.
- Rollback changes visual density but not logical output.

## Freeze condition

This layer is frozen when identity fields exist and canonicalization can explain every visible and hidden object deterministically.
