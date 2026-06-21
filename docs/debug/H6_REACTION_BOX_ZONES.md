# H6 Reaction Box Zones

Release 112 changes the official H6 chart visual from simple horizontal survivor lines to reaction-zone rectangles.

Contract:

- Raw M0001 nodes only.
- No M0002 branch samples.
- Same-known-time events are never internally ordered.
- A reaction box starts from the known node time and ends at the first future touch.
- The vertical box spans from the node price to the touch extreme.
- For a high node, the touch extreme is the touch candle high; the expected reaction is downward.
- For a low node, the touch extreme is the touch candle low; the expected reaction is upward.
- After touch, reversal confirmation must happen on a later candle. This avoids hidden OHLC sequence assumptions inside the touch candle.
- Once reaction is confirmed, the box color is upgraded if price does not retouch the far edge of the zone for 20 / 50 / 100 candles.

Default colors:

- H20 = red
- H50 = green
- H100 = purple

Key report lines:

- `DAL_H0006_REACTION_BOX_AUDIT`
- `DAL_H0006_REACTION_BOX_H20`
- `DAL_H0006_REACTION_BOX_H50`
- `DAL_H0006_REACTION_BOX_H100`
- `DAL_H0006_NODE_CHART_UPDATE`

Important inputs:

- `InpH6DrawReactionBoxes`
- `InpH6DrawNodeLines`
- `InpH6ReactionAwayBufferPoints`
- `InpH6ReactionZoneEndBufferPoints`
- `InpH6ReactionMinBoxHeightPoints`
- `InpH6ReactionMaxChartObjects`
- `InpH6ReactionBoxFill`
- `InpH6ReactionBoxBack`

The old horizontal lines are still available through `InpH6DrawNodeLines`, but they are off by default in the M0006 standalone expert.


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
