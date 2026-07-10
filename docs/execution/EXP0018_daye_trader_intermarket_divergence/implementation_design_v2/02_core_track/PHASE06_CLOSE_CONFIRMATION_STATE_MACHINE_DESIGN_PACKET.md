  ---
  id: EXP0018-P06-DESIGN-PACKET-V2
  title: "EXP0018 P06 — ماشین حالت تأیید در کلوز"
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
- p06
  ---
# P06 — ماشین حالت تأیید در کلوز

## 1. وضعیت و Gate

- Track: **CORE**
- وضعیت فعلی: `not_started`
- Dependencies: `P05`
- Downstream blocked: `P07, P08, P11, P12`

## 2. هدف

candidateهای intrabar را فقط در اولین close تایم‌فریم میزبان به confirmed یا invalidated تبدیل کند.

## 3. ورودی‌های authoritative

- hunt observations during host candle
- host closed-bar event
- signal definition

## 4. خروجی‌ها و قرارداد تحویل

- CANDIDATE
- CONFIRMED
- INVALIDATED_DOUBLE_HUNT
- NO_SIGNAL
- confirmation event

## 5. فایل‌ها و ماژول‌های مالک

- `DAYE_ConfirmationTypes.mqh`
- `DAYE_ConfirmationStateMachine.mqh`
- `DAYE_ClosedBarClock.mqh`
- `EXP0018_Daye_Confirmation_Anatomy.mq5`

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

- فقط closed bar state را نهایی می‌کند.
- یک confirmation برای composite identity صادر می‌شود.
- double hunt قبل از close سیگنال را رد می‌کند.

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

- hunter first protected later same candle
- one-sided through close
- multiple signal types same candle
- BUY and SELL simultaneous
- restart before close

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

- transition table complete
- duplicate confirmation impossible
- live/replay state transitions equal

## 14. ریسک‌ها و hostile review

- callback duplication
- host timeframe mismatch
- state loss on reattach
- stale state، future leakage، cross-symbol coordinate و duplicate identity بررسی شوند.

## 15. Non-goals

- order placement و risk sizing
- تغییر خودکار doctrine
- ادغام با EXP0017
- استفاده از Optional برای تغییر Core

## 16. Handoff

خروجی این فاز فقط زمانی به فاز بعدی می‌رود که evidence package شامل spec، tests، compile/runtime evidence، docs، Obsidian و rollback کامل باشد.
