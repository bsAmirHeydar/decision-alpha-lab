---
id: EXP0018-P03-LINKS
title: "P03 Previous and Current Period Links"
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

# لینک‌های دوره

هر Snapshot دو لینک دارد:

- `previous_chronological`: دوره قبلی در همان خانواده منطقی
- `previous_same_code`: نمونه قبلی همان code در روز قبلی

برای Subcycle، `p4` با خانواده 90m در یک زنجیره chronological قرار می‌گیرد. بنابراین `a1` می‌تواند previous chronological برابر `p4` داشته باشد. این لینک هنوز رابطه Daye نیست؛ P04 registry بعداً تعیین می‌کند کدام رابطه مجاز است.
