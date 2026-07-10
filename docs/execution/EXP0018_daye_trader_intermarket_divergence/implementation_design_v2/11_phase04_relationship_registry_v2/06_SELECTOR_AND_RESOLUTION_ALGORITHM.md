---
id: EXP0018-P04-RESOLUTION
title: "P04 Selector and Resolution Algorithm"
type: algorithm-spec
status: active
project: EXP0018
phase: P04
---
# Selector and Resolution Algorithm

Two selectors exist:

1. `PREVIOUS_SAME_CODE`: used by DD and WW.
2. `PREVIOUS_CHRONOLOGICAL`: used by session and subcycle chains.

Resolution steps:

```text
for each paired period:
  for each registry definition matching current_period_id:
    enforce family enable flag
    enforce doctrine readiness
    enforce current eligibility
    read declared previous-link field
    locate exact paired-period ID
    verify expected reference period ID/code
    enforce reference completeness
    build deterministic opportunity ID
    reject duplicates
    publish typed resolution
```

Nearest periods, array index, price similarity, and guessed fallback are forbidden.
