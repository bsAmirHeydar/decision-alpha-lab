---
id: EXP0018-P00-GLOSSARY
title: "EXP0018 Phase 00 — Canonical Glossary"
type: standard
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
# واژه‌نامه رسمی

## Architect

مرجع انسانی تصویب rule و ADR.

## Broker Time

زمان خام سرور بروکر؛ فقط ورودی تبدیل.

## New York Time

clock رسمی تمام Periodهای Core.

## Trading Day

روز Daye از 18:00 نیویورک تا 16:59:59 روز بعد.

## Session Gap

بازه 17:00 تا 17:59:59 که عضو A/L/N/P نیست.

## Period

پنجره زمانی نسخه‌دار با identity، start/end و OHLC.

## Reference Period

Period قبلی یا رابطه‌ای که سطح مرجع از آن می‌آید.

## Current Period

Period فعلی که رفتار آن در برابر Reference بررسی می‌شود.

## Reference Side

HIGH یا LOW یک Reference Period برای یک نماد.

## Hunt

touch یا عبور قیمت همان نماد از reference-side همان نماد.

## Hunter

نمادی که reference-side خودش را Hunt کرده است.

## Protected

نمادی که در همان سمت هنوز reference-side خودش را Hunt نکرده است.

## Candidate

one-sided hunt مشاهده‌شده پیش از Close نهایی.

## Confirmed

candidate که در Close کندل میزبان هنوز one-sided است.

## Double Hunt

هر دو نماد در همان سمت تا Close مرجع خود را Hunt کرده‌اند.

## Invalidated

candidate که در Close شرایط one-sided را ندارد.

## Host Timeframe

تایم‌فریمی که Expert روی آن اجرا شده و Close آن مرز تأیید است.

## First Sweep

سیاست مصرف نخستین فرصت معتبر برای reference-side؛ scope نهایی در ADR-DY-A04.

## Retired Reference

مرجعی که lifecycle اجازه سیگنال جدید از آن نمی‌دهد.

## Historical Line

خط immutable مربوط به رویداد Confirmed.

## Major Relationship

یکی از WW/DD/PA/AL/LN/NP که label متنی دارد.

## Minor Relationship

یکی از 16 رابطه 90m که فقط خط دارد.

## Core

موتور deterministic 22 رابطه و اجزای لازم برای آن.

## Optional

ماژول پژوهشی که authority تغییر Core ندارد.

## No Data

داده کافی وجود ندارد؛ با Not Hunted متفاوت است.

## Replay

اجرای chronological همان engine لایو روی تاریخ.

## Visual Event

خروجی typed برای renderer؛ خود object منبع truth نیست.

## Ledger Event

رکورد audit نسخه‌دار و idempotent.
