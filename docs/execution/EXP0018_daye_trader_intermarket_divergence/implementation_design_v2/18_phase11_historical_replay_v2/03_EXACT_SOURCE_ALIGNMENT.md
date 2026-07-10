---
id: EXP0018-P11-03_EXACT_SOURCE_ALIGNMENT
title: "Exact source alignment"
project: EXP0018
phase: P11
status: implemented
tags: [exp0018, daye, phase11, replay]
---

# Exact source alignment

SPX and NDX historical bars are joined only when `event_time_utc` is equal. Strict replay rejects unmatched timestamps. It does not nearest-match, forward-fill, substitute previous closes, synthesize bars, or infer no-hunt from absent data. This is stronger than exploratory partial alignment because equivalence claims require a common causal source grid.
