---
id: UCPS-368129098ED5
title: "Definition of Done and Quality Bar"
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
# Definition of Done and Quality Bar

## Stage done

A stage is done only when its declared outputs exist, all mandatory gates pass, the work is reproducible from a clean clone, rollback or recovery is proven and the next stage receives a hash-bound handoff.

## Program done

The program is done only when:

- one production source root remains;
- all active shared capabilities have one canonical implementation;
- three distinct Golden Contexts pass universal end-to-end execution;
- all known consumers use canonical interfaces;
- no compatibility telemetry remains;
- P0 and P1 defects equal zero;
- required evidence contains no UNKNOWN or BLOCKED dimension;
- obsolete duplicates are removed from the active branch;
- platform policies prevent structural regression;
- the seal certificate is issued.

## Defect policy

P0 and P1 defects block stage closure. P2 defects may remain only with owner, accepted risk, bounded scope, regression test and removal plan. Documentation inconsistencies that can misdirect implementation are classified as functional defects, not cosmetic issues.
