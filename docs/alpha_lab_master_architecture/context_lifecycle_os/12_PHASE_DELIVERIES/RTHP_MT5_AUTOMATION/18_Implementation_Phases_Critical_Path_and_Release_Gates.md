---
title: RTHP MT5 Automation — Implementation Phases, Critical Path, and Release Gates
status: roadmap-approved-for-implementation
version: 1.0.0
updated: 2026-07-22
tags: [rthp, implementation, critical-path, release-gates]
---

# Implementation Phases, Critical Path, and Release Gates

These are RTHP-owned implementation increments, not new ACL lifecycle phases.

## RTHP-MT5-I00 — Documentation and authority freeze

- approve this roadmap;
- freeze M1 data floor;
- freeze no-engine-change and no-trade boundaries;
- publish schemas and reason-code plan.

## RTHP-MT5-I01 — Terminal and symbol adapter

- terminal discovery and health;
- symbol enumeration and selection;
- metadata snapshot;
- fake-provider tests.

## RTHP-MT5-I02 — M1 acquisition and source receipts

- UTC chunked history download;
- retry/resume;
- current-bar exclusion;
- acquisition receipt ledger.

## RTHP-MT5-I03 — Quality, calendar, and common range

- M1 validation;
- gap taxonomy;
- joint-session alignment;
- common-history resolver.

## RTHP-MT5-I04 — Immutable source binding

- normalized M1 artifacts;
- hashes and provenance;
- real-data binding;
- atomic source freeze.

## RTHP-MT5-I05 — RTHP M1 materialization adapter

- M1 interval touch semantics;
- M15 confirmation from M1;
- four ledgers;
- compatibility and causality tests.

## RTHP-MT5-I06 — One-click train orchestration

- default profile resolution;
- existing Train Activation delegation;
- resume and verification;
- operator summary.

## RTHP-MT5-I07 — Hardening and first real run

- clean installation;
- real terminal smoke;
- historical coverage audit;
- end-to-end train run;
- independent evidence review.

## Critical path

```text
I00 → I01 → I02 → I03 → I04 → I05 → I06 → I07
```

No phase may bypass source quality, immutable binding, or existing train preflight.
