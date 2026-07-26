---
id: EXP0018-P03-FAMILIES
title: "P03 Period Families and Windows"
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

# خانواده‌های دوره

P03 سه خانواده فعال دارد:

- Daily Daye: از 18:00 تا 17:00 روز بعد
- Session: A، L، N، P
- Subcycle: a1 تا p4

`p4` یک tail سی‌دقیقه‌ای است و در لینک‌های chronological همراه سایر Subcycleها رفتار می‌کند. `GAP` دوره معاملاتی نیست و barهای 17:00 تا 18:00 در Core Period Store وارد نمی‌شوند. Weekly فقط در Registry شناخته می‌شود و ساخت آن مسدود است.
