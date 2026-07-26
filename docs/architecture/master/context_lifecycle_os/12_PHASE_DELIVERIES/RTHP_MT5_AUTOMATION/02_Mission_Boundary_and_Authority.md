---
title: RTHP MT5 Automation — Mission, Boundary, and Authority
status: roadmap-approved-for-implementation
version: 1.0.0
updated: 2026-07-22
tags: [rthp, mt5, authority, boundary]
---

# Mission, Boundary, and Authority

## In scope

- Read-only MetaTrader 5 terminal discovery and connection.
- Broker-symbol discovery and deterministic alias resolution.
- M1 historical bar acquisition.
- Source coverage and quality validation.
- UTC and New York time normalization.
- Immutable source artifacts, manifests, receipts, hashes, and provenance.
- RTHP-owned M1 materialization adapter.
- Invocation of the existing RTHP Train Activation and existing central engines.
- One-click orchestration, resume, verification, and operator diagnostics.

## Out of scope

- Changing RTHP semantics.
- Changing any shared ACL, SAED, UCEE, dataset, trainer, validator, reporting, promotion, or runtime engine.
- Creating or submitting orders.
- Requesting sub-M1 data for canonical research.
- Inferring tick order from M1 OHLC.
- Silently filling or interpolating missing bars.
- Automatically changing canonical symbol identity or contract-roll policy.
- Activating capital.

## Authority model

The adapter has **read-data authority only**. It may call approved terminal-information, symbol-information, and bar-history functions. It must not call any trade, position, order, or account-mutation function.

## Required invariance evidence

Every release must prove:

```text
central_engine_modified = false
canonical_context_modified = false
order_authority_created = false
capital_authority_created = false
sub_m1_canonical_source_enabled = false
```
