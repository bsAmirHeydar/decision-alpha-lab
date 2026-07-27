---
id: UCPS-A68C2D9F504B
title: "UC04-W1B Evidence Review and Conditional Cutover"
type: governance-record
status: canonical
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-27
updated: 2026-07-27
tags:
  - consolidation
  - uc04
  - w1b
  - evidence
  - cutover
---
# UC04-W1B Evidence Review and Conditional Cutover

## Independent review

The native receipt cannot authorize itself. A separate Python reviewer recomputes current source hashes, compile log hashes, EX5 hashes, the clean-compile result, runtime CSV hash, fixture order, fixture bytes, summary status, and the absence of authority grants.

A review is PASS only when it is hash-bound to the exact receipt and the current repository still reproduces the W1A characterization.

## Conditional candidate generation

After a PASS receipt and PASS independent review, the candidate builder may generate a non-apply-authorized payload under `.alpha/runs/uc04w1b/cutover_candidates`.

The generated shape is deliberately bounded:

1. one production include containing the exact historical body;
2. ten existing local helper names retained as wrappers;
3. forty-one call sites unchanged;
4. one production-include native test script;
5. one rollback manifest restoring the ten accepted W1A bytes and removing the two new files.

The generator does not write into production paths in the repository and does not grant implementation or consumer-cutover authority.

## Remaining gate

The generated overlay must still compile natively with zero errors and zero warnings and pass the thirteen-vector production shared-engine runtime test. Only a later final cutover decision may authorize application.

## Evidence

- `tools/consolidation/uc04w1b/native_review.py`
- `tools/consolidation/uc04w1b/cutover_candidate.py`
- `registry/consolidation/uc04/w1b/evidence_review_policy.json`
- `registry/consolidation/uc04/w1b/conditional_cutover_policy.json`

## Navigation

- [[01_UNIFIED_CONSOLIDATION_AND_PLATFORM_SEAL/15_UC04_W1B_NATIVE_QUALIFICATION/00_MOC|W1B records MOC]]
