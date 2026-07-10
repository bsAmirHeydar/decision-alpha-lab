  ---
  id: EXP0018-P08-DESIGN-PACKET-V2
  title: "EXP0018 P08 — رویداد تصویری تغییرناپذیر و رسم واگرایی"
  type: phase-design
  status: draft
  project: EXP0018
  version: 2.0.0
  created: 2026-07-10
  updated: 2026-07-10
  tags:
    - exp0018
- phase-design
- core
- p08
  ---
# P08 — رویداد تصویری تغییرناپذیر و رسم واگرایی

## 1. وضعیت و Gate

- Track: **CORE**
- وضعیت فعلی: `not_started`
- Dependencies: `P07`
- Downstream blocked: `P11, P13`

## 2. هدف

confirmed event را به خط Trend روی چارت Hunter تبدیل کند، بدون اینکه renderer منطق بازار را تغییر دهد.

## 3. ورودی‌های authoritative

- immutable confirmed event
- hunter symbol chart
- reference and confirmation coordinates
- label policy

## 4. خروجی‌ها و قرارداد تحویل

- owned trend objects
- major labels WW/DD/PA/AL/LN/NP
- drawing audit

## 5. فایل‌ها و ماژول‌های مالک

- `DAYE_VisualEvent.mqh`
- `DAYE_Drawing.mqh`
- `DAYE_ObjectRegistry.mqh`
- `EXP0018_Daye_Visual_Anatomy.mq5`

## 6. State / Events / APIs پیشنهادی

### State

- state فقط در owner این فاز mutable است.
- تمام snapshotها immutable به مصرف‌کننده بعدی تحویل می‌شوند.
- هر state دارای `schema_version` و identity پایدار است.

### Events

- ورودی eventها chronological و idempotent هستند.
- خروجی eventها دارای `event_time`, `availability_time`, `processing_time` هستند.
- event تکراری با همان identity نباید transition دوم ایجاد کند.

### API boundary

```text
Build/Observe(input snapshot) → typed result + explicit status
Apply(event) → transition result
Serialize(result) → versioned ledger row
```

## 7. Invariants

- فقط hunter chart.
- فقط symbol-local prices.
- confirmed lines immutable.
- object cleanup only owned prefix.

## 8. الگوریتم طراحی‌شده

1. preconditions و data quality را بررسی کن.
2. inputها را به canonical identity تبدیل کن.
3. pure calculation را بدون drawing/file I/O انجام بده.
4. transition را فقط در state owner اعمال کن.
5. typed event و diagnostics صادر کن.
6. consumer بعدی فقط contract را ببیند، نه internals.

## 9. Failure / Partial Data Behavior

- داده ناقص باید `INCOMPLETE/UNAVAILABLE` شود، نه false/no-signal.
- operation failure با error code پایدار ثبت می‌شود.
- exception یا failure adapter حق تغییر truth را ندارد.
- retry باید idempotent باشد.

## 10. تست‌ها

- high-side line
- low-side line
- major label/minor no-label
- historical redraw idempotency
- missing chart open failure

### دسته‌های تست اجباری

- happy path
- exact boundary/equality
- counterexample
- missing/partial data
- duplicate callback/restart
- historical vs live where applicable

## 11. Performance Budget

- loopهای تاریخی bounded هستند.
- هیچ full-history rescan در هر tick مجاز نیست.
- cache ownership و invalidation مشخص است.
- object/file I/O از pure detection جدا است.

## 12. Definition of Ready

- تمام blockerهای وابسته بسته یا feature صریحاً disabled است.
- examples/counterexamples و schema آماده‌اند.
- exact files to add/modify/not-touch مشخص‌اند.
- rollback و acceptance commands نوشته شده‌اند.

## 13. Definition of Done

- visual golden fixtures approved
- no text spam
- object IDs deterministic
- no cross-symbol scale distortion

## 14. ریسک‌ها و hostile review

- object duplication
- wrong chart handle
- renderer back-feeding state
- stale state، future leakage، cross-symbol coordinate و duplicate identity بررسی شوند.

## 15. Non-goals

- order placement و risk sizing
- تغییر خودکار doctrine
- ادغام با EXP0017
- استفاده از Optional برای تغییر Core

## 16. Handoff

خروجی این فاز فقط زمانی به فاز بعدی می‌رود که evidence package شامل spec، tests، compile/runtime evidence، docs، Obsidian و rollback کامل باشد.
