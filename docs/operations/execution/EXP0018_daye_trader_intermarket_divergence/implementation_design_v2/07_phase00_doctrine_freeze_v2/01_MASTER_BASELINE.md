---
id: EXP0018-P00-MASTER-BASELINE
title: "EXP0018 Phase 00 — Master Doctrine Baseline"
type: specification
status: draft
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

# خط مبنای دکترین هسته

## 1. هویت پروژه

EXP0018 یک پروژه مستقل برای نمایش و ممیزی روابط زمانی Daye میان دو نماد همبسته است. این پروژه از EXP0017 جداست و هیچ تعریف، state، object prefix یا lifecycle را از آن به‌صورت ضمنی به ارث نمی‌برد.

## 2. مسئله‌ای که هسته حل می‌کند

برای هر رابطه زمانی از رجیستری ۲۲گانه:

1. یک **Current Period** و یک **Reference Period** مشخص وجود دارد.
2. High و Low هر Period برای هر نماد به‌صورت مستقل محاسبه می‌شود.
3. Hunt فقط با مقایسه قیمت هر نماد با مرجع همان نماد سنجیده می‌شود.
4. اگر در یک سمت فقط یکی از دو نماد Hunt کرده باشد، divergence candidate شکل می‌گیرد.
5. candidate فقط در Close آخرین کندل بسته‌شده تایم‌فریم میزبان تأیید یا باطل می‌شود.
6. خط تأییدشده روی چارت Hunter و با قیمت‌های همان نماد رسم می‌شود.
7. lifecycle مرجع تعیین می‌کند آیا همان reference-side هنوز اجازه تولید رویداد جدید دارد یا خیر.

## 3. اصل‌های مادر

### D-01 — زمان دامنه اصلی است
تمام Periodها با ساعت نیویورک تعریف می‌شوند. Broker time فقط ورودی تبدیل است و حق تعریف session را ندارد.

### D-02 — هر نماد با مرجع خودش مقایسه می‌شود
سطح SPX با قیمت SPX و سطح NDX با قیمت NDX سنجیده می‌شود. مقایسه عدد خام قیمت دو نماد ممنوع است.

### D-03 — Hunt یک واقعیت است، نه سیگنال نهایی
Touch یا عبور از سطح یک observation است. تأیید divergence رویدادی جدا در Close کندل میزبان است.

### D-04 — نبود داده، نبود Hunt نیست
اگر داده یک نماد ناقص یا unsynchronized باشد، نتیجه `UNAVAILABLE/INCOMPLETE` است؛ نه `NOT_HUNTED`.

### D-05 — State مالک واحد دارد
Reference lifecycle، signal state، period store و renderer هرکدام owner مستقل دارند. Renderer حق ساخت truth ندارد.

### D-06 — خط تاریخی رکورد است
پس از تأیید، خط نماینده یک رویداد تاریخی است و تغییرات بعدی بازار نباید تاریخ تأیید را بازنویسی کند؛ تصمیم نهایی این اصل در ADR-DY-A12 ثبت می‌شود.

### D-07 — Core کوچک و deterministic می‌ماند
True Openهای گسترش‌یافته، DFR، خبر، triad، AMDX/XAMD و انواع SSMT تا زمان promotion در Track اختیاری باقی می‌مانند.

### D-08 — هیچ حدسی وارد کد نمی‌شود
تعارض sourceها با ADR حل می‌شود. تا زمانی که ADR blocker بسته نشده، feature وابسته disabled می‌ماند.

## 4. حدود نسخه Core v1

Core v1 شامل:

- New York time kernel؛
- A/L/N/P و a1…p4؛
- Daily و Weekly پس از تصویب boundary؛
- رجیستری ۲۲ رابطه؛
- touch-only hunt؛
- close confirmation؛
- first-sweep/reference lifecycle؛
- hunter-chart trend line؛
- session boxes؛
- TWO/TDO پس از تصویب anchor؛
- historical replay با همان engine لایو؛
- audit ledger و supervisor QA.

Core v1 شامل این موارد نیست:

- Order placement؛
- ریسک و تارگت؛
- فیلتر خبر؛
- DFR/Projection؛
- Triad confirmation؛
- AMDX/XAMD classifier؛
- body/close SSMT؛
- مدل آماری یا AI authority.

## 5. شرط بسته‌شدن Phase 00

Phase 00 فقط وقتی `ACTIVE/FROZEN` می‌شود که:

- ADRهای critical تصویب شوند؛
- هر rule مثال مثبت و counterexample داشته باشد؛
- rule registry و fixture registry معتبر باشند؛
- source→decision→phase traceability کامل باشد؛
- Strategy Architect approval ثبت شود.
