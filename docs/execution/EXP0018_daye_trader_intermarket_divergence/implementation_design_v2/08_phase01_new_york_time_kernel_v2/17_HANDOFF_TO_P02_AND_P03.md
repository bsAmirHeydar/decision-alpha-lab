---
id: EXP0018-P01-17-HANDOFF-TO-P02-AND-P03
title: "EXP0018 P01 — Handoff to P02 and P03"
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


# تحویل به P02

P02 از snapshot فقط این موارد را می‌گیرد:

- UTC instant؛
- NY time؛
- trading-day key؛
- replay-safe flag؛
- status.

P02 اجازه بازتعریف DST ندارد.

# تحویل به P03

P03 از period windowها استفاده می‌کند:

- instance_id؛
- start/end UTC؛
- start/end NY؛
- family/code؛
- variable duration flag.

P03 باید incomplete market data را جدا از valid time window مدیریت کند.

