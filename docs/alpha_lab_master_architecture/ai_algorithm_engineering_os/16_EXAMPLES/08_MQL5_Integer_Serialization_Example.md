---
id: AIEOS2-FFB6C0643118
title: "MQL5 Integer Serialization Compatibility Example"
type: example
status: active
domain: example
version: 2.0.0
created: 2026-07-10
updated: 2026-07-10
tags:
  - ai-engineering
  - alpha-lab
  - example
---
# MQL5 Integer Serialization Compatibility Example

## Failure

A code generator assumes `LongToString` exists. The target compiler reports an undeclared identifier and then parser warnings in the surrounding concatenation.

## Correct Project Pattern

```mql5
string size_text = IntegerToString(size_bytes);
```

Keep the data field typed as `long`; change only the compatible serialization call. Recompile dependent experts.
