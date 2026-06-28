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

# Level 11 — Canonicalization and Audit

## Purpose

This layer separates raw candidates from main-chart objects. It prevents two opposite failure modes: audit dump charts and over-pruned empty charts.

## Owned source modules

```text
mql5/Include/FlagCountingPhoenix/FP_SequenceEngine.mqh
mql5/Include/FlagCountingPhoenix/FP_Audit.mqh
```

## Pipeline

```text
raw candidates
-> lifecycle validation
-> phase ownership
-> semantic canonicalization
-> visual duplicate pruning
-> main-chart visible list
-> audit log complete list
```

## Main chart vs audit

### Main chart

Shows canonical structures that have semantic ownership and visual clarity.

### Audit

Preserves:

- raw Hook/ND branches;
- raw F bodies;
- rejected objects;
- duplicate losers;
- fail-open roots;
- hidden descendants;
- exact reason each object was hidden.

## Visibility reasons

Every hidden object must have one reason:

```text
hidden_duplicate_geometry
hidden_phase_loser
hidden_orphan_descendant
hidden_unqualified_f2
hidden_developing_hook
hidden_audit_only
hidden_exceeds_main_budget
hidden_config_disabled
```

## Visual duplicate rule

Visual duplicate pruning can remove main visibility when two objects share:

- direction;
- f-level;
- close origin anchor region;
- close leg1 anchor region;
- close waist anchor region;
- close leg2 anchor region;
- same phase or equivalent root context.

It cannot merge across truly different phase ids unless sequence ownership has already classified one as losing.

## Hook audit policy

Hook/ND emits full audit. Main chart draws Hook only when:

- it seeds or explains a visible F1;
- or diagnostic mode explicitly requests all Hook branches.

## Label audit policy

Main labels:

- concise F label;
- optionally ND label if connected to visible F1;
- no raw branch numbers by default.

Audit labels:

- node ids;
- parent ids;
- O/A/W/B ids;
- internal 1/2/3/4;
- Hook branch counts;
- hidden reasons.

## Acceptance tests

### Test 01 — Audit complete, main clean

For a dense range, raw candidate count can be high, but main visible count must be canonical and readable.

### Test 02 — Hidden reason complete

No object may be `visible=false` with empty hidden reason.

### Test 03 — Main labels off

When clean main chart is enabled, internal labels and Hook count labels are absent even if raw audit objects exist.

### Test 04 — Toggle audit

Turning audit labels on should add information without changing logical object emission.

## Failure symptoms

- Internal numbers leak onto main chart.
- Gray Hook curves dominate chart.
- F structures disappear because renderer filters them rather than sequence layer classifying them.
- Duplicate variants differ only by L and all remain visible.

## Freeze condition

This layer is frozen when the same raw candidate set can produce both a clean main chart and a complete audit view using only visibility filters, not different logic.
