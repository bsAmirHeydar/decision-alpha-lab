---
title: "LCM-08B — 09 Reference Family Semantics"
status: accepted-reference
version: 1.0.0
updated: 2026-07-19
tags: [acl-os, lcm, lcm-08b, pilot-migration]
phase_id: LCM-08B
---
# Reference Family Semantics

`previous_candle` uses `i-1`. `rolling` uses extrema in `[max(0,i-lookback), i)`. `current_session` uses prior bars on the same calendar date that satisfy the session predicate. `previous_session` uses the most recent prior calendar date with qualifying bars. Equal extrema retain pandas first-index behavior. No reference consumption lifecycle exists in the legacy batch.
