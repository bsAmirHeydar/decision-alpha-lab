# README — Hook Raw Terminal and Valid Labels Patch

## Problem

The Hook cycle envelope could stop at the last confirmed Phase01 node even when price had already traded to a more extreme raw price afterward.

For the user's Hook doctrine, this is wrong:

- Positive Hook terminal = the lowest price the Hook has seen.
- Negative Hook terminal = the highest price the Hook has seen.

A confirmed swing node is not enough for visual terminal geometry. Price itself is the terminal authority.

## Fix

Phase 02 now builds structural Hook sequences from nodes, then promotes the visual terminal price/time using raw canonical rates:

- Positive Hook: scans raw `low` after the crown and promotes the endpoint to the lowest raw low.
- Negative Hook: scans raw `high` after the crown and promotes the endpoint to the highest raw high.

The structural `resolve_node_id` is preserved for Hook-after-Hook validity, because Hook-after-Hook is node-continuity based:

```text
previous_hook_terminal_node_id == current_hook_origin_node_id
```

## Valid-only labels

In valid-only mode, only labels of visible valid Hook groups should be shown:

- Immediate Hook after opposing F3.
- Hook-2 after Hook-1.
- Hook-1 only as parent companion of Hook-2.

Debug/raw Hook labels remain hidden unless valid-only mode is disabled.
