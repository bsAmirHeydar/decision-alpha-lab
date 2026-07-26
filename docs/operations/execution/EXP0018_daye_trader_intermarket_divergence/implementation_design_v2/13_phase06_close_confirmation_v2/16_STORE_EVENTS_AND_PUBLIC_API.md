---
id: EXP0018-P06-STORE
title: "P06 Store, Events, and Public API"
type: implementation-note
status: implemented
project: EXP0018
phase: P06
version: 2.0.0
created: 2026-07-10
updated: 2026-07-10
tags:
  - exp0018
  - p06
  - confirmation
---

# Store

The store owns pending candidates, bounded runtime results, finalized IDs, and prior P05 source memory.

# Events

Events include engine initialization, source baseline, candidate open/update, host close, confirmed, double-hunt invalidation, no-signal, unavailable, missed close, checkpoint restore/save, and status change.

# Public API

- `GetCurrentSummary`;
- `ExportCandidates`;
- `ExportResults`.

Consumers receive copies, not mutable store references.
