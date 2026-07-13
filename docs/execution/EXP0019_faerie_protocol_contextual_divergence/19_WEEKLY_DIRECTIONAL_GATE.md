---
title: "19 — Weekly Directional Gate"
tags: [exp0019, faerie-protocol, divergence-context]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
doc_version: 1.0.0
last_updated: 2026-07-13
---
# 19 — Weekly Directional Gate

## رفتار مورد درخواست

- WW bearish → فقط lower relationهای bearish eligible.
- WW bullish → فقط lower relationهای bullish eligible.
- direction مخالف نادیده گرفته/سرکوب می‌شود.

## جایگاه معماری

Gate بعد از confirmation قرار می‌گیرد:

```text
confirmed raw FP signal -> weekly gate -> eligible/suppressed disposition
```

این ترتیب باعث می‌شود data research همه signalها را ببیند ولی execution policy Owner حفظ شود.

## states

| WW state | lower BUY | lower SELL |
|---|---|---|
| NONE | allow* | allow* |
| BULLISH_ONLY | allow | suppress |
| BEARISH_ONLY | suppress | allow |
| CONFLICT/BOTH | open decision | open decision |
| MISSING_DATA | fail-closed for trade; record raw | fail-closed for trade; record raw |

`*` رفتار NONE هنوز owner-confirmed نیست؛ توصیه allow both.

## drawing policy

دو view قابل پشتیبانی است:

- `RAW_AUDIT`: همه confirmedها با status WW.
- `TRADING_VIEW`: فقط alignedها.

Default production drawing باید تصمیم مالک را دنبال کند؛ ledger همیشه کامل است.

## سطح اختیار این سند

این سند چهار سطح حقیقت را از هم جدا می‌کند:

| سطح | معنی |
|---|---|
| `OWNER_CONFIRMED` | در فایل Word یا درخواست صریح مالک آمده است. |
| `LEGACY_IMPLEMENTED` | در `FP 101.mq5` وجود دارد، حتی اگر قرارداد نهایی نباشد. |
| `ARCHITECTURAL_DERIVATION` | برای ماژولارکردن و حفظ هسته‌های مشترک از منبع استنتاج شده است. |
| `OPEN_DECISION` | قبل از کدنویسی نهایی نیازمند تصمیم مالک است. |

قاعده: رفتار Legacy فقط وقتی canonical است که با Owner Intent و قرارداد این پکیج تعارض نداشته باشد.

## ناوبری

- [[00_EXP0019_MOC|MOC اصلی EXP0019]]
- [[33_AMBIGUITY_AND_DECISION_REGISTER|ثبت ابهام‌ها و تصمیم‌ها]]
- [[34_IMPLEMENTATION_ROADMAP|نقشه پیاده‌سازی]]
- [[35_HANDOFF_TO_CODE|تحویل به کدنویسی]]
