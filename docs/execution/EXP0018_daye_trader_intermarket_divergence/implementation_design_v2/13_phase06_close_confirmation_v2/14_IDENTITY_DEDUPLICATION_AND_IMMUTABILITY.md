---
id: EXP0018-P06-IDENTITY
title: "P06 Identity, Deduplication, and Immutability"
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

# Identities

```text
candidate_id = EXP0018|P06|CANDIDATE|<P05 observation_id>
result_id    = EXP0018|P06|RESULT|<P05 observation_id>|<host_close_utc>
host_bar_id  = EXP0018|P06|HOST|<timeframe>|<open_utc>|<symbolA>|<symbolB>
```

A finalized observation ID is remembered even when nonconfirmed results are not published. Duplicate callbacks cannot produce a second result. Confirmed results never transition back to pending or invalidated.
