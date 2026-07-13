---
title: "ADR — Adapters Are Read-Only Projections"
tags: [exp0019, faerie-protocol, fp-i01, compatibility, adapter-contracts]
status: normative
phase: FP-I01
phase_version: 1.0.0
doc_version: 1.0.0
last_updated: 2026-07-13
language: en
---
# Adapters Are Read-Only Projections

## Status

Accepted for FP-I01 v1.0.0.

## Decision

All FP-I01 adapters accept immutable/const source snapshots and write only neutral FP-owned target structures.

## Context

A compatibility adapter must not become a second engine, state store, or policy layer.

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
