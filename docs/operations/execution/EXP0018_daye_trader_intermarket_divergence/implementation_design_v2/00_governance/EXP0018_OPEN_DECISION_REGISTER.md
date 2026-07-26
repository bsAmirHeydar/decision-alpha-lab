---
id: EXP0018-OPEN-DECISIONS-V2
title: "EXP0018 Open Decision Register v2"
type: register
status: active
project: EXP0018
version: 2.1.0
created: 2026-07-10
updated: 2026-07-10
owner: Strategy Architect
tags:
  - exp0018
  - daye-trader
  - phase00
  - doctrine-freeze
---
# تصمیم‌های باز

## DY-A01 — BUY/SELL Mapping

- سؤال: آیا High-side به SELL و Low-side به BUY نگاشت شود؟
- شدت: `BLOCKER`
- فازها: `P04|P05|P13`
- وضعیت: `PROPOSED / AWAITING APPROVAL`
- پیشنهاد: `High-side=SELL; Low-side=BUY`
- ADR: [[../07_phase00_doctrine_freeze_v2/adr/ADR-DY-A01-BUY-SELL-MAPPING]]

## DY-A02 — TWO Anchor

- سؤال: TWO دقیقاً از کدام زمان شروع می‌شود؟
- شدت: `BLOCKER`
- فازها: `P10|P13`
- وضعیت: `PROPOSED / AWAITING APPROVAL`
- پیشنهاد: `Tuesday trading-day open = Monday 18:00 NY`
- ADR: [[../07_phase00_doctrine_freeze_v2/adr/ADR-DY-A02-TWO-ANCHOR]]

## DY-A03 — Weekly Boundary

- سؤال: مرز W چیست؟
- شدت: `BLOCKER`
- فازها: `P03|P04|P13`
- وضعیت: `PROPOSED / AWAITING APPROVAL`
- پیشنهاد: `Sunday 18:00 NY to Friday 16:59:59 NY`
- ADR: [[../07_phase00_doctrine_freeze_v2/adr/ADR-DY-A03-WEEKLY-BOUNDARY]]

## DY-A04 — First Sweep Scope

- سؤال: مصرف نخستین sweep با چه کلیدی اعمال شود؟
- شدت: `BLOCKER`
- فازها: `P07|P13`
- وضعیت: `PROPOSED / AWAITING APPROVAL`
- پیشنهاد: `relationship+reference period+side+hunter/protected`
- ADR: [[../07_phase00_doctrine_freeze_v2/adr/ADR-DY-A04-FIRST-SWEEP-SCOPE]]

## DY-A05 — NP Relationship

- سؤال: NP کدام Periodها را مقایسه می‌کند؟
- شدت: `BLOCKER`
- فازها: `P04|P13`
- وضعیت: `PROPOSED / AWAITING APPROVAL`
- پیشنهاد: `Current P vs immediately preceding N in same trading day`
- ADR: [[../07_phase00_doctrine_freeze_v2/adr/ADR-DY-A05-NP-RELATIONSHIP]]

## DY-A06 — Wick vs Body Scope

- سؤال: Core فقط wick-touch باشد؟
- شدت: `CORE_BOUNDARY`
- فازها: `P00|P16`
- وضعیت: `PROPOSED / AWAITING APPROVAL`
- پیشنهاد: `Core=wick touch only; body/close=P16 typed event`
- ADR: [[../07_phase00_doctrine_freeze_v2/adr/ADR-DY-A06-WICK-VS-BODY]]

## DY-A07 — Core 22 vs SSMT

- سؤال: ۲۲ رابطه با SSMT taxonomy ادغام شوند؟
- شدت: `CORE_BOUNDARY`
- فازها: `P04|P16`
- وضعیت: `PROPOSED / AWAITING APPROVAL`
- پیشنهاد: `Keep 22 Core relationships independent`
- ADR: [[../07_phase00_doctrine_freeze_v2/adr/ADR-DY-A07-CORE-VS-SSMT]]

## DY-A08 — Extended True Opens Placement

- سؤال: True Openهای گسترش‌یافته کجا باشند؟
- شدت: `OPTIONAL`
- فازها: `P14`
- وضعیت: `PROPOSED / AWAITING APPROVAL`
- پیشنهاد: `Separate optional module/expert`
- ADR: [[../07_phase00_doctrine_freeze_v2/adr/ADR-DY-A08-EXTENDED-TRUE-OPENS]]

## DY-A09 — DFR Placement

- سؤال: DFR چه جایگاهی دارد؟
- شدت: `OPTIONAL`
- فازها: `P15`
- وضعیت: `PROPOSED / AWAITING APPROVAL`
- پیشنهاد: `Research-only optional module first`
- ADR: [[../07_phase00_doctrine_freeze_v2/adr/ADR-DY-A09-DFR-PLACEMENT]]

## DY-A10 — Triad Authority

- سؤال: Triad در v1 چه اختیاری دارد؟
- شدت: `OPTIONAL`
- فازها: `P19`
- وضعیت: `PROPOSED / AWAITING APPROVAL`
- پیشنهاد: `Observer only`
- ADR: [[../07_phase00_doctrine_freeze_v2/adr/ADR-DY-A10-TRIAD-AUTHORITY]]

## DY-A11 — News Authority

- سؤال: خبر context است یا filter؟
- شدت: `OPTIONAL`
- فازها: `P18|P20`
- وضعیت: `PROPOSED / AWAITING APPROVAL`
- پیشنهاد: `Ledger-only context in v1`
- ADR: [[../07_phase00_doctrine_freeze_v2/adr/ADR-DY-A11-NEWS-AUTHORITY]]

## DY-A12 — Historical Line Persistence

- سؤال: خط confirmed بعداً حذف شود؟
- شدت: `BLOCKER`
- فازها: `P08|P13`
- وضعیت: `PROPOSED / AWAITING APPROVAL`
- پیشنهاد: `Keep confirmed line for configured lookback`
- ADR: [[../07_phase00_doctrine_freeze_v2/adr/ADR-DY-A12-HISTORICAL-LINE-PERSISTENCE]]
