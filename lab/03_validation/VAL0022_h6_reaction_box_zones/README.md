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
