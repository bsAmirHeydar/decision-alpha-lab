---
id: EXP0018-P00-AUTHORITY
title: "EXP0018 Phase 00 — Source Authority and Interpretation"
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

# سلسله‌مراتب منبع و روش تفسیر

## ترتیب اختیار

1. تصمیم صریح معمار استراتژی در ADR مصوب؛
2. Word اصلی Daye؛
3. مستندات تکمیلی Trader Daye PDF؛
4. Bucko Quarterly Theory؛
5. QT Education؛
6. قراردادهای مهندسی؛
7. رفتار کد قدیمی؛
8. پیشنهاد AI.

## قواعد تفسیر

- مثال صریح Word می‌تواند متن مبهم همان Word را به تعارض تبدیل کند، اما AI حق انتخاب نهایی ندارد.
- PDFها می‌توانند تعریف را روشن، corroborate یا hypothesis تولید کنند؛ نمی‌توانند Core را بی‌صدا تغییر دهند.
- رفتار یک کد قدیمی evidence پیاده‌سازی است، نه authority دامنه.
- هر ادعای عددی مانند «۷۵٪» تا زمان outcome study در وضعیت `QUARANTINED` باقی می‌ماند.
- هر تعریف Swiss Time برای EXP0018 Core قرنطینه است؛ clock رسمی نیویورک باقی می‌ماند.

## وضعیت‌های claim

| وضعیت | معنی |
|---|---|
| `CANONICAL` | قانون مستقیم و بدون تعارض از منبع اصلی یا ADR |
| `CORROBORATING` | تأییدکننده قانون موجود |
| `CLARIFYING_CANDIDATE` | پیشنهاد روشن‌سازی، نیازمند تصویب |
| `RESEARCH_CANDIDATE` | فقط برای Track اختیاری |
| `CONFLICT` | نیازمند ADR |
| `QUARANTINED` | اجازه ورود به کد ندارد |
| `EXAMPLE_ONLY` | نمونه آموزشی، نه قانون |

## قانون traceability

هیچ rule وارد registry نمی‌شود مگر اینکه حداقل یکی از این‌ها را داشته باشد:

```text
source artifact + location
یا
approved ADR
```
