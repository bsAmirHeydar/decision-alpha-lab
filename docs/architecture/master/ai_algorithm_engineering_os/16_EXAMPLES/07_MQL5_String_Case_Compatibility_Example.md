---
id: AIEOS2-7411EA4DABDD
title: "MQL5 String Case Compatibility Example"
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
# MQL5 String Case Compatibility Example

## Failure

```mql5
string value = StringToUpper(Clean(source));
```

MetaEditor reports `lvalue expected` because the function mutates a writable string and returns `bool`.

## Correct Pattern

```mql5
string value = Clean(source);
StringToUpper(value);
```

## Lesson

Compiler diagnostics that appear as conversion warnings after this line are cascading symptoms. Fix the first language-rule violation.
