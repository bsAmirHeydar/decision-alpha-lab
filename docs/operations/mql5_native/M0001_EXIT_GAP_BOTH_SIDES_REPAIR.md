# M0001 Exit-Gap Both-Sides Repair

This repair locks the event lifecycle around the completed exit window.

## Correct rule

A touch event is completed only after `exit_gap` consecutive candles whose high/low do not intersect the frozen event territory.

The exit can complete on either side of the frozen zone:

- rejection/reversal side,
- break/continuation side.

The event must not be discarded simply because the node price was crossed during the pending touch window.

## Consumption timing

The consume input still controls node lifecycle:

- `DAL_M0001_CONSUME_BY_TOUCH`: a confirmed touch consumes the node at the completed exit candle.
- `DAL_M0001_CONSUME_BY_HUNT`: a confirmed touch does not consume the node unless the node was hunted/broken during that completed touch event. If no hunt occurred, the node stays alive and the next territory cycle is recomputed after the confirmed exit candle.

## RTV

The RTV semantics remain unchanged:

- inside sample starts at event entry,
- the final `exit_gap` confirmation candles are excluded from inside RTV,
- baseline is the same-length window before entry,
- the event is RTV-ready only after exit-gap completion.

## H0002 dependency

H0002 must use the exact M0001 event stream and then label each completed event by close-vs-node at the completed exit candle. Branch labeling must not change the measured event RTV window.
