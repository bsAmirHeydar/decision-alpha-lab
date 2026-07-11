---
title: "Expected Maximum Under Search"
phase: 12
status: canonical
tags: [strategy-factory, anti-overfit, validation, phase12]
---
# Expected Maximum Under Search

## Purpose

Estimates how large the best statistic can appear merely because many configurations were evaluated.

## Canonical position

Phase 12 consumes immutable Phase 10 trial discovery evidence and Phase 11 statistical samples. It does not reconstruct anatomy, candidate geometry, fills or costs. Source identifiers remain unchanged through every validation artifact.

## Required invariants

1. Evaluation ranges are half-open and chronologically ordered.
2. Purge and embargo gaps are explicit artifacts, not comments.
3. Every searched trial remains visible in the trial family.
4. Test evidence is unavailable to parameter selection.
5. Cluster identity is respected when assigning observations to roles.
6. Seeds, thresholds, registry hashes and code revision are manifest inputs.
7. Missing, ambiguous or invalid evidence cannot improve a score.
8. No Phase 12 component has paper or live execution authority.

## Failure behavior

Validation fails closed on missing lineage, hash mismatch, incomplete fold roles, non-finite metrics, duplicate identities, undeclared trials, fatal leakage findings or absent stress evidence. A rejected strategy remains fully reportable; rejection never deletes evidence.

## Evidence outputs

The subsystem emits canonical folds, fold observations, leakage findings, corrected hypothesis results, deflated performance, PBO, reality-check evidence, surface stability, stress results, gate rows, promotion decision, report manifest and artifact index.

## Operational rule

The artifact is versioned and deterministic. Any material change to ranges, thresholds, family membership, cost assumptions, seeds or algorithms creates a new plan or registry identity rather than mutating prior evidence.

## Acceptance evidence

- deterministic hash on repeated execution;
- explicit lineage to source run and trial ledger;
- no optimistic handling of missing or ambiguous data;
- machine-readable failure reason;
- no live-order token in phase-owned MQL5 modules.
