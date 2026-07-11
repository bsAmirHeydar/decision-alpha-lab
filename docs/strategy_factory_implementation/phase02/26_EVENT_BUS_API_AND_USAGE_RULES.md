---
title: "Event Bus API and Usage Rules"
---

# Event Bus API and Usage Rules

## What Belongs on the Bus

- Runtime lifecycle records.
- Anatomy accepted or rejected.
- Snapshot accepted or rejected.
- Health state changes.
- Telemetry and replay notifications.

## What Does Not Belong on the Bus

- Primary candidate price calculation.
- Risk authorization.
- Broker request construction.
- Mutable shared strategy state.
- Unbounded binary payloads.
- Data that has no stable aggregate identity.

## Envelope Semantics

`aggregate_id` identifies the event, snapshot, candidate or runtime aggregate. `source_id` identifies the producer. `occurred_at` describes when the underlying event happened; `known_at` describes when it became observable. `payload_hash` binds the envelope to an immutable payload artifact or in-memory canonical form.

## Sequence Semantics

Sequence is local to one initialized bus generation. It is suitable for ordering within a runtime session, not as a globally unique event ID. Global identity comes from the canonical contract IDs.
