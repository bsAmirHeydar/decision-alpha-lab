---
title: "Filesystem Boundary"
phase: 14
status: canonical
tags: [strategy-factory, model-governance, registry, phase14]
---
# Filesystem Boundary

## Purpose

Keeps file hashing and JSON reporting outside the MQL5 decision fast path.

## Contract

Phase 14 consumes immutable Phase 12 validation evidence and immutable Phase 13 training artifacts. It does not retrain a model, reconstruct outcomes, load ONNX, rank live candidates, size positions or submit orders. Registry state changes are append-only governance decisions, and every promotable artifact remains explicitly no-execution-authority.

## Required invariants

1. One exact model version may be registered only once in a registry scope.
2. A promotable state requires an eligible, versioned promotion evaluation.
3. Every decision is sequence-checked and chained to the previous decision hash.
4. A registry scope may contain at most one champion.
5. Supersession, suspension, retirement, rejection and rollback preserve historical entries.
6. Release manifests pin the exact registry snapshot and artifact inventory.
7. Integrity hashes never masquerade as signer authenticity.
8. All Phase 14 outputs remain without execution or capital authority.

## Evidence

The implementation emits exact-version JSON contracts, deterministic FNV-1a identities, SHA-256 artifact inventories, immutable gate results, a hash-chained decision ledger, registry snapshots, model release manifests, rollback plans and machine-readable rejection reasons. A semantic change creates a new policy, scope, artifact, entry revision, decision or release identity; historical evidence is never edited in place.

## Operational consequence

A failure blocks promotion or release eligibility while preserving the model and all research evidence for diagnosis. Phase 15 may consume only a release whose registry entry is present in the referenced snapshot, whose artifact inventory reproduces, whose feature ordering is exact and whose authority flag remains false.
