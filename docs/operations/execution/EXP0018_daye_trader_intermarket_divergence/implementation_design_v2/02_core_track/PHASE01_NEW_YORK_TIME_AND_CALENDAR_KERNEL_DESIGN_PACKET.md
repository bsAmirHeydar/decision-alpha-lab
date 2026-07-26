  ---
  id: EXP0018-P01-DESIGN-PACKET-V2
  title: "EXP0018 P01 — هسته زمان نیویورک و تقویم"
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
- p01
  ---
# P01 — هسته زمان نیویورک و تقویم

## 1. وضعیت و Gate

- Track: **CORE**
- وضعیت فعلی: `foundation_exists_requires_validation`
- Dependencies: `P00`
- Downstream blocked: `P02, P03, P10, P11`

## 2. هدف

یک ساعت دامنه‌ای قطعی برای Broker→UTC→New York، DST، روز معاملاتی، سشن و زیرسایکل بسازد.

## 3. ورودی‌های authoritative

- Broker server time
- Manual offset fallback
- US DST rules
- 18:00 Daye day boundary

## 4. خروجی‌ها و قرارداد تحویل

- NY timestamp
- trading_day_key
- session_id A/L/N/P/NONE
- subcycle_id a1..p4/NONE
- period boundary events

## 5. فایل‌ها و ماژول‌های مالک

- `DAYE_Time.mqh`
- `DAYE_PeriodRegistry.mqh`
- `DAYE_Types.mqh`
- `EXP0018_Daye_Time_Foundation.mq5`

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

- تمام منطق زمانی بر NY domain time است.
- 17:00–17:59 سشن NONE است.
- p4 دقیقاً 30 دقیقه باقی می‌ماند.
- تبدیل زمان idempotent است.

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

- DST spring/fall transition
- 18:00 day rollover
- 00:00/06:00/12:00/17:00 boundaries
- p4 16:30–16:59
- manual offset parity

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

- 0 compile error/warning
- golden timestamp fixtures pass
- weekly boundary policy برای W مشخص است یا W صریحاً disabled می‌ماند.

## 14. ریسک‌ها و hostile review

- Broker offset drift
- ambiguous bars around DST
- holiday/session gaps
- stale state، future leakage، cross-symbol coordinate و duplicate identity بررسی شوند.

## 15. Non-goals

- order placement و risk sizing
- تغییر خودکار doctrine
- ادغام با EXP0017
- استفاده از Optional برای تغییر Core

## 16. Handoff

خروجی این فاز فقط زمانی به فاز بعدی می‌رود که evidence package شامل spec، tests، compile/runtime evidence، docs، Obsidian و rollback کامل باشد.
