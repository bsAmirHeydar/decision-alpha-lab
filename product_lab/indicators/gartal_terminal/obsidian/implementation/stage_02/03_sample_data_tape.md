---
title: Stage 02 — Sample Data Tape
type: implementation-note
stage: 02
---

# Sample Data Tape

Stage 02 introduces a deterministic full-day macro tape.

## Coverage

The sample tape contains:

- USD red events;
- same-minute red events;
- EUR/GBP/CAD/AUD/NZD/JPY/CHF/CNY events;
- low, medium, high, and holiday impacts;
- speech events;
- tentative events;
- breaking red-news proxy events;
- actual/forecast/previous value combinations;
- previous-day and next-day rows for date-window testing.

## Default behavior

Default inputs still show only the current day:

```text
InpDaysBack = 0
InpDaysForward = 0
InpShowPastEvents = true
```

Changing `InpDaysBack` or `InpDaysForward` reveals the surrounding sample rows.

## Breaking-news proxy

`Unscheduled Presidential Remarks` is marked as `is_breaking=true`. This is not yet real-time news ingestion. It is a product-design placeholder so UI, filtering, and alert logic can be designed around red unscheduled events before Stage 08.
