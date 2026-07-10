---
id: EXP0018-P02-SCOPE
title: "P02 Scope and Authority"
type: specification
status: active
project: EXP0018
---
# دامنه و اختیار

## هدف

دریافت دو symbol واقعی بروکر، خواندن barهای پایه، تبدیل timestamp آن‌ها به UTC و نیویورک، سنجش کیفیت history و ساخت جفت‌های exact-time.

## اختیار این فاز

- انتخاب symbolهای ورودی در Market Watch
- بررسی metadata و history readiness
- `CopyRates` و `CopyTime`
- اعتبارسنجی OHLC و timestamp
- تولید health، summary، pair و event

## خارج از اختیار

- تعریف Hunt یا SMT
- تفسیر نبود bar به‌عنوان «هانت نکرده»
- ساخت period high/low
- رسم روی چارت
- forward-fill یا synthetic price
- سفارش، ریسک و execution

قاعده مادر: **P02 فقط حقیقت داده را تحویل می‌دهد؛ بازار را تفسیر نمی‌کند.**
