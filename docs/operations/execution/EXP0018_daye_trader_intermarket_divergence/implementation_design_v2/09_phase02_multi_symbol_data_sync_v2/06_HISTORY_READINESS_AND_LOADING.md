---
id: EXP0018-P02-HISTORY-READINESS
title: "P02 History Readiness and Loading"
type: specification
status: active
project: EXP0018
---
# آمادگی history

Pipeline هر symbol:

1. symbol selection
2. `SERIES_SYNCHRONIZED`
3. `Bars()` minimum count
4. `CopyRates()` checked count
5. تبدیل و validation تک‌تک barها
6. chronological audit

History ممکن است هنگام attach هنوز آماده نباشد. این حالت runtime-retry است و Expert را از کار نمی‌اندازد. Status برابر `HISTORY_NOT_SYNCHRONIZED` یا `INSUFFICIENT_BARS` می‌شود و timer دوباره تلاش می‌کند.
