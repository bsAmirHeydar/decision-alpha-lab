---
title: "ADR — Neutral Contracts Do Not Define FP Semantics"
tags: [exp0019, faerie-protocol, fp-i01, compatibility, adapter-contracts]
status: normative
phase: FP-I01
phase_version: 1.0.0
doc_version: 1.0.0
last_updated: 2026-07-13
language: en
---
# Neutral Contracts Do Not Define FP Semantics

## Status

Accepted for FP-I01 v1.0.0.

## Decision

Neutral snapshots expose common facts but do not define A/L/N, AL/AN/LN/NA/NL/NN/WW, WW recency, quota, drawing, or tradeability.

## Context

Mixing compatibility facts with FP policy would make adapters context-specific engines.

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
