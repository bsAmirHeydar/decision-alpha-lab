# Real Data Requirements

Each symbol must be supplied as a causally ordered JSONL artifact. Every line must contain:

- `symbol`
- `event_time_ms`
- `known_time_ms`
- `bid`
- `tick_size`
- optional `source_sequence`

The two files must use distinct symbols, one stable tick size per versioned source, explicit BID prices, and explicit known times. Paths are local-only; network fetch is denied. The source configuration must declare provider, entitlement, producer version, revision, contract-roll policy, tick-size source, New York timezone, and the availability-time policy.

Continuous futures or contract chains must be normalized upstream under a versioned roll policy. The activation layer does not infer or silently change contract mapping.
