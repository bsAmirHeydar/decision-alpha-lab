---
id: EXP0018-P00-CONFIRM
title: "EXP0018 Phase 00 — Close Confirmation Doctrine"
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

# دکترین تأیید در Close

## مرز تأیید

Host Timeframe همان تایم‌فریم چارت Expert است. فقط آخرین کندل بسته‌شده می‌تواند Signal State را نهایی کند.

## ماشین حالت

```text
NONE
  → CANDIDATE_HIGH / CANDIDATE_LOW
  → CONFIRMED
  → INVALIDATED_DOUBLE_HUNT
  → INVALIDATED_NO_LONGER_ONE_SIDED
  → UNAVAILABLE_DATA
```

## مثال

در M30، اگر در دقیقه پنجم فقط NDX high مرجع را بزند اما تا پایان M30، SPX نیز high خودش را بزند:

```text
Intrabar candidate existed
Final close state = DOUBLE_HUNT
No confirmed line
```

اگر Relationship دیگری در همان کندل one-sided باقی بماند، همان Relationship مستقل تأیید می‌شود.

## Idempotency

برای هر `confirmation_bar_close + relationship + side + reference IDs` فقط یک transition نهایی مجاز است. Reattach، duplicate tick یا repeated timer نباید event دوم بسازد.

## No repaint

پس از بسته‌شدن کندل و ثبت event، داده آینده حق تغییر وضعیت تاریخی همان event را ندارد. lifecycle آینده می‌تواند reference را retire کند، اما event تاریخی را بازنویسی نمی‌کند.
