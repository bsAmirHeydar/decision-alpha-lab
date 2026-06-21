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
