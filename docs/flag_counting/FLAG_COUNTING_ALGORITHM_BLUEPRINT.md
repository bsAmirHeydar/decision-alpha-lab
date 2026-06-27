# Flag Counting Algorithm Blueprint

This document converts the concept specification into implementation-level algorithms.

## 1. Data model

### FC_Node

Fields:

- `int index`
- `datetime time`
- `double price`
- `int kind` where `+1 = high`, `-1 = low`
- `int scale_l`
- `bool confirmed`

### FC_Point

A lightweight copy of a node used inside a sequence:

- `index`
- `time`
- `price`
- `kind`
- `scale_l`
- `valid`

### FC_Sequence

Fields:

- `sequence_id`
- `parent_id`
- `root_id`
- `scale_l`
- `direction`
- `level`: F1/F2/F3
- `phase`: F or ND
- `status`: live/confirmed/invalidated/terminal
- `position`: building_leg1, building_waist, building_leg2, waiting_internal1, waiting_internal2, waiting_rebreak, confirmed, terminal_f3
- `origin`
- `leg1`
- `waist`
- `leg2`
- `internal1`
- `internal2`
- `confirm`
- `invalid`
- `branch_type`: none, normal_internal12, waist_break, terminal_f3
- `body_size`
- `parent_body_size`
- `created_at_index`
- `last_update_index`
- `extension_count`
- `reason`

## 2. Node engine

For every configured scale L:

1. Detect raw swing highs and lows.
2. Compress consecutive same-kind pivots by keeping the more extreme pivot.
3. Preserve alternating high/low structure.
4. Store node stream per scale.

The node engine must be deterministic. Same data and same L must produce the same node stream.

## 3. F1 body construction

### Bullish F1 body

Candidate sequence:

1. Origin = low node.
2. Leg1 = later high node above Origin.
3. Waist = later low node above Origin and below Leg1.
4. Leg2 = later high node above Leg1.

Reject if:

- time ordering fails.
- Waist <= Origin.
- Leg2 <= Leg1.
- Origin is not a legitimate root start.

### Bearish F1 body

Candidate sequence:

1. Origin = high node.
2. Leg1 = later low node below Origin.
3. Waist = later high node below Origin and above Leg1.
4. Leg2 = later low node below Leg1.

Reject if:

- time ordering fails.
- Waist >= Origin.
- Leg2 >= Leg1.
- Origin is not a legitimate root start.

## 4. F1 internal count

### Bullish

After Leg2:

1. Internal 1 = first low after Leg2.
2. Internal 2 = later low lower than Internal 1 but above Waist.
3. If price breaks Leg2 before Internal 2 exists, Leg2 extends; update Leg2 and restart internal search.
4. If price breaks Waist before confirmation, F1 invalidates.
5. Confirmation requires Leg2 rebreak after Internal 2.

### Bearish

After Leg2:

1. Internal 1 = first high after Leg2.
2. Internal 2 = later high higher than Internal 1 but below Waist.
3. If price breaks Leg2 before Internal 2 exists, Leg2 extends; update Leg2 and restart internal search.
4. If price breaks Waist before confirmation, F1 invalidates.
5. Confirmation requires Leg2 rebreak after Internal 2.

## 5. F2 construction

F2 is spawned from parent F1 Internal 2.

### Origin

`F2.origin = F1.internal2`

The engine can continue waiting for F2 if parent F1 is confirmed but Internal 2 is not yet finalized. In that case parent F1 remains the owner of the live segment.

### Body

Body rules are identical to F1, except invalidation and internal branch rules differ.

### Invalidation

F2 invalidates only if Origin is broken.

### Waist break branch

If F2 Waist breaks while Origin remains protected:

- Internal 1 = Waist.
- Internal 2 = waist-breaking node.
- branch type = waist_break.

If Waist does not break, F2 can use normal internal 1/2.

### Extension

F2 can extend beyond its previous Leg2 multiple times. No maximum extension is imposed.

### Confirmation

F2 confirms by rebreaking its own Leg2 before Origin invalidation.

### Size

F2 is valid only if:

`F2.body_size >= F1.body_size`

## 6. F3 construction

F3 is spawned from parent F2 Internal 2.

`F3.origin = F2.internal2`

F3 builds the same two-leg body:

Origin -> Leg1 -> Waist -> Leg2.

Once F3 body is established, the sequence becomes terminal/locked. Post-body movement is special and should be rendered or logged separately.

F3 does not need to satisfy `F3.size >= F2.size`.

F3 can use the same waist-break branch logic as F2 before its terminal body is complete.

## 7. ND / Hook algorithm

ND is detected when an area cannot produce a valid F at that scale or is structurally a hook/cycle.

Algorithm:

1. Start with minimum L, usually 2.
2. Detect node stream inside the suspected hook interval.
3. Count internal nodes.
4. If node count > 4, increase L.
5. Repeat until node count is 3 or 4.
6. Mark that L as the adaptive ND scale.
7. ND is confirmed when a valid F1 forms after it or the 3/4-node hook completes around the extreme.

ND should be represented in the state model, even if the first renderer version only draws F bodies.

## 8. Multi-scale sequence registry

The engine maintains a registry:

- active sequences
- confirmed sequences
- terminal sequences
- invalidated sequences
- ND phases

At every update:

1. Update existing sequences first.
2. Spawn child continuations from confirmed parents.
3. Scan for new F1 roots in unowned or valid reset regions.
4. Deduplicate identical structures across scales.
5. Resolve overlaps inside the same scale.

## 9. Conflict resolver

Two structures are duplicates if they have materially identical:

- direction
- level
- Origin time/price
- Leg1 time/price
- Waist time/price
- Leg2 time/price

Across different scales:

- If identical, keep one representative, usually the clearer/larger scale.
- If structurally different, keep both.

Inside one scale:

- Keep parallel sequences only when they have distinct origins or distinct ownership.
- Reject ownerless middle-start F1 candidates.

Ranking when conflict exists:

1. confirmed > live > invalidated
2. higher F-level in the same chain > lower duplicate
3. larger, cleaner body > smaller noisy body
4. earlier legitimate Origin > random middle Origin

## 10. Renderer algorithm

For each accepted visible sequence:

1. Determine color from direction + status.
2. Determine line width from scale L.
3. Draw straight line Origin -> Leg1.
4. Draw smooth curve Leg1 -> Waist -> Leg2.
5. Draw label F1/F2/F3 near Leg2.
6. Draw numeric labels 1/2 if available.
7. Do not draw post-Leg2 correction lines by default.
8. Remove all owned objects on deinit.

Curve rule:

- Use a Bezier curve from Leg1 to Leg2.
- Control points must make the curve belly tangent to or visually touching the Waist.

## 11. Query API target

The implementation should provide a function equivalent to:

`FC_GetCurrentState(symbol, timeframe, scale_set, mode, out states[])`

Returned state objects must tell strategy code:

- whether the market is in ND or F phase.
- current F-level.
- direction.
- sequence id.
- position inside the F-level.
- invalidation boundary.
- next expected event.
- live/confirmed/terminal status.

## 12. Implementation phases

Phase 1:

- Stable node engine.
- F1 body + F1 internal/confirm/invalidation.
- Body-only renderer.

Phase 2:

- F2 continuation with origin from F1 Internal 2.
- F2 size rule.
- F2 waist-break branch.

Phase 3:

- F3 terminal behavior.
- post-F3 special rendering/logging.

Phase 4:

- Multi-scale sequence registry.
- Conflict resolver.

Phase 5:

- ND/Hook partition engine.
- Adaptive L.

Phase 6:

- Full state query API and audit/replay mode.
