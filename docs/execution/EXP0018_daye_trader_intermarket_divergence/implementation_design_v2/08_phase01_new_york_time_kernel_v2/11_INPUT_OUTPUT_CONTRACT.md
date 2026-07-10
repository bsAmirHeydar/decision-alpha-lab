---
id: EXP0018-P01-11-INPUT-OUTPUT-CONTRACT
title: "EXP0018 P01 — Input and Output Contract"
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


# Inputهای مهم

- broker offset mode؛
- broker UTC offset؛
- NY offset mode؛
- manual NY offset؛
- ambiguity policies؛
- timer seconds؛
- self-test؛
- audit CSV.

# Snapshot خروجی

- broker/UTC/NY timestamp؛
- resolved offsets؛
- DST/fold؛
- trading-day key؛
- session/subcycle/gap؛
- local و UTC windowها؛
- replay safety؛
- typed status/reason.

P02 و P03 باید فقط این contract را مصرف کنند، نه internals تبدیل زمان.

