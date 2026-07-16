---
type: architecture
system: NDS
phase: 55
status: implemented
version: 1.2.0
---
# NDS Hook 86.4 Exact Acceleration

## هدف

بیشترین سرعت ممکن برای بک‌تست ستاپ Hook 86.4، بدون کاهش تعداد کندل‌ها، Scaleها، دقت نودشماری، موتور Closure یا مدل اجرای سفارش.

## مسیر سریع دقیق

```text
Broker exposure preflight
├── Pending / Fixed-R position → execution lifecycle only
└── No exposure
    → canonical Phase01/02 Hook
    → F engine only when F3 ownership can change eligibility
    → Phase03/04 only for pre-closure eligible candidates
    → one-pass funnel + latest selection
    → existing execution core
```

## چیزهایی که کم نشده‌اند

```text
PARITY bars = 5000
Scales = 2,3,5,8,13,21,34,55
Closed bars only = true
Phase04 closure = canonical 50%
Entry = canonical 86.4%
X count = canonical 3 or 4
Reward = fixed 1R
```

## تنظیم پیشنهادی

```text
InpBTProfile = PARITY
InpBTTradeProfile = HOOK_864_CYCLE_R1
InpBTExactAcceleration = true
```

برای مقایسه مرجع، فقط `InpBTExactAcceleration` را `false` کن و همه ورودی‌های دیگر را ثابت نگه دار.

## تله مهم

پوزیشن قدیمی `TERMINAL_F123` از fast path ثابت-R استفاده نمی‌کند، چون خروجش هنوز به F3 هم‌جهت بعد از ورود وابسته است. فقط پوزیشن پروفایل 86.4 که SL/TP آن روی Broker ثبت شده است می‌تواند کل rebuild ساختاری را رد کند.

## لینک‌ها

- [[NDS Hook 86.4 Cycle R1 Entry Contract]]
- [[NDS Hook 86.4 Cycle R1 State Machine]]
- [[NDS Hook 86.4 No Trade Diagnostic Funnel]]
- [[NDS Lightweight Backtest Runtime]]
- [[../../nds_entry_architecture/phase55_hook_864_cycle_r1_execution/20_exact_acceleration_and_maximum_speed_contract|Detailed Exact Acceleration Contract]]

## تست برابری

در هر دو Run مقدار `InpBTPrintEveryNRuns = 1` باشد. سپس:

```powershell
python .\tools\flag_counting\compare_nds_hook_864_acceleration_logs.py ".\exact.log" ".\reference.log"
```

ابزار باید `decision_parity: true` بدهد. مقایسه روی Action، Status، Setup Key و هندسه Entry/SL/TP انجام می‌شود.
