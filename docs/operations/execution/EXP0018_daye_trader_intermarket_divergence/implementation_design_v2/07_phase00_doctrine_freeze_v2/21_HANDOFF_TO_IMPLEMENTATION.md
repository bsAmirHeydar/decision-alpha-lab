---
id: EXP0018-P00-HANDOFF
title: "EXP0018 Phase 00 — Handoff to Implementation"
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

# تحویل Phase 00 به فازهای بعدی

## خروجی به P01

- Time contract پذیرفته‌شده؛
- DST policy؛
- Trading Day/session/subcycle boundaries؛
- Weekly/TWO decisions برای قسمت‌های وابسته.

## خروجی به P02

- symbol pair semantics؛
- No Data policy؛
- timestamp alignment requirement.

## خروجی به P03

- Period types و completeness؛
- Daily/Weekly boundaries؛
- stable period identity.

## خروجی به P04

- 22 relationship snapshot؛
- NP و WW enablement؛
- Core/SSMT separation.

## خروجی به P05/P06

- touch-only semantics؛
- direction mapping؛
- close-only finalization؛
- double-hunt behavior.

## خروجی به P07/P08

- First Sweep scope؛
- lifecycle terminal states؛
- line persistence.

## اصل مهم

فاز بعدی فقط fieldهای تصویب‌شده را مصرف می‌کند. `OPEN` یا `PROPOSED` نباید در کد به default پنهان تبدیل شود.
