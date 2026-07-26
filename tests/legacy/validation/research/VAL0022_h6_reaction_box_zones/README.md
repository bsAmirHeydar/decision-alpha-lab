# VAL0022 — H6 Reaction Box Zones

Goal: validate the H6 chart object logic where a node touch that confirms reversal creates a rectangle from node origin to touch location.

Validation checklist:

1. `sampleCalls=0`, `branchSamplesBuilt=0`, `m0002Calls=0` remain unchanged.
2. `DAL_H0006_REACTION_BOX_AUDIT` is printed.
3. Boxes are drawn when `InpH6DrawReactionBoxes=true`.
4. Horizontal lines are not drawn when `InpH6DrawNodeLines=false`.
5. Red, green, and purple counts correspond to 20, 50, and 100 candles of post-confirmation survival without zone-end retouch.
6. Increasing `InpH6ReactionAwayBufferPoints` reduces confirmed reaction count.
7. Increasing `InpH6ReactionZoneEndBufferPoints` makes the invalidation stricter and may reduce survival.

Recommended fast test:

- `InpH6UseAllAvailableBars=false`
- `InpH6FastDefaultClosedBars=50000`
- `InpH6DrawReactionBoxes=true`
- `InpH6DrawNodeLines=false`
- `InpH6ReactionMaxChartObjects=150`


Release 113 visual correction:
- Draw every confirmed reaction box, not only still-active boxes.
- Box color now reflects the maximum reversal-life stage achieved before the zone end was retouched: under 20 bars = orange if still active / silver if already closed, 20 = red, 50 = green, 100 = purple.
- Horizontal span stays from node-origin known time to first touch time; vertical span stays from node price to first touch extreme.


Release 117 hard visual reset:
- M0006_NodeSurvivalMap now uses a direct L-rule raw-node visual engine.
- Drawing no longer depends on M0001 events, H4 reports, regime labels, reversal/continuation classification, or confirmation events.
- Every touched raw node can draw a rectangle.
- Rectangle width is exactly node origin time to first touch time.
- Rectangle height is exactly node price to touch extreme.
- Color is based only on candles after touch without retouching the zone end.
- `DAL_M0006_DIRECT_VISUAL_AUDIT` reports nodes, touched, drawn objects, object failures, and last object error.


Release 118 visibility and coordinate controls:
- Consumed / zone-end-retouched boxes are hidden by default with `InpH6ShowConsumedBoxes=false`.
- Separate inputs control each layer: pre-H, red, green, purple.
- `InpH6BoxLeftAnchorMode` controls whether the box starts from the node pivot/origin candle or the known/active-from candle.
- `InpH6BoxRightAnchorMode` controls whether the box ends at the touch candle open time or touch candle end time.
- Audit output reports skipped consumed boxes and skipped level-filtered boxes.


Release 119 live level and exact zone box update:
- Node levels are now drawn and updated live on chart rebuild / tick update.
- When `InpH6IncludeLiveBar=true`, the current forming bar is included, so the first touch, zone end, and colors can update in live conditions.
- Box time span stays from the chosen left anchor to the first touch.
- Box price span is the exact touched zone height: zone start (node price) to zone end (first-touch extreme).
- Horizontal node levels are colored with the same stage color logic and extend live until the current bar while the node remains active.
- Consumed nodes remain hidden by default unless explicitly enabled.


Release 120 visual-tester stability fix:
- Default update policy changed to new-bar updates instead of every tick.
- Empty / early visual-tester snapshots no longer delete existing chart objects.
- `InpH6PreserveExistingOnEmptyUpdate=true` preserves current drawings when the tester has not yet built enough bars or no nodes exist.
- The audit now prints `SKIP_PRESERVE_EXISTING` when an update is intentionally skipped without wiping objects.


Release 121 delayed zone-box maturity fix:
- Live node levels may be drawn immediately, but reaction zone boxes are delayed by default.
- `InpH6DrawBoxesOnlyAfterHorizon=true` means a colored zone box appears only after H1/H2/H3 candles have elapsed after the first touch without zone-end retouch.
- `InpH6ShowPreHBoxes=false` by default, so pre-H1 touch boxes are not drawn.
- Origin/touch markers are only drawn when the actual matured zone box is drawn.
- Audit output reports `skippedBoxNotMatured` for touched zones that are not old enough yet.


Release 122 compile fix:
- Fix the touch marker color variable after delayed-box maturity refactor: `c` -> `box_color`.


Release 123 state-machine correction:
- H6 visual is now documented as a candle-by-candle state machine:
  UNTOUCHED_LEVEL -> TOUCHED -> WATCHING_AFTER_TOUCH -> MATURED_DRAW_BOX or CONSUMED.
- Live levels are neutral references; they are no longer colored as maturity signals.
- The colored box is the only official maturity signal.
- A box is drawn only when the node was touched, reversal confirmation is satisfied, the zone end has not been retouched, and the post-touch candle age reaches an input horizon.
- If the age later reaches a higher input horizon, the same node is redrawn with the higher-stage color.


Release 124 no-pre-touch visual policy:
- Official H6 no longer draws any zone or level before first touch by default.
- `InpH6ShowUntouchedLevels=false` is now the official default.
- Touched node levels start at the first-touch candle, not at the node-origin candle, so no object visually exists before the touch.
- Untouched levels can still be enabled only as debug references.
- Matured colored boxes still appear only after the input horizon has passed after touch without zone-end retouch.


Release 125 performance update:
- `OnInit` can still run a larger backfill through `InpBars`.
- Live/visual updates now use `InpH6LiveUpdateBars` instead of rescanning the full history on every update.
- `InpH6UpdateEveryNBars` throttles visual updates; default 1 means once per new candle.
- The audit now prints `runMode`, `fullBarsInput`, `liveUpdateBarsInput`, and `updateEveryNBars`.


Release 126 persistent box policy:
- Matured reaction boxes use stable names: one box per node/side.
- Live updates no longer delete matured boxes.
- If the node reaches a higher post-touch horizon, the existing box is color-updated only.
- Box geometry is not moved/recreated after creation.
- Volatile live levels may still be rebuilt, but persistent boxes remain on chart.
- `InpH6ClearAllObjectsOnInit=true` clears old objects once when the expert starts, not during live updates.


Release 127 boxes-only official mode:
- Official default mode is now boxes-only.
- No text markers, circles, or horizontal levels are drawn in official mode.
- Matured boxes remain persistent on the chart and are never deleted by live updates.
- If a zone reaches a higher horizon, the same box remains and only its color changes.
- `InpH6BoxesOnlyMode=true` forces `draw_node_levels=false`, `show_origin_touch_markers=false`, and `show_untouched_levels=false`.


Release 128 root persistence fix:
- Persistent boxes now use a separate namespace: `DAL_H6_PERSIST_BOX_`.
- Volatile/debug objects use a separate namespace: `DAL_H6_VOL_`.
- Live update cleanup only deletes volatile objects and cannot match persistent box names.
- `InpH6ClearAllObjectsOnInit` now clears volatile/debug objects only.
- Persistent boxes are deleted only when `InpH6ClearPersistentBoxesOnInit=true`.
- Box object names are stable per node/side and update color only on higher horizons.


Release 129 box geometry and color update correction:
- Persistent box names are now stable by node time + node price + side, not by window-local node id.
- This fixes color updates across live windows.
- New box height mode input:
  - `InpH6BoxHeightMode=1` official default: symmetric band around node by percent of first-touch penetration.
  - Example: if touch penetration / zone is 0.90 and `InpH6BoxNodePaddingPct=10`, the box spans 0.09 above and 0.09 below the node.
  - `0` keeps legacy node-to-touch-extreme height.
  - `2` expands node-to-touch-extreme by the same percent.
- Existing persistent boxes can have geometry corrected with `InpH6UpdateExistingBoxGeometry=true` without deleting/recreating them.
- Box color still updates to the highest reached post-touch horizon without zone-end retouch.


Release 130 upsert-only visual lifecycle:
- Live/new-bar updates no longer delete previous objects and rebuild from scratch.
- Official default is `InpH6DeleteVolatileOnUpdate=false`.
- Each update only upserts: create missing objects, update color/geometry/tooltip on existing objects.
- Persistent boxes remain untouched by any routine cleanup and keep stable identity.
- Optional volatile cleanup exists only as an explicit debug mode, not the official mode.


Release 131 compile fix:
- Add missing expert inputs used by the geometry config:
  `InpH6BoxHeightMode`, `InpH6BoxNodePaddingPct`, and `InpH6UpdateExistingBoxGeometry`.
- This keeps release 130 upsert-only lifecycle while exposing the release 129 box geometry controls.


Release 132 official box semantics:
- Box vertical range is one-sided: from the node/touch boundary to the back of the zone.
- With `InpH6BoxHeightMode=1`, thickness is `first_touch_penetration * InpH6BoxNodePaddingPct / 100`.
- Example: penetration 0.90 and pct 10 means zone thickness 0.09. For a HIGH node the box spans node to node+0.09; for a LOW node it spans node-0.09 to node.
- Candle counting starts at the candle after touch. The touch candle itself is not counted.
- The box appears when the requested horizon is reached before the back end of the zone is retouched.
- Existing boxes are never deleted by live updates. Color updates continue by stage/horizon, and geometry can update in-place if enabled.


Release 133 high/low-only official policy:
- Official H6 no longer depends on candle close.
- Touch uses high/low only.
- Zone-back-end retouch uses high/low only.
- Maturity/color updates use candle count starting from the candle after touch.
- `InpH6RequireCloseAwayAfterTouch=false` is now the official default. The close-away check is legacy/debug-only.


Release 134 quiet + backfill maturity fix:
- Disable heavy Journal prints by default with `InpH6PrintAudit=false`.
- Fix historical/backfill logic: if a zone reached a horizon before a later zone-back retouch, the box is drawn and preserved.
- Later retouch no longer prevents drawing a box that would have appeared candle-by-candle.
- Add `docs/history/debug/H6_BOX_ALGORITHM_README.md` as the canonical H6 box algorithm specification.


Release 135 M0001 event-source refactor:
- H6 no longer computes touch, zone, revisit, or invalidation independently.
- H6 draws boxes directly from `DAL_M0001ComputeEvents()` output.
- Box vertical geometry is exactly `event.territory_lower` to `event.territory_upper`.
- Touch is the official M0001 `DAL_CandleIntersectsZone` revisit entry.
- Box color is based on `event.exit_index - event.entry_index` against H6 horizons.
- Persistent boxes are upsert-only and never deleted by live updates.


Release 136 fast box-only reset:
- Replace H6 visual engine with a compact M0001-event-source visualizer.
- Draw every confirmed M0001 event by default, including pre-horizon events, so touched/revisited events do not disappear.
- Remove tick execution path; H6 runs only on init and new candles.
- Remove line/marker/level/debug drawing and keep only persistent upserted rectangles.
- Keep prints disabled by default and reduce audit to one compact optional line.


Release 137 time-origin fix:
- Box horizontal origin is exactly the original node candle time: `event.node_time`.
- Box horizontal destination is exactly the first M0001 touch/revisit candle time: `event.entry_time`.
- This includes wick/shadow-only touches because M0001 entry is based on candle range intersecting the frozen territory.
- H6 no longer uses horizon, exit, or latest-bar time as the rectangle right edge.
- `InpH6BoxRightMode` was removed; the time policy is fixed and official.


Release 138 color update fix:
- Box color age is now based on `event.rtv_sample_length - 1`.
- This matches the official candle count: the touch candle is zero and M0001 exit-gap candles are not counted.
- Existing box colors are monotonic by default: pre -> red -> green -> purple.
- A persistent box never downgrades color during later live windows or partial recalculations.
- `InpH6NeverDowngradeBoxColor=true` controls this behavior.


Release 139 dynamic color tracking:
- H6 box color no longer depends on `event.rtv_sample_length` or `event.exit_index`.
- After a confirmed M0001 touch/revisit creates a box, H6 checks every closed candle after entry.
- Color tracking stops only when the far/back side of the frozen M0001 territory is hit or the purple/highest horizon is reached.
- HIGH node back side = `event.territory_upper`; LOW node back side = `event.territory_lower`.
- The touch candle is zero; the first closed candle after touch is one.
- Persistent box names no longer include `revisit_id`, so the same node/touch box updates reliably across live windows.
- Official default is closed-candle only: `InpH6IncludeLiveBar=false`.


Release 140 valid-zone color lifecycle:
- Zone-back hit before the max/purple horizon invalidates the box.
- If an orange/red/green box already existed and the zone back is hit before purple, it is deleted/hidden because the zone no longer has value.
- If purple is reached before any zone-back hit, the box is considered completed and remains purple; later zone-back hits are not tracked.
- Colors are visible only while the frozen M0001 territory back side has not been hit.
- New input: `InpH6InvalidateOnZoneBackHitBeforeMax=true`.

## Release 141 zone projection test

Run two passes:

1. Full M0001 territory:
   - `InpH6ZoneProjectionMode = DAL_M0006_ZONE_FULL_M0001_TERRITORY`

2. Node-capped near-node map:
   - `InpH6ZoneProjectionMode = DAL_M0006_ZONE_NODE_CAPPED_90_TO_NODE`
   - `InpH6NodeCappedInvalidateOnTouchCandle = true`

Compare how red/green/purple boxes change when the invalidation edge is moved from the old territory back side to the exact node price.
