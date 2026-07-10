---
id: EXP0018-P11-19_PERFORMANCE_BUDGET
title: "Performance budget"
project: EXP0018
phase: P11
status: implemented
tags: [exp0018, daye, phase11, replay]
---

# Performance budget

The reference implementation rebuilds as-of stores per cursor to maximize transparency and equivalence. Operators should use bounded ranges and timer chunks. The default one-week M1 range is appropriate for validation. Later optimization may introduce incremental reducers only after golden-output equivalence is proven.
