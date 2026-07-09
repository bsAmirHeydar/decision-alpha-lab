# Hook Candidate vs Closed Hook

A Hook candidate is not yet a production Hook.

It becomes a closed Hook only when its final same-side terminal node is confirmed.

## Confirmation

For scale `L`, the terminal node is confirmed after the confirmation window completes. User language:

> if the Hook has an L-node of 5, and five candles do not reach the final node, the node stabilizes and the Hook is closed.

## Important distinction

A raw price extreme is not a closed terminal.

A candidate can move forward if a newer same-side node appears before origin death. The Hook terminal is therefore the last confirmed terminal node, not the latest wick.
