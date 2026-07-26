---
id: EXP0018-P00-IDENTITY
title: "EXP0018 Phase 00 — Identity and Deduplication Doctrine"
type: specification
status: draft
project: EXP0018
version: 2.1.0
created: 2026-07-10
updated: 2026-07-10
owner: Strategy Architect
tags:
  - exp0018
  - daye-trader
  - phase00
  - doctrine-freeze
---

# دکترین هویت و جلوگیری از تکرار

## IDهای لازم

- `period_instance_id`
- `reference_side_id`
- `relationship_instance_id`
- `hunt_observation_id`
- `confirmation_event_id`
- `visual_event_id`
- `ledger_event_id`

## اصول

- ID از randomness ساخته نمی‌شود.
- title یا display label بخشی از identity نیست.
- timezone و boundary version در period identity لحاظ می‌شوند.
- duplicate callback با همان event identity transition جدید ایجاد نمی‌کند.
- restart و historical replay باید همان IDs را بازتولید کنند.

## الگوی پیشنهادی

```text
period_id = type|ny_start|ny_end|calendar_contract_version
signal_id = relationship|refA|refB|currentA|currentB|side|confirm_close
```

قیمت‌ها نباید به‌تنهایی identity باشند؛ اصلاح tick size یا precision نباید ID تاریخی را بشکند.
