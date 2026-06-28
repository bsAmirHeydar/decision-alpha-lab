# Phoenix Flag Counting Implementation Ladder V1

This document is part of the implementation ladder for the Phoenix Flag Counting engine. Lower layers become frozen foundations before higher layers depend on them.

# Level 03 — Node Identity and Scale

## Purpose

Level 03 makes identity explicit before Hook/ND, F1/F2/F3 lifecycle, ownership, and renderer work. Phoenix must never decide visibility from only `node_id`, `event_id`, or chart object names.

This layer separates:

```text
structural identity = exact replay identity
visual identity     = chart-geometry identity across L variants
phase identity      = ownership window identity
chain identity      = F1 -> F2 -> F3 sequence identity
audit identity      = source/config/pass trace identity
```

## Owned source modules

```text
mql5/Include/FlagCountingPhoenix/FP_Identity.mqh
mql5/Include/FlagCountingPhoenix/FP_IdentityAudit.mqh
mql5/Include/FlagCountingPhoenix/FP_Types.mqh
```

Wiring consumers:

```text
FP_NodeCanonicalizer.mqh
FP_SequenceEngine.mqh
FP_Audit.mqh
FlagCountingPhoenixExperiment.mq5
```

## Identity fields

`FP_Node`, `FP_HookBranch`, and `FP_FlagEvent` carry Level 03 fields:

```text
structural_id
visual_id
phase_id
chain_id
audit_id
source_L
source_mode
is_fail_open
canonical_rank_score
hidden_reason
visible_main
```

For `FP_Node`, `source_L` is represented by the existing `L` field.

## Node identity

Structural node identity:

```text
side + L + anchor_index + normalized_price + plateau_span
```

Visual node identity:

```text
side + anchor_index + normalized_price
```

This allows audit to keep multiple L versions while the main chart can collapse visually identical structures deterministically.

## Event identity

Structural event identity:

```text
level + direction + source_L + chain_index + structural O/A/W/B node ids
```

Visual event identity:

```text
level + direction + chain_index + visual O/A/W/B node ids
```

Phase identity:

```text
symbol + timeframe + direction + phase_start_anchor + phase_boundary_anchor
```

Chain identity:

```text
phase_id + sequence_id
```

Audit identity:

```text
generation_pass + source_mode + config_hash + structural_id
```

## Canonical winner policy

Visibility/canonicalization may use `canonical_rank_score`, but identity assignment is lower-level and deterministic. When two candidates are visually equivalent inside the same phase, the winner preference remains:

1. non-fail-open over fail-open;
2. phase-boundary/Hook-derived root over raw root;
3. higher lifecycle maturity: locked F3 > completed F3 > confirmed F2 > confirmed F1 > post-flag;
4. lower/local L if semantic quality is equal;
5. earlier valid phase ownership;
6. deterministic event id only as final tie-breaker.

Objects with the same visual body but different `phase_id` must not be merged automatically.

## Audit contract

`FP_LEVEL03` must print identity sanity before renderer output is trusted. It reports:

```text
events
structural ids assigned
visual ids assigned
phase ids assigned
chain ids assigned
audit ids assigned
hidden events
hidden events with reason
hooks with identity
duplicate visible visual ids
```

`InpPrintIdentitySamples=true` prints sample identities for events and hooks.

## Forbidden behavior

- Using only `node_id` to detect visual duplicates.
- Using only `event_id` to decide parent/child semantics.
- Merging same-geometry events from different phases.
- Hiding an event without a deterministic `hidden_reason`.
- Letting renderer object names become semantic ids.

## Acceptance tests

### Test 01 — Same visible body across L

Two F1 bodies with identical visual O/A/W/B anchors but different L must produce one visible main-chart object and at least one hidden audit duplicate with `hidden_reason`.

### Test 02 — Different phase same geometry

If two objects have similar geometry but different `phase_id`, they must not be merged automatically.

### Test 03 — Hidden descendant propagation

If a root F1 loses canonical visibility, descendants in the same `chain_id` must not remain visible as orphans.

### Test 04 — Identity sanity

`FP_LEVEL03` must report all emitted events and hooks with identity fields assigned. Hidden events must have non-empty `hidden_reason`.

## Freeze condition

Level 03 is frozen when identity fields exist, are populated before ownership pruning, normalized after pruning, and `FP_LEVEL03 status=ok` is reachable on a normal Phoenix run.
