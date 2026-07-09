---
title: Stage 02 — Store Lifecycle
type: architecture-note
stage: 02
---

# Store Lifecycle

`GT_NewsStore` is the runtime container for all events inside the current configured date window.

## Lifecycle

```text
GT_ResetStore()
  -> GT_LoadSampleEvents() or GT_ParseCalendar()
  -> GT_AddEventEx()
  -> GT_FinalizeStore()
       -> GT_SortEventsByBrokerTime()
       -> GT_MarkRelevance()
       -> GT_UpdateEventStatuses()
       -> GT_UpdateStoreMetrics()
  -> dashboard/timeline/alerts consume store
```

## Store-owned metrics

The store computes these values centrally:

```text
high_count
medium_count
low_count
holiday_count
speech_count
breaking_count
released_count
upcoming_count
active_count
expired_count
relevant_count
visible_count
next_event_index
next_high_index
checksum
```

## Boundary rule

Dashboard, timeline, and alerts may read store metrics, but they must not compute their own event model. Rendering modules can choose presentation, not truth.
