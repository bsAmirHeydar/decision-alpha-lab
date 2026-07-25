---
id: UCPS-372AF7B758FC
title: "Wave, Commit, Branch and Integration Strategy"
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
# Wave, Commit, Branch and Integration Strategy

## Branch model

- immutable tag and archive branch before UC-01;
- one long-lived consolidation branch;
- short-lived wave branches for bounded work;
- protected main branch;
- no direct destructive experimentation on main.

## Wave properties

A wave has one capability or one relocation family, an exact file set, explicit consumers, characterization tests, rollback plan and acceptance command. Large mixed patches that combine movement, semantic rewrite and feature addition are prohibited.

## Commit discipline

Commits are ordered to preserve bisectability:

1. tests and fixtures;
2. canonical destination implementation;
3. consumer rewrites;
4. compatibility telemetry if required;
5. retirement or deletion;
6. documentation and generated projections.

## Integration

Every wave rebases on the accepted stage baseline, runs targeted tests plus repository preflight and publishes a machine-readable receipt. The stage closes only after the integrated branch passes full acceptance.
