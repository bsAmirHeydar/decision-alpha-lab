---
id: EXP0018-P01-06-SESSION-AND-SUBCYCLE-WINDOWS
title: "EXP0018 P01 — Session and Subcycle Windows"
type: specification
status: implemented-awaiting-metaeditor-compile
project: EXP0018
phase: P01
version: 2.2.0
created: 2026-07-10
updated: 2026-07-10
owner: Quant Engineering
tags:
  - exp0018
  - daye-trader
  - phase01
  - time-kernel
---


# سشن‌ها

| ID | Interval |
|---|---|
| A | [18:00, 24:00) |
| L | [00:00, 06:00) |
| N | [06:00, 12:00) |
| P | [12:00, 17:00) |

# زیرسایکل‌ها

هر boundary نیمه‌باز است. equality همیشه به period جدید تعلق دارد.

| ID | Interval |
|---|---|
| a1 | [18:00, 19:30) |
| a2 | [19:30, 21:00) |
| a3 | [21:00, 22:30) |
| a4 | [22:30, 24:00) |
| l1 | [00:00, 01:30) |
| l2 | [01:30, 03:00) |
| l3 | [03:00, 04:30) |
| l4 | [04:30, 06:00) |
| n1 | [06:00, 07:30) |
| n2 | [07:30, 09:00) |
| n3 | [09:00, 10:30) |
| n4 | [10:30, 12:00) |
| p1 | [12:00, 13:30) |
| p2 | [13:30, 15:00) |
| p3 | [15:00, 16:30) |
| p4 | [16:30, 17:00) |

`p4` دقیقاً ۳۰ دقیقه است.

