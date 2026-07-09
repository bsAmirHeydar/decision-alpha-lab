# 04 — Date Window Model

## Default

Default remains today only:

```text
InpDaysBack = 0
InpDaysForward = 0
```

This produces:

```text
from = today broker midnight
to   = tomorrow broker midnight
```

## Stored values

The store records:

```text
store.today_start_broker
store.window_from_broker
store.window_to_broker
```

## Event flags

Each event receives:

```text
event.day_start_broker
event.minute_of_day
event.day_offset
event.is_today
event.in_date_window
```

## Important implementation rule

The date window is broker-time based. A calendar event that is technically yesterday in UTC but today in broker time belongs to today on the trader's chart.
