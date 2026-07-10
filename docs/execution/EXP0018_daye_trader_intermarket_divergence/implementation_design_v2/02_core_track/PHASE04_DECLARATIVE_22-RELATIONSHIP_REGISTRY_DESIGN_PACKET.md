  ---
  id: EXP0018-P04-DESIGN-PACKET-V2
  title: "EXP0018 P04 — رجیستری اعلامی ۲۲ رابطه"
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
- p04
  ---
# P04 — رجیستری اعلامی ۲۲ رابطه

## 1. وضعیت و Gate

- Track: **CORE**
- وضعیت فعلی: `blocked_by_doctrine`
- Dependencies: `P00, P03`
- Downstream blocked: `P05, P06, P07`

## 2. هدف

۲۲ رابطه Word را بدون if/else پراکنده در یک registry نسخه‌دار، قابل‌ممیزی و قابل‌فعال/غیرفعال‌سازی تعریف کند.

## 3. ورودی‌های authoritative

- approved pair definitions
- period identities
- major/minor label policy

## 4. خروجی‌ها و قرارداد تحویل

- DAYE_SignalDefinition[22]
- canonical IDs
- source aliases
- current/reference resolver metadata

## 5. فایل‌ها و ماژول‌های مالک

- `DAYE_SignalRegistry.mqh`
- `daye_signal_pairs_v2.json`
- `DAYE_SignalIdentity.mqh`

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

- تعداد Core دقیقاً 22 است.
- alias راست‌به‌چپ هویت canonical نیست.
- هیچ Sequential SMT اختیاری وارد registry Core نمی‌شود.

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

- 22 unique IDs
- 6 major + 16 subcycle
- all periods resolvable
- NP and W rules explicit

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

- registry snapshot approved
- schema validator pass
- every signal source trace recorded

## 14. ریسک‌ها و hostile review

- alias inversion
- current/reference swap
- mixing optional SSMT
- stale state، future leakage، cross-symbol coordinate و duplicate identity بررسی شوند.

## 15. Non-goals

- order placement و risk sizing
- تغییر خودکار doctrine
- ادغام با EXP0017
- استفاده از Optional برای تغییر Core

## 16. Handoff

خروجی این فاز فقط زمانی به فاز بعدی می‌رود که evidence package شامل spec، tests، compile/runtime evidence، docs، Obsidian و rollback کامل باشد.
