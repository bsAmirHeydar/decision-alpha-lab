  ---
  id: EXP0018-MASTER-BLUEPRINT-V2
  title: "EXP0018 Master Implementation Blueprint v2"
  type: architecture
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
# نقشه مادر پیاده‌سازی EXP0018
## مسیر کلان
```mermaid
flowchart TD
  S[Approved Sources + Architect Decisions] --> P00[P00 Doctrine Freeze]
  P00 --> P01[P01 Time Kernel]
  P01 --> P02[P02 Data Sync]
  P02 --> P03[P03 Period Aggregation]
  P03 --> P04[P04 22-Signal Registry]
  P04 --> P05[P05 Hunt Facts]
  P05 --> P06[P06 Close Confirmation]
  P06 --> P07[P07 Reference Lifecycle]
  P07 --> P08[P08 Hunter Drawing]
  P03 --> P09[P09 Session Boxes]
  P01 --> P10[P10 TWO/TDO]
  P08 --> P11[P11 Replay]
  P09 --> P11
  P10 --> P11
  P11 --> P12[P12 Ledger/Diagnostics]
  P12 --> P13[P13 Core RC]
  P13 --> P14[P14 Extended Opens]
  P13 --> P15[P15 DFR]
  P13 --> P16[P16 Typed SSMT]
  P13 --> P17[P17 Context Ledger]
  P13 --> P18[P18 News Adapter]
  P13 --> P19[P19 Triad Observer]
  P17 --> P20[P20 Outcome/Promotion]
  P18 --> P20
  P19 --> P20
```
## وضعیت فازها
| فاز | نام | Track | وضعیت | Dependencies |
|---|---|---|---|---|
| P00 | انجماد دکترین نسخه ۲ و خط مبنای تصمیم‌ها | core | `blocked_decisions_open` | — |
| P01 | هسته زمان نیویورک و تقویم | core | `foundation_exists_requires_validation` | P00 |
| P02 | همگام‌سازی داده چندنمادی | core | `not_started` | P01 |
| P03 | تجمیع دوره‌ها و کامل‌بودن آن‌ها | core | `not_started` | P02 |
| P04 | رجیستری اعلامی ۲۲ رابطه | core | `blocked_by_doctrine` | P00, P03 |
| P05 | تشخیص هانت و Snapshot مرجع | core | `blocked_by_doctrine` | P04 |
| P06 | ماشین حالت تأیید در کلوز | core | `not_started` | P05 |
| P07 | چرخه عمر مرجع و سیاست First Sweep | core | `blocked_by_doctrine` | P06 |
| P08 | رویداد تصویری تغییرناپذیر و رسم واگرایی | core | `not_started` | P07 |
| P09 | رندر باکس‌های سشن | core | `not_started` | P03 |
| P10 | رندر Anchorهای TWO و TDO | core | `blocked_by_doctrine` | P00, P01 |
| P11 | موتور بازپخش تاریخی و Backfill | core | `not_started` | P08, P09, P10 |
| P12 | دفتر ممیزی و Diagnostics | core | `not_started` | P06, P07, P11 |
| P13 | کنترل کیفیت، اعتبارسنجی ناظر و نسخه آزمایشی Core | core | `not_started` | P12 |
| P14 | رجیستری توسعه‌یافته True Open | optional | `optional_not_admitted` | P13 |
| P15 | موتور پژوهشی DFR و Projection | optional | `optional_not_admitted` | P13 |
| P16 | موتور پژوهشی انواع SSMT | optional | `optional_not_admitted` | P13 |
| P17 | دفتر Featureهای زمینه‌ای | optional | `optional_not_admitted` | P13 |
| P18 | Adapter خبر و زمان رویداد | optional | `optional_not_admitted` | P13 |
| P19 | ناظر Triad و Intermarket | optional | `optional_not_admitted` | P13 |
| P20 | مطالعه نتیجه و دروازه ارتقای قانون | optional | `optional_not_admitted` | P17, P18, P19 |


## معیار عبور از هر فاز

هر فاز فقط با این شواهد بسته می‌شود:

- specification و API contract تأییدشده
- state/event/invariant کامل
- test fixtures مثبت، منفی و boundary
- compile/static evidence
- replay/visual/schema evidence متناسب با فاز
- documentation + Obsidian + rollback
- هیچ warning یا risk پنهان
