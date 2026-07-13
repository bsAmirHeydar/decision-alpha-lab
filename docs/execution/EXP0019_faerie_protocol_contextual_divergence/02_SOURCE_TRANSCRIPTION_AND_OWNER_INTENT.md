---
title: "02 — استخراج Owner Intent و سلسله‌مراتب حقیقت"
tags: [exp0019, faerie-protocol, divergence-context]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
doc_version: 1.0.0
last_updated: 2026-07-13
---
# 02 — استخراج Owner Intent و سلسله‌مراتب حقیقت

## هدف

این سند توضیح می‌دهد چگونه متن محاوره‌ای، کد Legacy و معماری هدف به قرارداد تبدیل می‌شوند بدون اینکه یک رفتار تصادفی Legacy به قانون استراتژی تبدیل شود.

## سلسله‌مراتب

1. اظهارات صریح مالک در Word و پیام فعلی.
2. تصمیم‌های قبلی تأییدشده پروژه درباره هسته عمومی واگرایی.
3. رفتار Legacy که با 1 و 2 تعارض ندارد.
4. پیشنهاد معماری برای موارد ساکت.
5. تصمیم باز برای موارد چندمعنا.

## اظهارات قطعی استخراج‌شده

- زمان استراتژی New York است و DST باید auto/manual باشد.
- A=`18:00–03:59:59`، L=`04:00–09:29:59`، N=`09:30–16:59:59`.
- هانت touch-only است؛ close برای هانت لازم نیست.
- واگرایی در close کندل timeframe اجراشده تأیید می‌شود.
- اگر تا close هر دو نماد سطح متناظر را بزنند، آن رابطه در آن کندل واگرایی نیست.
- entry روی protected/clean symbol است.
- stop روی reference همان protected symbol است.
- RR input با default 1 و risk percent equity با default 2 است.
- در یک کندل چند relation و دو جهت می‌توانند ثبت شوند.
- confirmed drawing پاک نمی‌شود.
- WW جهت lower relations را gate می‌کند.

## مواردی که از Legacy وارد canonical نمی‌شوند

- وابستگی range/reference به timeframe جاری.
- نام آبجکت بر اساس D0/K1 بدون تاریخ مطلق.
- مصرف سطح hunter پیش از check window.
- DST با transition ساعت 02:00 UTC.
- rescan کامل 100 هفته هر پنج ثانیه.
- حذف WW و execution.

## قاعده حل تعارض

هرجا Word و Legacy متفاوت‌اند، Legacy به‌عنوان fixture مطالعه می‌شود، نه authority. تعارض در Decision Register ثبت و implementation تا تصمیم نهایی fail-closed می‌ماند.

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
