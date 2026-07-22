---
title: RTHP MT5 Automation — Session-Aware Gap, Duplicate, and Cross-Symbol Quality Gates
status: roadmap-approved-for-implementation
version: 1.0.0
updated: 2026-07-22
tags: [rthp, data-quality, gaps, alignment]
---

# Session-Aware Gap, Duplicate, and Cross-Symbol Quality Gates

## Structural gates

Hard-fail conditions:

- invalid schema;
- non-finite or non-positive prices;
- `low > high`;
- Open or Close outside `[low, high]`;
- non-M1 timeframe;
- current incomplete bar admitted;
- duplicate key with conflicting values;
- out-of-order canonical sequence;
- tick-size or symbol metadata mutation without a version boundary;
- unknown timezone or calendar classification;
- no usable common history.

## Gap taxonomy

A missing timestamp is not automatically bad data. Classify each absence as:

- expected market closure;
- symbol-specific closure;
- holiday/early close;
- no broker bar because no quote/tick occurred;
- terminal-history truncation;
- acquisition failure;
- unexplained gap.

Only the first four can be accepted under explicit policy. Truncation, acquisition failure, and unexplained gaps block the affected region.

## Cross-symbol alignment

For every M15 confirmation cut:

- both symbols must have sufficient closed M1 coverage;
- missing or stale input yields `UNCONFIRMED`;
- no forward filling or interpolation is allowed;
- common coverage and pair-specific gaps are reported separately.

## Quality decision

```text
PASS
PASS_WITH_DECLARED_NON_CRITICAL_GAPS
BLOCKED
```

A warning may never silently become a pass unless its classification and policy are recorded.
