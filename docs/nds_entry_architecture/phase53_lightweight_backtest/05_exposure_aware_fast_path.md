# Exposure-Aware Fast Path

## No exposure

Both F detection and Hook snapshot construction are required because a new valid F3H/HH setup may appear.

## Pending limit

Hook reconstruction remains enabled. The pending order must still be cancelled when its death boundary is reached, and ownership state must remain current.

## Open position

The entry source is no longer relevant. The only active decision is whether a complete same-direction post-entry F1-F2-F3 chain exists.

Therefore:

```text
open managed position
→ run canonical F detector
→ skip Hook Phase 02 rebuild
→ clear stale snapshot
→ run shared trade core
```

This fast path does not change exit semantics. It removes node and Hook reconstruction while a position owns the strategy.
