---
id: EXP0018-P03-EVENTS
title: "P03 State, Events and Idempotency"
type: spec
status: active
project: EXP0018
version: 2.0.0
created: 2026-07-10
updated: 2026-07-10
tags:
  - exp0018
  - phase03
  - period-aggregation
---

# State و Event

Eventهای P03 شامل initialize، تغییر status، ready، degraded، unavailable و پیشروی آخرین دوره کامل است. ID از نوع event، event time و period identity ساخته می‌شود. refresh تکراری با همان آخرین bar نباید یک completion جدید بسازد.

`event_time` زمان واقعی پایان دوره، `availability_time` زمان آماده‌شدن تمام داده لازم و `processing_time` زمان اجرای callback است.
