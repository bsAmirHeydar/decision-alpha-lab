---
id: EXP0018-P02-RUNTIME-VALIDATION
title: "P02 Runtime Validation Guide"
type: runbook
status: active
project: EXP0018
---
# راهنمای تست در MT5

1. هر دو symbol را در Market Watch فعال کن.
2. history M1 هر دو را باز و دانلود کن.
3. Expert P02 را روی یک chart attach کن.
4. `InpPrintSymbolHealthOnRefresh=true` بگذار.
5. باید `series_synchronized=true` و `aligned >= minimum` ببینی.
6. با انتخاب symbol اشتباه Init باید fail شود.
7. با قطع history یکی از symbolها status باید unavailable شود؛ نه aligned false data.
8. Audit CSV را یک بار روشن و pair time/price را با chart تطبیق بده.
