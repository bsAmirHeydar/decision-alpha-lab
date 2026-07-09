---
title: Stage 02 — Filter Compatibility
type: implementation-note
stage: 02
---

# Filter Compatibility

Stage 02 keeps the Stage 01 input-level filters but moves visibility logic closer to the event store.

## Active visibility conditions

An event is visible only when:

- it is inside the configured date window;
- its currency is enabled;
- its impact class is enabled;
- speech/holiday/tentative/breaking flags are allowed;
- if symbol-only mode is on, it is relevant to the current chart symbol;
- if past events are hidden, released/expired rows are excluded.

## Symbol relevance

Basic relevance remains simple:

- a symbol containing `EUR` makes EUR news relevant;
- a symbol containing `USD` makes USD news relevant;
- XAU/GOLD/US30/NAS/SPX/DOW are treated as USD-sensitive.

This is intentionally conservative. A more advanced relevance map can be added later without changing `GT_NewsEvent`.
