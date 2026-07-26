---
id: EXP0018-P01-05-TRADING-DAY-AND-GAP
title: "EXP0018 P01 — Trading Day and Gap"
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


# روز Daye

```text
Start inclusive: 18:00:00 NY
End exclusive:   17:00:00 NY next civil date
```

کلید روز با کم‌کردن ۱۸ ساعت از NY time ساخته می‌شود. بنابراین:

- 17:59 روز 10 ژوئیه → کلید 9 ژوئیه؛
- 18:00 روز 10 ژوئیه → کلید 10 ژوئیه.

## Gap

```text
[17:00:00, 18:00:00)
```

در gap:

- session = NONE؛
- subcycle = NONE؛
- `in_declared_session_gap=true`؛
- داده «ناموجود» نیست؛ وضعیت زمانی معتبر ولی خارج از سشن است.

این تمایز برای P02/P03 حیاتی است.

