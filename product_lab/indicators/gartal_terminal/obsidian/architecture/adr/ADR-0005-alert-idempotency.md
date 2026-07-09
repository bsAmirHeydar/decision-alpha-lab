---
type: adr
product: gartal terminal
status: accepted
language: en
adr: 0005
---

# ADR-0005 — Alert Idempotency

## Decision

Every alert is keyed by event, stage, and channel.

```text
EVENT_ID|STAGE|CHANNEL
```

## Rationale

`OnTimer` runs repeatedly. Without idempotency, the same event can alert every timer tick.

## Consequence

Alert state must store sent keys.

## Enforcement

No alert dispatch is allowed unless the sent-key check passes first.
