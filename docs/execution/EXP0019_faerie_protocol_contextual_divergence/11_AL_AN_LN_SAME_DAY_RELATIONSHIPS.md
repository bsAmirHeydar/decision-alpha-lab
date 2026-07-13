---
title: "11 — روابط Same-Day: AL / AN / LN"
tags: [exp0019, faerie-protocol, divergence-context]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
doc_version: 1.0.0
last_updated: 2026-07-13
---
# 11 — روابط Same-Day: AL / AN / LN

## AL

A(d) باید کامل باشد. L(d) check window است. high/low مرجع برای هر نماد از A ساخته می‌شود و first touchها در L بررسی می‌شوند.

## AN

A(d) reference و N(d) check است. huntهای رخ‌داده در L به‌خودی‌خود AN نیستند، اما روی freshness سطح اثر دارند؛ policy مصرف باید event timeline را ببیند.

## LN

L(d) reference و N(d) check است.

## نکته حیاتی chronology

برای AN، اگر protected level A در L touch شده باشد، A دیگر برای N protected نیست. پس AN eligibility فقط با snapshot ساده A/N قابل تعیین نیست؛ lifecycle بین `A.end` و `N.start` باید audit شود.

## candidate key

```text
trading_day + relation + reference_session_id + check_session_id + side + hunter + protected
```

## simultaneous relations

N می‌تواند هم AN و هم LN و هم NN/NA/NL بسازد. core هیچ relation را به‌دلیل relation دیگر حذف نمی‌کند؛ WW/quota بعداً disposition می‌دهند.

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
