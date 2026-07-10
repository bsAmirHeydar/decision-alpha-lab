---
id: EXP0018-P02-DATA-QUALITY
title: "P02 Data Quality Rules"
type: quality-contract
status: active
project: EXP0018
---
# قواعد کیفیت

Critical failures:

- duplicate UTC timestamp در یک symbol
- non-monotonic chronology
- invalid OHLC
- time conversion failure

Configurable conditions:

- stale latest closed bar
- partial alignment
- invalid bar tolerance

Default strict است: هر invalid bar load را fail می‌کند. Freshness به‌صورت پیش‌فرض خاموش است تا weekend و market closure با data corruption اشتباه نشوند.
