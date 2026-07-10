  ---
  id: EXP0018-DESIGN-V2-INDEX
  title: "EXP0018 Implementation Design v2 — Index"
  type: moc
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

# EXP0018 Implementation Design v2

این شاخه نقشه مهندسی کامل برای تبدیل دکترین Daye/Quarterly Theory به سیستم **deterministic، replayable، visual-only و بدون اختیار معامله** است.

## نقطه شروع

1. [[EXP0018_DESIGN_OPERATING_CONTRACT|قرارداد کار طراحی]]
2. [[EXP0018_MASTER_IMPLEMENTATION_BLUEPRINT|نقشه مادر پیاده‌سازی]]
3. [[EXP0018_OPEN_DECISION_REGISTER|تصمیم‌های باز و blockerها]]
4. [[EXP0018_FIRST_DESIGN_SPRINT|اولین Sprint طراحی]]
5. [[CG_EXP0018_IMPLEMENTATION_DESIGN_V2_MOC|MOC اصلی Obsidian]]

## Tracks

- **Core P00–P13:** همان ۲۲ رابطه Word، touch-only hunt، close confirmation، lifecycle، drawing، boxes، TWO/TDO، replay و QA.
- **Optional P14–P20:** True Opens توسعه‌یافته، DFR، SSMTها، context، news، triad و outcome research؛ فقط پس از Core RC.

## وضعیت فعلی

- P01 Time Foundation کد پایه دارد، اما هنوز باید در این معماری review و validate شود.
- P00 هنوز به‌علت تصمیم‌های doctrine باز، کامل نیست.
- P02 تا P20 در وضعیت طراحی/عدم شروع هستند.
- هیچ فاز در این شاخه order placement، risk sizing یا execution authority ندارد.
## Phase 00 Detailed Package

- [[07_phase00_doctrine_freeze_v2/00_INDEX|P00 Doctrine Freeze v2 — بسته تفصیلی]]
- [[07_phase00_doctrine_freeze_v2/15_ARCHITECT_DECISION_WORKBOOK|برگه تصمیم معمار]]
- [[07_phase00_doctrine_freeze_v2/20_DOCTRINE_FREEZE_GATE|Gate انجماد دکترین]]
