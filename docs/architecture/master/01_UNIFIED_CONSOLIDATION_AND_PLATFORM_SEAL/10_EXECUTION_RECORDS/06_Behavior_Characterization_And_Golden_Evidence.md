---
id: UCPS-UC01-BEHAVIOR-91C86204
title: "Behavior Characterization and Golden Evidence"
type: implementation_standard
status: approved
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-23
updated: 2026-07-23
tags:
  - behavior
  - characterization
  - tests
---
# Behavior Characterization and Golden Evidence

Critical logic is grouped into kernel, market, context, treatment, research, evidence, capital, runtime, execution and monitoring domains.

Every critical artifact must have:

1. immutable source SHA-256;
2. public symbol-surface fingerprint;
3. critical-domain assignment;
4. executable test evidence at the domain level;
5. explicit `retirement_allowed: false` during UC-01.

Existing test functions and classes are inventoried as evidence. Static surface fingerprints preserve structure where direct execution is unsafe or unavailable, but they are labeled separately from executable evidence. Missing executable evidence in a required critical domain blocks stage acceptance.
