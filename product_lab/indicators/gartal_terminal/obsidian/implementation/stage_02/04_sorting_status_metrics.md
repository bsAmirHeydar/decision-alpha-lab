---
title: Stage 02 — Sorting, Status, and Metrics
type: implementation-note
stage: 02
---

# Sorting, Status, and Metrics

## Sorting

Events are sorted by:

1. broker time ascending;
2. impact rank descending for same-minute events;
3. currency alphabetical for deterministic ordering.

This means two USD CPI rows at the same minute remain grouped and red events dominate visual priority.

## Status lifecycle

```text
UPCOMING  -> event time is still in the future
ACTIVE    -> event time has arrived but the event has not expired
RELEASED  -> actual value is present
EXPIRED   -> event is older than the configured expiry window
```

Stage 02 uses:

```text
active window = 15 minutes
expired after = 60 minutes
```

## Metrics

Metrics are recalculated on refresh and timer ticks. The dashboard no longer derives these locally. This avoids UI drift when future filters become interactive.
