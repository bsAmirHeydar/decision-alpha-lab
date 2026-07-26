---
title: "Indicator Visual Language and Object Identity"
tags: [exp0019, faerie-protocol, implementation-program, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
implementation_program: FP-IMP-001
program_version: 1.0.0
doc_version: 1.0.0
last_updated: 2026-07-13
language: en
---
# Indicator Visual Language and Object Identity

## Visual hierarchy

1. **Context background:** session boxes and week boundaries.
2. **Reference structure:** high/low lines and labels.
3. **Hunt evidence:** Hunter touch marker and protected level evidence.
4. **Signal evidence:** relation connector, direction, confirmation marker.
5. **Policy overlay:** WW alignment, quota suppression, missing-data status.
6. **Operator UI:** panel, filters, diagnostics.

## Object identity

Canonical object key material:

```text
FP | product-version | chart-id | instance-id | config-hash |
projection-kind | semantic-id | projection-revision
```

Object names are deterministic projections but are never the source-of-truth signal ID.

## Required styles

| State | Visual behavior |
|---|---|
| raw hunt | small neutral marker |
| candidate | dashed relation line and pending label |
| confirmed bullish | bullish relation style |
| confirmed bearish | bearish relation style |
| invalidated | muted strike/invalid marker |
| neutralized | neutral style retaining historical geometry |
| suppressed by WW | visible muted style + `SUPPRESSED_BY_WW` |
| suppressed by quota | visible muted style + `SUPPRESSED_BY_QUOTA` |
| data incomplete | warning style; never pretend no signal |
| entry eligible | explicit eligibility badge, not recoloring raw state only |

## Scale and timeframe behavior

- Detection does not change when the chart timeframe changes.
- Confirmation semantics change only through the resolved confirmation timeframe in config identity.
- Labels use responsive offsets based on visible price range and font metrics.
- Object placement must avoid overlap using stable lane allocation, not random pixel shifting.
- Historical objects may be culled outside configured display depth without deleting ledger history.
