# 08 — Handoff to Stage 04

## Stage 04 must implement

```text
Chart Timeline Renderer
```

It may use:

```text
event.time_broker
event.minute_of_day
event.day_offset
event.impact
event.kind
event.status
store.window_from_broker
store.window_to_broker
```

It must not implement:

```text
GMT detection
source conversion
UTC conversion
date window recomputation outside store/time engine
```

## Target output

- clean vertical lines
- bottom news tape
- future projection area
- compact labels
- object cleanup by prefix
- no time conversion in renderer
