---
title: "12 — روابط Cross-Day: NA / NL / NN"
tags: [exp0019, faerie-protocol, divergence-context]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
doc_version: 1.0.0
last_updated: 2026-07-13
---
# 12 — روابط Cross-Day: NA / NL / NN

## selector

برای trading day جاری `d`، referenceها از N روزهای قبل انتخاب می‌شوند:

```text
N(d-1), N(d-2), ...
```

و check به‌ترتیب A(d)، L(d)، N(d) است.

## دو معنی ممکن برای lookback

1. `CALENDAR_DAY_DEPTH`: k=1..N و missing weekend فقط skip می‌شود. رفتار نزدیک FP101.
2. `AVAILABLE_N_SESSION_COUNT`: تا N سشن N معتبر به عقب می‌رود و weekend/expiry gaps count نمی‌شوند.

Owner گفته weekend و data absence نباید خطا بدهد، اما count semantic را قطعی نکرده است. baseline پیشنهادی برای research: هر دو mode با default `AVAILABLE_N_SESSION_COUNT` و ثبت mode در event identity.

## history cap

اگر فقط m<N reference معتبر موجود است، همان m بررسی می‌شود؛ هیچ synthetic reference ساخته نمی‌شود.

## reuse across stages

یک N reference می‌تواند در A و سپس L/N event ایجاد کند تا وقتی protected side آن level را touch نکرده است. first-sweep dedup در هر check window جداست؛ protected touch reference را برای stageهای آینده exhaust می‌کند.

## complexity

حداکثر candidate pairs:

```text
3 cross-day relations × lookback depth × 2 sides × 2 hunter assignments
```

پس cache و incremental lifecycle ضروری است.

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
