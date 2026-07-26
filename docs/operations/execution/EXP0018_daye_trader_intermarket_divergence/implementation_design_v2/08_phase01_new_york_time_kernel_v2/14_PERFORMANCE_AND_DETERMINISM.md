---
id: EXP0018-P01-14-PERFORMANCE-AND-DETERMINISM
title: "EXP0018 P01 — Performance and Determinism"
type: specification
status: implemented-awaiting-metaeditor-compile
project: EXP0018
phase: P01
version: 2.2.0
created: 2026-07-10
updated: 2026-07-10
owner: Quant Engineering
tags:
  - exp0018
  - daye-trader
  - phase01
  - time-kernel
---


# بودجه عملکرد

- یک snapshot در هر timer callback؛
- registry فقط یک‌بار در init ساخته می‌شود؛
- هیچ CopyRates، full-history scan یا chart object وجود ندارد؛
- transition detection مقایسه ثابت است؛
- CSV اختیاری و پیش‌فرض خاموش است.

# Determinism

در حالت manual broker offset، یک broker timestamp و config یکسان باید snapshot یکسان بسازد. Auto current live به‌طور صریح replay-safe نیست.

