  ---
  id: EXP0018-P05-DESIGN-PACKET-V2
  title: "EXP0018 P05 — تشخیص هانت و Snapshot مرجع"
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
- p05
  ---
# P05 — تشخیص هانت و Snapshot مرجع

## 1. وضعیت و Gate

- Track: **CORE**
- وضعیت فعلی: `blocked_by_doctrine`
- Dependencies: `P04`
- Downstream blocked: `P06, P07`

## 2. هدف

واقعیت touch-only hunt را برای هر نماد، side و reference به‌صورت pure fact تولید کند؛ بدون تأیید و رسم.

## 3. ورودی‌های authoritative

- signal definition
- reference period snapshot
- current period snapshot
- symbol-local extrema

## 4. خروجی‌ها و قرارداد تحویل

- DAYE_HuntObservation
- hunter/protected candidates
- high/low touch flags
- first touch time

## 5. فایل‌ها و ماژول‌های مالک

- `DAYE_HuntTypes.mqh`
- `DAYE_HuntDetector.mqh`
- `DAYE_ReferenceResolver.mqh`
- `EXP0018_Daye_Hunt_Anatomy.mq5`

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

- equality counts as hunt.
- close beyond level لازم نیست.
- hunt fact با divergence confirmation یکی نیست.
- cross-symbol price comparisons ممنوع است.

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

- equal touch
- one-sided high
- one-sided low
- double hunt same candle
- no touch
- missing symbol data

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

- pure function fixtures pass
- direction mapping approved
- hunter/protected role output deterministic

## 14. ریسک‌ها و hostile review

- using stale reference
- side inversion
- intrabar repaint assumptions
- stale state، future leakage، cross-symbol coordinate و duplicate identity بررسی شوند.

## 15. Non-goals

- order placement و risk sizing
- تغییر خودکار doctrine
- ادغام با EXP0017
- استفاده از Optional برای تغییر Core

## 16. Handoff

خروجی این فاز فقط زمانی به فاز بعدی می‌رود که evidence package شامل spec، tests، compile/runtime evidence، docs، Obsidian و rollback کامل باشد.
