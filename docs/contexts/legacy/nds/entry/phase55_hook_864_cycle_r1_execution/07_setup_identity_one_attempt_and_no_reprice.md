# 07 — Setup Identity, One Attempt, and No Reprice

## Identity objective

A Hook may expose x3 and later x4. Those are states of one canonical Hook sequence, not two independent trade opportunities.

## Phase 55 setup key

The persistent key includes:

```text
symbol
timeframe
sequence_id
direction
origin_time
Hook family
profile code
entry ratio
```

It deliberately excludes `resolve_time` for Phase 55. Therefore an x3→x4 extension cannot create another setup identity or move an existing pending order.

## Phase 52 compatibility

The terminal/F123 profile retains `resolve_time` in its key because its entry is the current canonical Terminal. Its historical identity behavior is unchanged.

## One-attempt lifecycle

- A paper decision marks the setup used.
- A successfully sent limit marks the setup used.
- A later x4 extension does not reset usage.
- Pending cancellation after Hook death does not permit re-entry for that Hook.
- Restart reloads the account-scoped Global Variable registry.
- `reset_used_setups_on_init` is an explicit research/testing operation and defaults false in the central EA.

## No reprice

An existing pending order is held until fill, structural-death cancellation, operator action, or broker lifecycle outcome. The code does not chase a changed Terminal, recompute a new 86.4 level, or amend Entry after the first accepted setup.

## Race control

The terminal-wide account/magic lock uses `GlobalVariableSetOnCondition`, then rechecks managed pending, managed positions, and foreign same-symbol positions before send. This preserves the original single-exposure invariant across charts.
