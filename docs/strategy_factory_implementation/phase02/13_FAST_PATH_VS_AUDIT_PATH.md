# Fast Path vs Audit Path

## Fast Path

Direct typed calls:

```text
Host → Runtime → Anatomy Port → Feature Port → Sink
```

## Audit Path

A bounded event bus records what happened without controlling the decision flow.

This split avoids dynamic dispatch chains, unknown subscriber ordering and unbounded queue growth in latency-sensitive code while preserving replay and observability.
