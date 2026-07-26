---
id: UCPS-UC01-CHARTER-C5B7E201
title: "UC-01 Implementation Charter"
type: execution_charter
status: implemented_reference
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-23
updated: 2026-07-23
tags:
  - consolidation
  - uc-01
  - charter
---
# UC-01 Implementation Charter

## Mission

UC-01 establishes a complete, recoverable and behavior-aware baseline of the current Alpha Lab repository before any physical reorganization, semantic merge, consumer cutover or deletion is permitted.

## Implementation boundary

The implementation adds scanners, contracts, policies, tests, preservation tools and baseline receipts. It does **not** move, rename, merge, supersede, cut over or delete any pre-existing source artifact. It includes exactly eleven bounded baseline-stabilization repairs that restore malformed newline string literals in already-existing Python files. Those repairs are syntax restoration only, are enumerated in the release manifest, and become effective only after the pre-repair repository state is protected by the UC-01 preservation tag, archive branch, bundle and source archive.

## Authority ceiling

- file deletion: forbidden
- file movement: forbidden
- semantic refactoring: forbidden
- bounded syntax restoration: allowed only for the eleven manifest-declared baseline-stabilization paths after pre-state preservation
- import rewrite: forbidden
- consumer cutover: forbidden
- runtime activation: forbidden
- order authority: forbidden
- capital authority: forbidden
- UC-02 authorization: permitted only after every non-compensatory gate passes

## Evidence products

The authoritative baseline root is `registry/consolidation/uc01/baselines/UC01_BASELINE_V1/`. Large inventories are deterministic gzip JSONL; decision, environment, recovery and handoff records remain readable JSON.

## Completion meaning

Implementation completion means the mechanism exists and passes its own tests. Stage acceptance is a separate decision produced from the actual user repository after Git LFS materialization, full capture, external preservation, recovery drill and qualification.
