---
id: EXP0018-P02-PERFORMANCE
title: "P02 Performance and Determinism"
type: engineering-standard
status: active
project: EXP0018
---
# کارایی و determinism

- historical loops bounded by requested bars
- alignment complexity O(A+B)
- no full scan on every tick
- IDs based on stable inputs
- exact timestamp comparison
- no random state
- manual broker offset remains replay canonical

Auto-current broker offset inherits P01 replay warning and marks bars/pairs replay-unsafe.
