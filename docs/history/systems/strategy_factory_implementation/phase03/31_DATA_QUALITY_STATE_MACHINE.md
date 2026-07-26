---
title: "Data Quality State Machine"
status: implemented
phase: PHASE_03
language: en
tags:
  - strategy-factory
  - phase03
  - mql5
  - market-services
---

# States

Every market object exists in an explicit quality state:

```text
UNKNOWN
→ VALID
→ STALE
→ VALID after trusted refresh

VALID
→ GAPPED
→ VALID only after verified rebuild

ANY
→ INVALID
```

`MISSING` represents absence rather than deterioration. `DESYNCHRONIZED` is a relationship state between otherwise valid series.

# Transition rules

- A new validated source observation may move `UNKNOWN` or `MISSING` to `VALID`.
- Time alone may move a tick or series from `VALID` to `STALE`.
- A close-time discontinuity moves a bar series to `GAPPED`.
- Contract failure moves only the rejected observation to `INVALID`; it does not overwrite the last valid cache item.
- A gap flag is sticky. Only a trusted rebuild that proves continuity can clear it.
- Synchronization readiness is recomputed from current series generations.

# Consumer behavior

Research diagnostics may persist every state. Decision-capable paths may consume only `VALID` data unless a future capability contract explicitly authorizes a weaker state for a non-price feature.

# Why state is explicit

Without quality state, consumers infer validity from nulls, zero prices, or return codes. That creates inconsistent behavior across strategies. Explicit quality allows later context snapshots to record not only feature values but also the provenance and confidence of the market inputs that created them.

# Audit requirement

Every transition away from `VALID` should eventually emit a typed audit event with symbol, timeframe, previous generation, new state, and reason. Phase 03 provides state and telemetry; persistent event-ledger integration follows later.
