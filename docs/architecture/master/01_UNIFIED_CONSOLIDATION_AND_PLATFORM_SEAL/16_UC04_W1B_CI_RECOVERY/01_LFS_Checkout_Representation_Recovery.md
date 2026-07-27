---
id: UCPS-5F0718C25D4E
title: "UC04-W1B CI LFS Checkout Representation Recovery"
type: implementation-record
status: accepted
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-27
updated: 2026-07-27
tags:
  - consolidation
  - uc04
  - w1b
  - ci
  - git-lfs
  - recovery
---
# UC04-W1B CI LFS Checkout Representation Recovery

## Incident

The accepted UC04-W0 verifier treated the working-tree representation of four historical Git LFS artifacts as the canonical evidence. GitHub Actions checked out those paths with LFS hydration enabled, so the working tree contained valid hydrated objects rather than pointer text. The verifier therefore rejected a valid checkout before W1B checks could run.

## Corrected contract

The canonical Git blob remains the Git LFS pointer. The working tree may validly contain either:

1. the exact pointer representation, as in a source archive or skip-smudge checkout; or
2. a hydrated object whose byte length and SHA-256 match the pointer metadata stored in `HEAD`.

Any missing path, malformed canonical pointer, pointer metadata mismatch, hydrated-size mismatch, or hydrated-digest mismatch fails closed.

## Scope and non-goals

This recovery changes verification only. It does not modify workflows, historical W0 release ledgers, market data, trading semantics, MQL5 consumers, execution behavior, runtime authority, order authority, or capital authority.

## Historical release preservation

The original UC04-W0 hash ledger remains unchanged. The verifier change is admitted through `releases/unified_consolidation/ci_recovery_03/UC04_W0_RELEASE_AMENDMENT.json`, which binds the original verifier hash to the corrected verifier hash and grants no semantic or execution authority.
