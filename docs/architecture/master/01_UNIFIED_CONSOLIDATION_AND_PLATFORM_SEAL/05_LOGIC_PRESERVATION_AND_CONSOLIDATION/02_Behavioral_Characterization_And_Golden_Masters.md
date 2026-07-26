---
id: UCPS-DD9B3E46CFE1
title: "Behavioral Characterization and Golden Masters"
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
# Behavioral Characterization and Golden Masters

## Purpose

Characterization captures what current code does before deciding what it should do. This separates semantic preservation from later improvement.

## Required cases

Normal cases, boundaries, invalid inputs, stale and missing data, duplicate and reordered observations, DST, session boundaries, multi-symbol timing, restart, persistence, floating-point tolerance, cost assumptions and abstention.

## Golden Masters

Golden outputs include normalized traces, state transitions, reason codes, artifact digests and terminal reports. Raw timestamps and environment-specific noise are normalized under documented rules.

## Defect discovery

If characterization reveals an existing defect, preserve the observed behavior in a baseline record, create a defect record and separately approve the correction. The refactor must not hide the behavioral change.
