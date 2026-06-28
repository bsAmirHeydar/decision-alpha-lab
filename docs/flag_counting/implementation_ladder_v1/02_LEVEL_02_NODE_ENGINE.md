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

This layer extracts canonical structural high/low nodes from the Level 01 closed-bar stream. Every later concept depends on node correctness. Hook, flag body, F lifecycle, and sequence ownership are invalid if nodes are unstable.

Level 02 is now split into small modules so debugging can happen at the exact failure layer rather than inside one large monolithic node file.

## Owned source modules

```text
mql5/Include/FlagCountingPhoenix/FP_NodeExtractTypes.mqh
mql5/Include/FlagCountingPhoenix/FP_NodePlateau.mqh
mql5/Include/FlagCountingPhoenix/FP_NodeClearance.mqh
mql5/Include/FlagCountingPhoenix/FP_NodeCanonicalizer.mqh
mql5/Include/FlagCountingPhoenix/FP_NodeScaleList.mqh
mql5/Include/FlagCountingPhoenix/FP_NodeAudit.mqh
mql5/Include/FlagCountingPhoenix/FP_NodeEngine.mqh
```

`FP_NodeEngine.mqh` is the public facade. Other Phoenix layers may call the facade, but should not duplicate plateau or L-clearance logic locally.

Shared model type:

```text
mql5/Include/FlagCountingPhoenix/FP_Types.mqh::FP_Node
```

## Canonical input contract

Level 02 consumes only canonical Level 01 bars:

```text
rates[0] = oldest closed bar
rates[n - 1] = newest closed bar
ArraySetAsSeries(false)
current forming bar excluded by default
```

Level 02 must not call `CopyRates`.

## Canonical node definition

A node is a local structural high or low confirmed by `L` real non-reaching candles on the left and `L` real non-reaching candles on the right.

### High node

For a high candidate at price `P`:

```text
left clearance  = at least L bars with high < P
right clearance = at least L bars with high < P
```

A strict higher high inside a clearance scan rejects the candidate:

```text
high > P + eps => rejection
```

### Low node

For a low candidate at price `P`:

```text
left clearance  = at least L bars with low > P
right clearance = at least L bars with low > P
```

A strict lower low inside a clearance scan rejects the candidate:

```text
low < P - eps => rejection
```

## Equality and plateau rule

Equality is not a break and not clearance.

```text
price == node_price => equal touch
price > high_node_price => strict high break
price < low_node_price  => strict low break
```

Adjacent equal highs/lows are merged into one plateau candidate. The stable anchor convention is:

```text
anchor_index = plateau_end_index
anchor_time  = plateau_end_time
```

Equal-price touches beside the plateau do not count as clearance. The scan continues until it either finds `L` real non-reaching candles, sees a strict break, or reaches the available history boundary.

## Confirmed versus live-pending

Confirmed historical node:

```text
confirmed = true
is_confirmed = true
is_live_pending = false
source = confirmed_history
```

Live-pending candidate:

```text
confirmed = false
is_confirmed = false
is_live_pending = true
source = live_candidate
```

Default Phoenix setting keeps pending nodes out of the canonical F body stream:

```text
InpIncludePendingNodes = false
```

Pending nodes may support Hook/ND live inspection only when explicitly enabled and must remain tagged in audit.

## Canonicalization after raw extraction

Raw nodes are sorted chronologically and re-id'd.

Then Level 02 creates the canonical alternating node stream:

```text
HIGH, HIGH, HIGH run => keep most extreme HIGH
LOW, LOW, LOW run    => keep most extreme LOW
HIGH -> LOW boundary => emit previous run winner
LOW -> HIGH boundary => emit previous run winner
```

The result is the node stream consumed by Hook/F layers.

## Public functions

```text
FP_ExtractNodesForLWithReport(...)
FP_ExtractNodesForL(... legacy-compatible wrapper)
FP_CompressAlternatingExtremeWithReport(...)
FP_CompressAlternatingExtreme(... legacy-compatible wrapper)
FP_BuildCanonicalNodesForScale(...)
FP_BuildScaleList(...)
```

## Required audit logs

When `InpPrintNodeSanity=true`, Phoenix emits per-scale Level 02 logs:

```text
FP_LEVEL02_RAW
FP_LEVEL02_CANONICAL
```

These logs expose:

```text
L
bars
include_pending
epsilon
candidate high/low plateaus
raw emitted nodes
confirmed nodes
pending nodes
high/low counts
left/right rejections
strict-break rejections
equality touches skipped
max plateau width
first/last anchor
same-side compression statistics
```

When `InpPrintNodeSamples=true`, Phoenix also emits node sample lines from raw and canonical streams.

## Forbidden behavior

- Calling `CopyRates` inside the node engine.
- Using close/open/body/color/volume to confirm or reject nodes.
- Treating equality as a strict break.
- Counting equal-price touches as L clearance.
- Emitting untagged pending nodes.
- Letting renderer infer nodes from object geometry.
- Letting Hook/F layers silently rebuild their own node stream.

## Acceptance tests

### Test 01 — Equal high plateau

If adjacent candles have equal highs and no strict higher high rejects them, emit one high plateau candidate, not one per candle.

### Test 02 — Equal low plateau

If adjacent candles have equal lows and no strict lower low rejects them, emit one low plateau candidate, not one per candle.

### Test 03 — Equality not break

If a clearance scan sees equal price, it does not reject the node as a break and it does not count as clearance.

### Test 04 — Strict break rejection

A high candidate is rejected only by `high > P + eps`. A low candidate is rejected only by `low < P - eps`.

### Test 05 — Pending isolation

A right-side scan that has not yet found `L` real clearance bars may create a pending node only when `include_pending=true`. The node must have `source=live_candidate` and `is_live_pending=true`.

### Test 06 — Alternating compression

Same-side runs are compressed to the most extreme node before Hook/F layers see the stream.

### Test 07 — Standalone audit

`FP_LEVEL02_RAW` and `FP_LEVEL02_CANONICAL` must be sufficient to explain why node counts changed without reading renderer output.

## Freeze condition

Level 02 is frozen when:

- Node extraction is only performed through the Level 02 facade.
- Raw extraction and alternating compression both have standalone audit reports.
- Confirmed and pending nodes are explicitly tagged.
- Later modules consume canonical `FP_Node` arrays and do not derive nodes from chart objects or raw candle scans, except for documented boundary-hit checks.
