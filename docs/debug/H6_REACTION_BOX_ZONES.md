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
