---
id: EXP0018-P02-BASE-BAR-CONTRACT
title: "P02 Base Bar Data Contract"
type: data-contract
status: active
project: EXP0018
---
# قرارداد bar پایه

Default برابر M1 و closed-bars-only است. هر bar باید:

- timestamp مثبت
- قیمت‌های finite و مثبت
- `high >= open, close, low`
- `low <= open, close, high`
- volume و spread غیرمنفی

داشته باشد.

`event_time_utc` زمان بازشدن bar است. `close_time_utc` زمان در دسترس‌شدن کامل bar است. `availability_time_utc` pair حداکثر close time دو bar است.
