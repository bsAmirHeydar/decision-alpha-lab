---
id: EXP0018-P06-HANDOFF
title: "P06 Handoff to P07, P08, P11, and P12"
type: implementation-note
status: implemented
project: EXP0018
phase: P06
version: 2.0.0
created: 2026-07-10
updated: 2026-07-10
tags:
  - exp0018
  - p06
  - confirmation
---

# P07

Consumes immutable final results. Only `CONFIRMED` may advance reference lifecycle. Invalidated or unavailable outcomes must not consume or retire references unless doctrine explicitly says so.

# P08

Consumes confirmed results and uses `hunter_reference_price`, `host_bar_close_utc`, and `confirmation_endpoint_price`. P08 must not recalculate confirmation.

# P11

Replays the same candidate and finalization functions chronologically for backfill and missed-close recovery.

# P12

Serializes candidate, result, and event identities and reconciles live/replay equality.
