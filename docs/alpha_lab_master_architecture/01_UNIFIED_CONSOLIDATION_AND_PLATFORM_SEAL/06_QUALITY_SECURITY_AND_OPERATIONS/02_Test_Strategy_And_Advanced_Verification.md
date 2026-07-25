---
id: UCPS-F6C7F4D7BDEF
title: "Test Strategy and Advanced Verification"
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
# Test Strategy and Advanced Verification

## Layers

Unit tests protect local behavior. Contract tests protect interfaces. Property and metamorphic tests protect invariants. Differential tests protect migrations. Mutation tests assess whether tests detect meaningful faults. Integration tests verify service boundaries. End-to-end tests prove complete lifecycle behavior.

## Characterization versus specification

Characterization records old behavior. Specification tests define accepted future behavior. When they differ, the change requires an explicit defect or ADR record.

## Coverage

Line coverage is diagnostic, not acceptance. Critical decision, authority, time and money paths require branch, condition and mutation strength evidence.

## Flakiness

Flaky tests are defects. Retries may collect evidence but cannot convert nondeterminism into PASS. Random tests use recorded seeds and failure replay.
