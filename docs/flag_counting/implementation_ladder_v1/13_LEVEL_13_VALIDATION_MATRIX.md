# Phoenix Flag Counting Implementation Ladder V1

This document is part of the implementation ladder for the Phoenix Flag Counting engine.

Global non-negotiables:

- All structural decisions use candle `high` and `low` only.
- `open`, `close`, candle body, candle color, volume, and indicators are not structural inputs.
- Equality is not a break. A level is broken only by a strict pass beyond it.
- The renderer is non-authoritative. It may only draw logical objects emitted by engines.
- Main-chart rendering and audit rendering are separate products.
- Every layer must expose enough audit fields to prove why an object exists.
- A higher layer may never silently repair a lower-layer defect.

# Level 13 — Validation Matrix

## Purpose

This layer prevents repeated regression. Phoenix must be validated by deterministic data and audit baselines, not by only reacting to screenshots.

The active validation registry is:

```text
docs/flag_counting/VALIDATION_CASE_REGISTRY.md
```

## Baseline rule

Do not invent expected counts. A validation case is either:

```text
baseline_required
baselined
```

The first accepted run on a pinned broker/range creates the baseline. Later patches compare against it and explain every intentional delta.

## Test families

### Family A — Node tests

- plateau high emits one node;
- plateau low emits one node;
- equality is not break;
- L increase reduces or merges nodes predictably;
- pending nodes are tagged separately.

Mandatory case: `FC-GC-001`.

### Family B — Hook/ND tests

- 2-node branch is not ND;
- 3-node branch can be ND if retracement passes;
- 4-node branch can be ND if retracement passes;
- 5-node branch rejects current L or requires higher L;
- broken cycle start invalidates Hook;
- Hook does not starve F visibility.

Mandatory case: `FC-GC-002`.

### Family C — Flag body tests

- bullish two-leg body;
- bearish two-leg body;
- Waist equal to Origin is not invalidation;
- Leg2 equal to Leg1 is not break;
- pre-internal Leg2 extension is absorbed.

Mandatory case: `FC-GC-003`.

### Family D — F lifecycle tests

- F1 confirms only after valid internal 1/2 and Leg2 re-break;
- F2 only after confirmed F1;
- F2 undersized cannot authorize F3;
- F3 only after confirmed qualified F2;
- F3 OR completion;
- opposite F1 locks completed F3.

Mandatory cases: `FC-GC-004`, `FC-GC-005`, `FC-GC-006`.

### Family E — Sequence ownership tests

- one phase does not display repeated same-direction F1;
- child candidate death does not kill parent;
- hidden root hides descendants;
- phase reset is explicit and auditable.

Mandatory case: `FC-GC-007`.

### Family F — Canonicalization/audit/export tests

- same geometry across L gives one main visible object;
- audit preserves hidden duplicates;
- high-L umbrella loses to local lower-L structure when semantic quality is equal;
- hidden reason is never empty;
- renderer can be disabled while audit still emits raw/visible objects.

Mandatory cases: `FC-GC-007`, `FC-GC-010`.

### Family G — Renderer tests

- clean chart does not show audit labels;
- audit mode does not change logical output;
- index-based curves survive time gaps;
- stale objects are removed.

Mandatory cases: `FC-GC-008`, `FC-GC-009`.

## Golden chart ranges

Maintain fixed regression chart ranges through the validation registry:

```text
FC-GC-001 through FC-GC-010
```

Each case stores:

```text
symbol
timeframe
from_time
to_time
expected node count by L
expected Hook count by L
expected raw/visible event counts
expected visible F1/F2/F3 count
expected locked F3 count
known screenshot
audit export file
```

## Acceptance report format

Every patch must add a mini report:

```text
Patch name:
Canon file used:
Highest touched layer:
Files touched:
Compile result:
Baseline cases used:
Node tests:
Hook tests:
Flag body tests:
Lifecycle tests:
Ownership tests:
Audit/export tests:
Renderer tests:
Visual smoke result:
Known limitations:
```

## Stop conditions

Stop coding and return to documents/tests when:

- a patch touches more than two semantic layers;
- an upper layer needs to compensate for lower-layer uncertainty;
- a screenshot shows a new failure mode unrelated to the patch layer;
- compile passes but audit cannot explain visibility;
- expected counts are being guessed instead of baselined.

## Freeze condition

Validation layer is frozen when every mandatory case has a pinned broker/range, audit export, screenshot, and expected count baseline.
