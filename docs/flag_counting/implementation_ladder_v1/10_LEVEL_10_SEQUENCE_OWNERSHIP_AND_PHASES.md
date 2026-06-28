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

# Level 10 — Sequence Ownership and Phases

## Purpose

This is the layer that prevents the engine from becoming a raw candidate enumerator. It owns the rule that a direction/phase proceeds as F1 -> F2 -> F3, not F1 -> F1 -> F1.

## Owned source module

```text
mql5/Include/FlagCountingPhoenix/FP_SequenceEngine.mqh
```

## Core state machine

For each phase and direction:

```text
empty
-> F1_owner
-> F2_search
-> F2_owner
-> F3_search
-> F3_owner
-> F3_extension
-> locked_by_opposite_F1
-> reset_allowed
```

## Main-chart ownership

Main chart should show the canonical owner sequence for a phase. Audit may keep all candidates.

## Same-direction F1 suppression

Once a same-direction F1 owns a phase, later same-direction F1 roots inside the same phase are not main-chart structures. They may be:

- internal extension;
- child candidate;
- duplicate variant;
- audit-only alternative.

## Phase reset

The strict documented reset is:

```text
opposite completed/confirmed F1 after F3 completion locks previous F3 and resets phase ownership
```

If the user later chooses a looser reset rule, it must be explicitly documented as a config variant. It must not be implied by code.

## Competing roots

When multiple F1 candidates compete for a phase owner, the winner is chosen by semantic maturity and source quality, not by arbitrary drawing order.

Ranking:

1. chain has locked F3;
2. chain has completed F3;
3. chain has confirmed qualified F2;
4. chain has confirmed F1;
5. root is phase-boundary/Hook-derived;
6. root is not fail-open;
7. lower/local L if equal semantic quality;
8. earliest valid phase root;
9. deterministic id tie-break.

## Descendant handling

If a root loses phase ownership, its descendants must not remain on the main chart.

```text
hidden root => hidden F2/F3 descendants
```

Audit must record them.

## Relationship to canonicalization

Sequence ownership is semantic. Canonicalization is visual. Sequence ownership runs before renderer. Visual duplicate pruning must not decide phase truth by itself.

## Required fields

```text
phase_id
phase_direction
phase_owner_root_id
chain_state
next_expected_f_level
phase_reset_reason
owner_rank_score
losing_candidate_ids[]
hidden_descendant_ids[]
```

## Acceptance tests

### Test 01 — One phase one main F1

In a continuous bullish phase with many candidate bullish F1 roots, only one main-chart F1 owner is visible until reset.

### Test 02 — F2 after F1

After F1 owner confirms, next visible same-direction structure should be F2, not another F1.

### Test 03 — F3 after F2

After F2 confirms and qualifies, next visible same-direction structure should be F3.

### Test 04 — Opposite reset

Opposite confirmed F1 after F3 completion locks old F3 and permits a new opposite phase.

## Failure symptoms

- Multiple F1 labels in the same trend leg.
- F2/F3 orphans.
- Turning pruning on makes chart empty; turning it off makes chart noisy.
- Different patches trade off between all gray and all colored chaos.

## Freeze condition

This layer is frozen only when a replay audit can show phase state transitions and explain every hidden same-direction F1.
