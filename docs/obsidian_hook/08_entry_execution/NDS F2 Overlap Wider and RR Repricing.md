---
title: NDS F2 Overlap Wider and RR Repricing
aliases:
  - F2 Wider Context Arbitration
  - F2 Minimum RR Repriced Entry
status: implemented
phase: F2 waist-break Point2 v5
---

# NDS F2 Overlap Wider and RR Repricing

## Canonical links

- [[NDS F2 Waist-Break Point2 Limit Setup]]
- [[NDS F2 RR Hedge and Parallel Contexts]]
- [[NDS_ENTRY_EXECUTION_MOC]]

## Duplicate rule

Two same-direction contexts are one opportunity when the intersection of their final Entry-to-Stop corridors covers at least the configured percentage of the narrower corridor. Default is 80%; 70% can be selected through Input. The wider corridor wins.

## RR rule

When the original limit behind F2 Waist provides less than the configured RR, Stop and Target remain fixed and Entry is moved toward Stop to the exact minimum-RR boundary, then rounded toward Stop by symbol tick.

```text
Entry* = (Target + Rmin × Stop) / (1 + Rmin)
```

## Lifecycle

- same bar: keep wider before any send;
- wider later while narrower is pending: replace pending;
- wider later after fill: keep existing position, block duplicate;
- opposite direction: defer to hedge policy, no overlap merge.
