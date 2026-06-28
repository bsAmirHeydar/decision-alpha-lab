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

# Level 13 — Validation Matrix

## Purpose

This layer defines the tests that prevent repeated regression. Phoenix must be validated by deterministic cases, not by only visually reacting to one screenshot.

## Test families

### Family A — Node tests

- plateau high emits one node;
- plateau low emits one node;
- equality is not break;
- L increase reduces or merges nodes predictably;
- pending nodes are tagged separately.

### Family B — Hook/ND tests

- 2-node branch is not ND;
- 3-node branch can be ND if retracement passes;
- 4-node branch can be ND if retracement passes;
- 5-node branch rejects current L;
- broken cycle start invalidates Hook;
- Hook does not starve F visibility.

### Family C — Flag body tests

- bullish two-leg body;
- bearish two-leg body;
- Waist equal to Origin is not invalidation;
- Leg2 equal to Leg1 is not break;
- pre-internal Leg2 extension is absorbed.

### Family D — F lifecycle tests

- F1 confirms only after valid internal 1/2 and Leg2 re-break;
- F2 only after confirmed F1;
- F2 undersized cannot authorize F3;
- F3 only after confirmed qualified F2;
- F3 OR completion;
- opposite F1 locks completed F3.

### Family E — Sequence ownership tests

- one phase does not display repeated same-direction F1;
- child candidate death does not kill parent;
- hidden root hides descendants;
- phase reset is explicit and auditable.

### Family F — Canonicalization tests

- same geometry across L gives one main visible object;
- audit preserves hidden duplicates;
- high-L umbrella loses to local lower-L structure when semantic quality is equal;
- hidden reason is never empty.

### Family G — Renderer tests

- clean chart does not show audit labels;
- audit mode does not change logical output;
- index-based curves survive time gaps;
- stale objects are removed.

## Golden chart ranges

Maintain fixed regression chart ranges:

```text
GOLD M1 trend continuation range
GOLD M1 reversal range
GOLD H1 long historical range
Range with weekend/time gap
Range with dense equal highs/lows
Range with a known F1->F2->F3 chain
Range with Hook branch >4 requiring higher L
```

Each range should store:

```text
symbol
timeframe
from_time
to_time
expected node count by L
expected Hook count by L
expected visible F1/F2/F3 count
expected locked F3 count
known screenshot
```

## Acceptance report format

Every patch must add a mini report:

```text
Patch name:
Highest touched layer:
Files touched:
Compile result:
Node tests:
Hook tests:
Flag body tests:
Lifecycle tests:
Ownership tests:
Renderer tests:
Visual smoke result:
Known limitations:
```

## Stop conditions

Stop coding and return to documents/tests when:

- a patch touches more than two semantic layers;
- an upper layer needs to compensate for lower layer uncertainty;
- a screenshot shows a new failure mode unrelated to the patch layer;
- compile passes but audit cannot explain visibility.

## Freeze condition

Validation layer is frozen when every level has at least one deterministic positive test and one negative test.
