---
id: UCPS-FAEEA04F8D12
title: "Python/MQL5 Parity and Compiled Evidence"
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
# Python/MQL5 Parity and Compiled Evidence

## Parity scope

State transitions, Context occurrence, known-time guards, numerical transforms, Treatment decisions, risk calculations and reason codes require shared case IDs and comparable normalized traces.

## Required terminal evidence

Static scan is not compile evidence. Accepted terminal changes require MetaEditor compilation, emitted binary digest, terminal build identity, Strategy Tester report, journal, inputs, data range and normalized result digest.

## Tolerance

Numeric tolerance is field-specific and justified. Discrete states, reason codes and authority decisions require exact equality.

## Failure handling

A mismatch is classified as Python defect, MQL5 defect, contract ambiguity, environment variance or unresolved. It cannot be averaged away or ignored because aggregate performance is similar.
