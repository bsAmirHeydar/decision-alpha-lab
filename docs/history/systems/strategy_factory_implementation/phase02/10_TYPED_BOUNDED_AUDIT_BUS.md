# Typed Bounded Audit Bus

The bus is deliberately not the main decision pipeline. It records lifecycle events such as anatomy accepted, snapshot created, runtime failed and audit overflow.

## Design

- Fixed capacity after initialization.
- Monotonic sequence numbers.
- FIFO polling.
- Explicit overflow policy.
- Causal timestamps.
- Stable aggregate and payload identity.

## Overflow

`REJECT_NEW` is recommended for audit-critical runs because it exposes insufficient capacity. `DROP_OLDEST` is useful for high-volume diagnostic telemetry when freshness is more important than complete history. Either policy increments the dropped counter.
