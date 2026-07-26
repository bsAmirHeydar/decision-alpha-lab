# Origin Death Before Terminal Confirmation

If price touches or crosses the Hook origin before the final terminal node is confirmed, the structure was never a Hook.

It should not be displayed as a valid Hook.
It should not leak into valid-only mode.
It should not create a production zone later.

## Positive Hook

Death occurs when price touches/crosses the origin below the candidate path before the terminal valley is confirmed.

## Negative Hook

Death occurs when price touches/crosses the origin above the candidate path before the terminal peak is confirmed.

## After closure

Once the terminal node is confirmed, the Hook is historically closed. Later behavior belongs to later lifecycle/zone logic, not to candidate existence.
