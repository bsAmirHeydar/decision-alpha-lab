---
id: EXP0018-P00-SCOPE
title: "EXP0018 Phase 00 — Core Scope and Non-Goals"
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

# دامنه Core و مرزهای ممنوع

## Core باید چه چیزی را ثابت کند؟

Core فقط باید بتواند با داده قابل‌دسترس همان لحظه بگوید:

- Period جاری و مرجع کدام‌اند؛
- high/low هر Period برای هر نماد چیست؛
- کدام نماد سطح خودش را Hunt کرده؛
- کدام نماد Protected باقی مانده؛
- در Close کندل میزبان وضعیت نهایی چیست؛
- آیا reference-side طبق lifecycle هنوز قابل استفاده است؛
- چه Visual Event و Ledger Event باید صادر شود.

## Core نباید چه چیزی را بگوید؟

- معامله بخر یا بفروش؛
- احتمال برد چند درصد است؛
- کدام setup بهتر است؛
- خبر اجازه ورود می‌دهد یا نه؛
- DFR یا True Open اضافی سیگنال را فیلتر می‌کند؛
- triad باید pair را رد کند؛
- ریسک یا حجم چقدر باشد.

## جداسازی ماژولی

```text
Time → Data Sync → Period Store → Relationship Registry
     → Hunt Facts → Confirmation State → Reference Lifecycle
     → Visual Events / Ledger Events
```

Session boxes و TWO/TDO فقط consumer زمان و period هستند و حق تغییر Hunt یا Signal state ندارند.
