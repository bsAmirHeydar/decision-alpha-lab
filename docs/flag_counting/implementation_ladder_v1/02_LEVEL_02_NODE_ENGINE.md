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

# Level 02 — Node Engine

## Purpose

This layer extracts structural high and low nodes from candles. Every later concept depends on node correctness. Hook, flag body, F lifecycle, and sequence ownership are invalid if nodes are unstable.

## Owned source module

```text
mql5/Include/FlagCountingPhoenix/FP_NodeEngine.mqh
```

Shared types:

```text
mql5/Include/FlagCountingPhoenix/FP_Types.mqh
```

## Canonical node definition

A node is a local structural high or low confirmed by `L` candles to the left and `L` candles to the right that do not reach the node price.

### High node

A high node exists when no candle in the left/right confirmation window reaches or exceeds the plateau high except candles that are part of the equal-high plateau itself.

### Low node

A low node exists when no candle in the left/right confirmation window reaches or goes below the plateau low except candles that are part of the equal-low plateau itself.

### Plateau rule

Equal highs or equal lows are one plateau node. The anchor may be chosen as the last equal touch if that is the project convention, but the choice must be documented and stable.

## Equality rule

Equality is not a break.

```text
price == node_price => touch/equal, not break
price > high_node_price => strict high break
price < low_node_price => strict low break
```

## Pending nodes

Hook live inspection may observe a currently forming same-side node that is not fully confirmed yet. This must be explicitly tagged:

```text
is_confirmed = false
is_live_pending = true
```

Confirmed node logic and live-pending inspection must not be mixed silently.

## Required node fields

```text
node_id
side: HIGH | LOW
L
anchor_index
anchor_time
price
plateau_start_index
plateau_end_index
is_confirmed
is_live_pending
source: confirmed_history | live_candidate
```

## Forbidden behavior

- Using close to confirm or reject nodes.
- Treating equal high/equal low as a break.
- Creating multiple nodes for one plateau.
- Recalculating node identity differently per module.
- Letting renderer infer nodes from object geometry.

## Acceptance tests

### Test 01 — Equal high plateau

If three adjacent candles have equal high and no surrounding candle strictly exceeds it, emit one high node, not three.

### Test 02 — Equality not break

If a later candle equals a prior high node, the high is not broken. A break requires strict greater-than.

### Test 03 — L stability

Increasing L may remove nodes or merge context, but cannot change the price of a plateau node already identified at smaller L unless the plateau definition itself changes.

### Test 04 — Live pending isolation

A pending node may feed Hook live inspection, but cannot be treated as confirmed input to F2/F3 unless the relevant layer explicitly allows it.

## Failure symptoms

- F structures jump after new candles because node identity was not stable.
- Hook counts duplicate equal highs/lows.
- F invalidates when price only equals a boundary.
- Backfill picks different origins in different modules.

## Freeze condition

This layer is frozen when node extraction has standalone audit output and all later modules consume only `FP_Node` objects, not raw candle highs/lows directly, except for strict boundary hit checks that are documented.
