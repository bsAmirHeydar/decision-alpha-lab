---
id: UCPS-32A735EC9440
title: "Retirement, Quarantine, Deletion and History Preservation"
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
# Retirement, Quarantine, Deletion and History Preservation

## Final dispositions

`ACTIVE_CANONICAL`, `ACTIVE_EXTENSION`, `FIXTURE_ONLY`, `HISTORICAL_ONLY`, `SUPERSEDED`, `REJECTED_WITH_EVIDENCE`.

## Quarantine

Quarantine is used for unresolved behavior, ownership or consumer evidence. It has owner, reason, evidence gap and deadline. Indefinite `BLOCKED` is not an acceptable final disposition.

## Deletion gate

Deletion requires preserved history, canonical destination or explicit historical-only decision, zero active consumers, parity or approved semantic-change evidence, recovery proof and independent approval.

## History

Git tags, archive branches, bundles and immutable release indexes preserve historical source. The active branch is an operational product, not the storage location for every delivery artifact ever created.
