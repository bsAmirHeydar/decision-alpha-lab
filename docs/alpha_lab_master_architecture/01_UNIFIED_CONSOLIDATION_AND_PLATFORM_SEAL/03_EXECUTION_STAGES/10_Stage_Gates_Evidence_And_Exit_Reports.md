---
id: UCPS-B690C84D8AB5
title: "Stage Gates, Evidence and Exit Reports"
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
# Stage Gates, Evidence and Exit Reports

## Gate dimensions

Every stage evaluates structure, behavior, dependencies, documentation, security, authority, reproducibility, recovery and external evidence. Results are `PASS`, `FAILED`, `BLOCKED` or `NOT_APPLICABLE` with reason.

## Non-compensation

A stage with one required `BLOCKED` dimension does not pass because thousands of tests succeeded elsewhere. `NOT_APPLICABLE` requires a documented scope proof.

## Exit report

The exit report contains baseline identity, changed paths, output digests, tests, environment, defects, residual risks, waivers, recovery evidence, approvals and next-stage handoff.

## Acceptance authority

Implementation authors may not be the sole approvers for destructive deletion, security boundary change or final seal. The report records signer role and reviewed digest.
