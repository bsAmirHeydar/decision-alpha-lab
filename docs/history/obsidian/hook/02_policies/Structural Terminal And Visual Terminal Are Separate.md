# Structural Terminal And Visual Terminal Are Separate

The Hook system has two terminal concepts.

## Structural terminal node

Used for Hook-after-Hook continuity:

```text
Hook2.origin_node_id == Hook1.resolve_node_id
```

## Visual terminal price/time

Used for cycle drawing:

```text
arc end = raw terminal price/time
```

This separation prevents raw candle wick geometry from breaking the node-based Hook-after-Hook chain.
