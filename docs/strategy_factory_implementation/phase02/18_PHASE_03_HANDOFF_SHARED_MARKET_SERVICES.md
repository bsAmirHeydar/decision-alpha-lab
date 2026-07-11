# Phase 03 Handoff — Shared Market Services

Phase 03 must implement the real services behind three ports:

1. Market Data Cache
2. UTC Time Kernel
3. Symbol Specification Cache

It must also add multi-symbol synchronization and new-bar identity.

## Required Outputs

- Cached tick and bar retrieval.
- One canonical bar identity.
- Explicit missing-bar and stale-data states.
- Broker-time to UTC conversion policy.
- DST test fixtures.
- Session and trading-day primitives.
- Symbol specification generation and invalidation.
- Shared synchronization diagnostics.

No anatomy plugin may be integrated before these services are accepted.
