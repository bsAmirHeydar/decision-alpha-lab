---
id: EXP0018-P02-NO-EXECUTION
title: "P02 Security and No-Execution Boundary"
type: boundary
status: active
project: EXP0018
---
# مرز امنیتی

این فاز شامل این موارد نیست:

```text
CTrade
OrderSend
PositionOpen
WebRequest
risk sizing
target logic
signal filtering
```

SymbolSelect فقط data availability را مدیریت می‌کند. هیچ تغییر account یا position مجاز نیست.
