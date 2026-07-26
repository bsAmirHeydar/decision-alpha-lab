---
id: EXP0018-P02-STATE-EVENTS
title: "P02 State, Events and Idempotency"
type: state-machine
status: active
project: EXP0018
---
# State و Event

Engine مالک previous summary، latest probes و refresh clock است.

Events:

- ENGINE_INITIALIZED
- STATUS_CHANGED
- ALIGNMENT_READY
- ALIGNMENT_DEGRADED
- DATA_UNAVAILABLE
- LATEST_COMMON_BAR_ADVANCED

Event ID deterministic است. callback تکراری بدون bar جدید event advance دوم تولید نمی‌کند. `event_time`, `availability_time`, `processing_time` جدا هستند.
