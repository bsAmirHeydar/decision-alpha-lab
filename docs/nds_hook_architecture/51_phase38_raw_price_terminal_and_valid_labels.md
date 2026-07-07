# 51 — Phase 38: Raw Price Terminal and Valid Hook Labels

## Doctrine

A Hook cycle endpoint is a price terminal, not only a node terminal.

For a positive Hook:

```text
terminal = lowest raw low seen after the Hook crown
```

For a negative Hook:

```text
terminal = highest raw high seen after the Hook crown
```

The confirmed node stream is still used for structural sequence counting, Hook-after-Hook continuity, and seed ownership. But the envelope endpoint must respect raw price.

## Reason

A Phase01 node requires structural confirmation. A raw price extreme may appear before that node is confirmed. If the visual Hook envelope waits only for confirmed nodes, the cycle can appear to stop early even though price has already moved farther into the Hook terminal side.

## Implementation

Phase02 now uses the rate-aware entrypoint:

```text
FP_HookP02BuildSequencesWithRates(...)
```

The builder first constructs node-owned Hook sequences, then promotes terminal price/time from canonical rates:

```text
positive -> min(raw low after crown)
negative -> max(raw high after crown)
```

The `resolve_node_id` remains structural. The `resolve_time` and `resolve_price` represent the promoted visual terminal when raw price extends beyond the structural node.

## Valid-only labels

When valid-only mode is enabled, production labels are allowed only for:

1. Immediate Hook after opposing F3.
2. Hook-2 after Hook-1.
3. Hook-1 only as the visible parent companion of Hook-2.

No standalone unqualified Hook sequence labels should leak into production view.
