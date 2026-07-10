---
id: EXP0018-P04-RUNTIME
title: "P04 Runtime Validation Guide"
type: validation-guide
status: active
project: EXP0018
phase: P04
---
# Runtime Validation

Compile the P04 Expert with zero errors and warnings. Verify embedded tests pass. On a synchronized SPX/NDX M1 history, confirm registry count 22, ready registry count 20, blocked count 2, and at least one ready resolution. Inspect the optional audit CSV and verify exact current/reference IDs rather than bar-index adjacency.

WW and NP must remain blocked. No chart line should be created by P04.
