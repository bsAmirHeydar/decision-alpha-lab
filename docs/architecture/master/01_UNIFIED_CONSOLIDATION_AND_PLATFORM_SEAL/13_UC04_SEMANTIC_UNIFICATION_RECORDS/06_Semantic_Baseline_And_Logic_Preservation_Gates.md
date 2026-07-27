---
id: UCPS-5E66194C99CE
title: "Semantic Baseline and Logic Preservation Gates"
type: standard
status: canonical
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-27
updated: 2026-07-27
tags:
  - consolidation
  - uc04
  - logic-preservation
---
# Semantic Baseline and Logic Preservation Gates

## W0 freeze

`semantic_baseline_freeze.json` binds the recovered path resolver, RTHP activation packages, ACL policies, generated acceptance evidence, registrations and engine baseline amendments to exact SHA-256 identities.

This freeze is the before-state for UC04-W1. Changing a frozen file without regenerating and reviewing the corresponding evidence invalidates the candidate gate.

## Required records for a semantic candidate

A UC-04 candidate requires:

1. capability migration ledger row;
2. source and consumer inventory;
3. semantic equivalence record;
4. logic-preservation certificate;
5. consumer cutover record;
6. rollback evidence;
7. a separately authorized retirement decision if deletion is requested.

## Observable dimensions

Characterization must include, where applicable:

- exact output bytes and normalization;
- ordering and stable identity;
- known-time and closed-bar behavior;
- null, stale and partial-data behavior;
- file, network, chart-object and global-state side effects;
- symbol, timeframe, precision and tick-size dependence;
- error type, message and fail-closed behavior;
- performance envelope without removing validation.

## Acceptance rule

Source similarity is not semantic equivalence. Compilation is not semantic equivalence. Passing only the new implementation tests is not semantic equivalence.

A candidate may cut consumers over only after the old and new implementations are exercised against the same fixture corpus and produce the approved observable result. Deletion remains false until every known consumer is migrated and zero-use evidence is accepted.
