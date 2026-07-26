---
title: "Model Plugin Interface"
phase: 13
status: canonical
tags: [strategy-factory, training, leakage-safety, phase13]
---
# Model Plugin Interface

## Purpose

Defines exact family-version-task registration and rejects unregistered or ambiguous trainers.

## Contract

Phase 13 consumes only immutable, accepted Phase 12 fold and promotion-review evidence. Every artifact retains source run, validation-plan, feature-schema, label-contract, rowset and code-revision lineage. The phase never reconstructs anatomy, candidate geometry or outcome simulation, and it never grants paper or live authority.

## Required invariants

1. Feature values are ordered by an exact-versioned schema and were known no later than the decision timestamp.
2. Labels are derived only from terminal outcome evidence through a versioned label contract.
3. Cluster identity remains atomic inside each fold role.
4. Imputation and scaling parameters are fitted only on training rows.
5. Model fitting uses training rows; family selection and calibration use validation rows; published evaluation predictions use test rows only.
6. Missing, ambiguous, duplicate, non-finite or lineage-inconsistent evidence fails closed or remains explicitly excluded.
7. Every seed, search bound, optimizer setting, model family and metric is part of the training-plan identity.
8. Model artifacts and cards explicitly carry no capital authority.

## Evidence

The implementation emits machine-readable manifests, stable hashes, model parameters, calibration parameters, OOS prediction rows, metric summaries and rejection reasons. Re-running the same inputs must reproduce the same identities. Any material semantic change creates a new schema, contract, plan or artifact version instead of modifying historical evidence.

## Operational consequence

Phase 14 can review and register a candidate without private knowledge because the full dataset, transform, model, calibration, evaluation and limitation chain is explicit. A failure here blocks registry eligibility but never deletes the underlying research evidence.
