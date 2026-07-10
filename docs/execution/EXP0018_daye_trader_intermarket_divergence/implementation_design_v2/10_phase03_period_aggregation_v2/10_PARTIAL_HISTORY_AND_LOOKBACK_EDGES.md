---
id: EXP0018-P03-PARTIAL-HISTORY
title: "P03 Partial History and Lookback Edges"
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

# تاریخچه ناقص و لبه Lookback

اولین period داخل مجموعه داده ممکن است از وسط Window آغاز شود. فیلد `left_edge_truncated` این وضعیت را ثبت می‌کند. دوره بسته‌ای که آخرین bar موردانتظار را ندارد `right_edge_truncated` می‌شود. هیچ‌کدام با حدس یا forward fill ترمیم نمی‌شوند.

برای تولید reference در مراحل بعد، consumer باید صریحاً مشخص کند فقط `COMPLETE` را می‌پذیرد یا دوره `PARTIAL` را صرفاً برای audit نگه می‌دارد.
