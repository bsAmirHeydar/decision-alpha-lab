  ---
  id: EXP0018-P13-DESIGN-PACKET-V2
  title: "EXP0018 P13 — کنترل کیفیت، اعتبارسنجی ناظر و نسخه آزمایشی Core"
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
- p13
  ---
# P13 — کنترل کیفیت، اعتبارسنجی ناظر و نسخه آزمایشی Core

## 1. وضعیت و Gate

- Track: **CORE**
- وضعیت فعلی: `not_started`
- Dependencies: `P12`
- Downstream blocked: `P14, P15, P16, P17, P18, P19, P20`

## 2. هدف

Core را با compile، contract، replay، visual، supervisor، performance و rollback به RC قابل‌ممیزی تبدیل کند.

## 3. ورودی‌های authoritative

- all core artifacts
- golden scenarios
- supervisor checklist
- release manifest

## 4. خروجی‌ها و قرارداد تحویل

- RC build
- validation evidence
- known limitations
- rollback package
- core baseline hash

## 5. فایل‌ها و ماژول‌های مالک

- `EXP0018_Daye_Core_RC.mq5`
- `release evidence docs`
- `golden fixtures`
- `supervisor guide`

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

- RC هیچ order API ندارد.
- warningها پنهان نمی‌شوند.
- enrichment قبل از Core RC وارد نمی‌شود.

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

- 0 errors/warnings
- all contract tests
- 10+ golden visual cases
- live/replay parity
- performance budget
- rollback drill

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

- architect sign-off
- supervisor pass
- all blockers closed or explicitly disabled
- versioned RC produced

## 14. ریسک‌ها و hostile review

- visual-only false confidence
- uncovered broker differences
- stale state، future leakage، cross-symbol coordinate و duplicate identity بررسی شوند.

## 15. Non-goals

- order placement و risk sizing
- تغییر خودکار doctrine
- ادغام با EXP0017
- استفاده از Optional برای تغییر Core

## 16. Handoff

خروجی این فاز فقط زمانی به فاز بعدی می‌رود که evidence package شامل spec، tests، compile/runtime evidence، docs، Obsidian و rollback کامل باشد.
