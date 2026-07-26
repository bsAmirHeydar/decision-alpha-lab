---
title: "ADR — Shared Cores Remain Semantic Owners"
tags: [exp0019, faerie-protocol, fp-i01, compatibility, adapter-contracts]
status: normative
phase: FP-I01
phase_version: 1.0.0
doc_version: 1.0.0
last_updated: 2026-07-13
language: en
---
# Shared Cores Remain Semantic Owners

## Status

Accepted for FP-I01 v1.0.0.

## Decision

EXP0017, EXP0018, and Strategy Factory retain ownership of their time, reference, hunt, confirmation, lifecycle, visual, economics, paper, and live semantics.

## Context

Copying or forking source logic would permit contexts to drift and make regressions invisible.

## Consequences

- The rule is represented in code, tests, artifacts, and delivery validation.
- Violations fail closed and block handoff.
- A change requires a new exact version and reviewed migration/rebaseline.
- Previous-context evidence remains retained.

## Rejected alternatives

- Silent compatibility based on file names.
- Mutable adapters that repair source data.
- Reimplementing shared algorithms inside Faerie Protocol.
- Treating static validation as a successful MetaEditor compile.

## Verification

- Python contract and negative tests.
- Source hash guard.
- Golden adapter fixtures.
- MQL5 static and local compile gates.
- Patch-index ownership check.

## Navigation

- [[../00_FP_I01_DELIVERY_MOC|FP-I01 Delivery MOC]]
