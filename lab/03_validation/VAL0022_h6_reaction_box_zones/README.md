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


Release 116 logic update:
- Chart drawing no longer waits for H1 maturity; pre-H1 boxes are also drawn.
- Reaction rectangles are now drawn for every touched raw node, with no regime filter.
- A box no longer requires a later explicit away-confirm bar to be drawn.
- Box time span: from node known-time to first touch time.
- Box price span: from node price to the touch extreme on the touch bar.
- Box color is based on the number of candles after the touch during which the far edge of the zone is not retouched.
- Color stages: pre-H1 active=orange, pre-H1 closed=silver, H1=red, H2=green, H3=purple.
