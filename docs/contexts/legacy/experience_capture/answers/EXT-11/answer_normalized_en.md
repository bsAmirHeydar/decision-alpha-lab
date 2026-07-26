# EXT-11 — Normalized Interpretation

## Core Claim

Extreme is a reversal/contrarian entry at the entry-point level.

This does not necessarily mean the whole higher-timeframe scenario is contrarian.

It means the local execution action is contrarian to the immediate move that is reaching the node.

The entry is made with a limit order near the near-death zone, and the stop is placed behind the node.

## Extreme as Local Reversal Entry

Extreme is not a breakout or momentum entry.

It is a limit-based reversal entry.

The local structure is:

```text
price moves toward the anchor node
price reaches or approaches the near-death zone
limit entry is waiting against that local move
stop is placed behind the node
```

So the entry relation is:

```text
entry_direction_relation_to_current_move = CONTRARIAN_AT_ENTRY_LEVEL
```

## Stop Placement Confirms the Logic

The stop goes behind the node.

This confirms that the trade expects the node/near-death area to reject or repel price.

If price crosses beyond the cycle-origin node, EXT-06 applies:

```text
one-point penetration beyond the cycle-origin node invalidates the anchor
```

So the node is the invalidation boundary.

## Not a Continuation Entry Family

Within the definition given here, Extreme itself should not be treated as a continuation entry.

Continuation entries may exist in the system, such as post-F1 continuation entries, but those are separate entry families.

Extreme remains:

```text
limit-based local reversal entry
```

Continuation logic should be modeled under a different entry family, not mixed into Extreme.

## Higher-Timeframe Context Can Still Be Aligned

Even though Extreme is contrarian at the local entry level, it may still align with a larger scenario.

Example concept:

```text
higher timeframe wants buy
lower timeframe moves down into an Extreme buy zone
local entry is contrarian to the downward move
but aligned with the higher-timeframe bullish scenario
```

So the system needs to distinguish:

```text
local entry direction relation
higher-context scenario alignment
```

This prevents confusion.

## Current Move Definition

For Extreme, the current move should be defined locally as the immediate move into the anchor node.

Suggested definition:

```text
current_move = the local price movement that approaches the Extreme anchor node
```

Then:

```text
buy Extreme = limit buy against a local downward move into a lower node
sell Extreme = limit sell against a local upward move into an upper node
```

This is a local entry-level definition, not a full-market prediction.

## Dataset Consequence

Future Extreme records should store:

```text
entry_order_type
entry_direction
current_move_direction
entry_direction_relation_to_current_move
stop_behind_node
higher_context_alignment
```

For Extreme, expected value:

```text
entry_order_type = LIMIT
entry_direction_relation_to_current_move = CONTRARIAN_AT_ENTRY_LEVEL
stop_behind_node = true
```

## AI Relevance

AI should not relabel Extreme as continuation simply because the higher timeframe is aligned.

The correct representation is two-layered:

```text
local entry relation = contrarian
scenario relation = can be aligned with higher context
```

This allows the model to know that the execution mechanism is reversal-style while the strategic thesis may still be continuation or alignment at a higher scale.

## Short Formal Statement

Extreme is a limit-based reversal entry at the local entry-point level. It enters against the immediate move into the anchor node, with the stop behind the node. Continuation entries may exist elsewhere in NDS, but they should be treated as separate entry families rather than redefining Extreme.
