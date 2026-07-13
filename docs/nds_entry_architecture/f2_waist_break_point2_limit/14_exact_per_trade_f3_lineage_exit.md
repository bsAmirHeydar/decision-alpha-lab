# Exact Per-Trade F3 Lineage Exit

## Status

Canonical hotfix contract for dynamic F3-retest exits.

## Problem corrected

The previous dynamic manager searched the F2 event stream for a confirmed F2 that looked compatible by direction, scale, origin time, waist time, and parent waist time. In overlapping or parallel contexts, that was still too broad. A later or competing F2 could satisfy the same coarse conditions, causing multiple positions to borrow one confirmation node and therefore share an incorrect exit.

The exit must never be selected from the latest same-direction structure or from a common market-level state.

## Authority chain

Every dynamic position now owns a complete immutable lineage:

```text
Position Ticket
→ Order Ticket / Position Identifier
→ Setup Hash
→ Source F1 Event
→ Source F2 Event
→ Source Sequence
→ Source F2 Parent Event
→ Source F2 Origin Node
→ Source F2 Waist Node
→ Direct Child F3
→ Child F3 Leg1 target
→ Child F3 Waist correction gate
```

## Per-trade source identity

At order creation, the setup captures:

- source F1 event ID;
- source F2 event ID;
- source sequence ID;
- source parent sequence ID;
- source F2 parent event ID;
- source F2 chain index;
- source F1 waist node ID and time;
- source F2 origin node ID and time;
- source F2 waist node ID and time;
- initial source F2 Leg2 node ID and time.

These fields are copied into the dynamic-exit context that belongs to the order and later to the exact position ticket. Event IDs are retained as audit snapshots. Because event arrays can be reindexed when an earlier sequence later emits F3, runtime matching uses stable sequence, chain, node ID, and node-time anatomy rather than trusting an old array index alone.

## Exact source F2 matching

A future F2 event may serve the position only if all lineage conditions match:

```text
level = F2
direction = context direction
scale = context scale
sequence_id = source sequence_id
parent_sequence_id = source parent sequence id
chain_index = source F2 chain index
chain_index = source F2 chain index
origin node = source F2 origin node
waist node = source F2 waist node
status = confirmed
f2_can_spawn_f3 = true
```

A same-direction F2 on the same scale is not sufficient.

## Exact child F3 matching

After the exact source F2 is found, the exit manager searches only for its direct child:

```text
F3.parent_event_id = exact source F2.event_id
F3.parent_sequence_id = exact source F2.sequence_id
F3.sequence_id = exact source F2.sequence_id
F3.direction = source direction
F3.scale = source scale
F3.Leg1 node = exact source F2 confirmation node
```

No cross-context borrowing is permitted.

If more than one child appears for the same exact parent, the context fails closed. It does not choose the newest, earliest, widest, or best-looking child.

## Canonical correction gate

The previous generic one-tick adverse movement was only a price approximation. It did not prove that the exact child F3 had formed its own flag correction.

The new correction authority is structural:

```text
Exact child F3 has Leg1
→ Exact child F3 forms its Waist after Leg1
→ correction is confirmed for this position
```

Only then is the dynamic target authorized.

## Dynamic target

The dynamic target is taken from the exact child F3:

```text
Dynamic TP = exact child F3.Leg1.price
```

The target is attached only to the position ticket bound to that context.

## Reward/Risk remains unchanged

Minimum RR and RR-based entry repricing still use the original F2 Leg2 endpoint known at setup creation:

```text
Reference Reward = |Original F2 Leg2 - Entry|
Risk             = |Entry - F1-waist Stop|
Reference RR      = Reference Reward / Risk
```

The future child-F3 target is not used for entry authorization.

## Parallel positions

For two concurrent trades A and B:

```text
Trade A → Source F2-A → Child F3-A → TP-A
Trade B → Source F2-B → Child F3-B → TP-B
```

The following are forbidden:

```text
Trade A → latest bullish F3
Trade B → same latest bullish F3

Trade A → F3-B
Trade B → F3-A
```

## Runtime cost

Fixed-target mode remains F1/F2-only.

Dynamic mode enables only the direct F3 lifecycle already available inside the shared Phoenix sequence engine. It does not enable Hook, renderer, chart objects, CSV, ownership ranking, or AI runtime.

## Failure policy

The manager keeps the position open under its original stop when:

- exact source F2 cannot be reconstructed;
- exact parent F1 cannot be reconstructed;
- exact child F3 does not yet exist;
- child F3 exists but has not formed its Waist;
- multiple children are ambiguous;
- broker TP geometry is temporarily invalid.

It never substitutes another structure.
