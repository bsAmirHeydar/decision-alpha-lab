---
id: EXP0018-P03-HANDOFF
title: "P03 Handoff to P04 P05 P09 P11"
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

# تحویل به فازهای بعد

- P04 از identity، code و previous links برای resolve رابطه‌های ۲۲گانه استفاده می‌کند.
- P05 فقط Snapshotهای مورد قبول doctrine را به‌عنوان reference/current می‌خواند.
- P09 باکس سشن را از OHLC Session می‌سازد، نه از scan دوباره chart.
- P11 همین pure aggregator را در replay chronological استفاده می‌کند.

هیچ consumer حق ندارد completeness را نادیده بگیرد یا period ناقص را بی‌صدا کامل فرض کند.
