---
id: UCPS-3705550FE160
title: "Critical Path, Stage Dependencies and Stop Rules"
type: standard
status: canonical
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-23
updated: 2026-07-23
tags:
  - consolidation
  - platform-seal
---
# Critical Path, Stage Dependencies and Stop Rules

## Critical path

```text
UC-01 → UC-02 → UC-03 → UC-04 → UC-05 → UC-06 → UC-07
```

Stages are sequential at the acceptance boundary. Parallel work is allowed only within a stage when workstreams have disjoint write sets and a shared baseline.

## Hard dependencies

- UC-03 cannot move an asset without UC-02 disposition.
- UC-04 cannot retire a duplicate without UC-01 behavior evidence and UC-03 stable location.
- UC-05 cannot generalize RTHP by deleting special behavior before UC-04 preservation.
- UC-06 cannot cut over external consumers without environment evidence.
- UC-07 cannot delete any active source while compatibility telemetry is non-zero.

## Global stop conditions

Evidence corruption, missing LFS objects, unexplained numerical delta, known-time regression, secret exposure, live-authority escalation, recovery failure, unknown required consumer or unreviewed destructive diff stops the affected wave.

## No schedule pressure exception

Time, patch size and documentation volume do not justify bypassing a gate. Work may be partitioned into smaller waves, but acceptance semantics remain unchanged.
