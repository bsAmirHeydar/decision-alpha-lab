  ---
  id: EXP0018-OPEN-DECISIONS-V2
  title: "EXP0018 Open Decision Register v2"
  type: register
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
# تصمیم‌های باز و Blockerها

## DY-A01 — BUY/SELL side mapping

- پرسش: آیا SELL دقیقاً high-side و BUY دقیقاً low-side است؟
- فازهای وابسته: `P04|P05|P13`
- شدت: `BLOCKER`
- وضعیت: **OPEN**
- خروجی لازم: ADR مصوب + مثال مثبت/منفی + fixture

## DY-A02 — TWO exact time

- پرسش: Monday 18:00 NY یا Tuesday 18:00 NY؟
- فازهای وابسته: `P10|P13`
- شدت: `BLOCKER`
- وضعیت: **OPEN**
- خروجی لازم: ADR مصوب + مثال مثبت/منفی + fixture

## DY-A03 — Weekly period boundary

- پرسش: شروع و پایان دقیق Weekly period چیست؟
- فازهای وابسته: `P03|P04|P13`
- شدت: `BLOCKER`
- وضعیت: **OPEN**
- خروجی لازم: ADR مصوب + مثال مثبت/منفی + fixture

## DY-A04 — First Sweep composite scope

- پرسش: کلید مصرف reference شامل relationship/side/hunter است یا گسترده‌تر؟
- فازهای وابسته: `P07|P13`
- شدت: `BLOCKER`
- وضعیت: **OPEN**
- خروجی لازم: ADR مصوب + مثال مثبت/منفی + fixture

## DY-A05 — NP relationship

- پرسش: current P در برابر previous N یا تفسیر دیگر؟
- فازهای وابسته: `P04|P13`
- شدت: `BLOCKER`
- وضعیت: **OPEN**
- خروجی لازم: ADR مصوب + مثال مثبت/منفی + fixture

## DY-A06 — Body/close divergence scope

- پرسش: در Core فقط wick-touch است یا body/close هم وارد شود؟
- فازهای وابسته: `P00|P16`
- شدت: `CORE_BOUNDARY`
- وضعیت: **OPEN**
- خروجی لازم: ADR مصوب + مثال مثبت/منفی + fixture

## DY-A07 — 22 relationships vs SSMT taxonomy

- پرسش: ۲۲ رابطه مستقل از taxonomy اختیاری باقی بمانند؟
- فازهای وابسته: `P04|P16`
- شدت: `CORE_BOUNDARY`
- وضعیت: **OPEN**
- خروجی لازم: ADR مصوب + مثال مثبت/منفی + fixture

## DY-A08 — Extended True Opens placement

- پرسش: در Expert اصلی یا module/Expert جدا؟
- فازهای وابسته: `P14`
- شدت: `OPTIONAL`
- وضعیت: **OPEN**
- خروجی لازم: ADR مصوب + مثال مثبت/منفی + fixture

## DY-A09 — DFR roadmap status

- پرسش: Research vault یا module رسمی اختیاری؟
- فازهای وابسته: `P15`
- شدت: `OPTIONAL`
- وضعیت: **OPEN**
- خروجی لازم: ADR مصوب + مثال مثبت/منفی + fixture

## DY-A10 — Triad confirmation authority

- پرسش: در v1 فقط observer باشد؟
- فازهای وابسته: `P19`
- شدت: `OPTIONAL`
- وضعیت: **OPEN**
- خروجی لازم: ADR مصوب + مثال مثبت/منفی + fixture

## DY-A11 — News context authority

- پرسش: فقط ledger یا filter؟
- فازهای وابسته: `P18|P20`
- شدت: `OPTIONAL`
- وضعیت: **OPEN**
- خروجی لازم: ADR مصوب + مثال مثبت/منفی + fixture

## DY-A12 — Historical line persistence

- پرسش: پس از retirement/invalidation آینده، خط confirmed همیشه باقی بماند؟
- فازهای وابسته: `P08|P13`
- شدت: `BLOCKER`
- وضعیت: **OPEN**
- خروجی لازم: ADR مصوب + مثال مثبت/منفی + fixture
