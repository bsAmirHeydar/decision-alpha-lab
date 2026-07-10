  ---
  id: EXP0018-TIME-CONTRACT-V2
  title: "قرارداد زمان و تقویم v2"
  type: contract
  status: active
  project: EXP0018
  version: 2.0.0
  created: 2026-07-10
  updated: 2026-07-10
  tags:
    - exp0018
- daye-trader
- implementation-design
  ---
# قرارداد زمان و تقویم v2

- Domain clock: New York local time with explicit UTC conversion.
- Broker time فقط adapter input است.
- تمام boundaryها half-open `[start, end)` طراحی می‌شوند.
- trading day از 18:00 تا 17:00 روز بعد؛ 17:00–18:00 gap.
- event/availability/processing time جدا ثبت می‌شوند.
- DST ambiguity باید با UTC instant حل شود، نه local string.
