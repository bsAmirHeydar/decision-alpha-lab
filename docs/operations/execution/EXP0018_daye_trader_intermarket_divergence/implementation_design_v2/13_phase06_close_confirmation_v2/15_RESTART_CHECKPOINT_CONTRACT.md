---
id: EXP0018-P06-CHECKPOINT
title: "P06 Restart Checkpoint Contract"
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

# Checkpoint

The default checkpoint is stored in MetaTrader Common Files and is namespaced by prefix, canonical symbol pair, and host timeframe.

Persisted data:

- latest processed closed host-bar open;
- every pending candidate;
- finalized observation IDs.

The checkpoint is state recovery, not research truth. P12 audit remains the durable event ledger. Corrupt or schema-mismatched checkpoints fail initialization instead of silently resetting identity.
