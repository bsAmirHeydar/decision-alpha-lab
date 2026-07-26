---
id: SAED-0A461D7CAA
title: "Search Budgets and Complete Trial Ledger"
type: architecture
status: canonical
domain: strategy-factory-setup-ai-edge-discovery
version: 1.0.0
created: 2026-07-13
updated: 2026-07-13
tags:
  - strategy-factory
  - setup-factory
  - ai-training
  - experiment
  - budget
  - ledger
---

# Search Budgets and Complete Trial Ledger

## Budget Dimensions

Number of candidates, model families, hyperparameter trials, folds, seeds, feature ablations, treatment ablations, nulls, stresses, compute time, memory and human review iterations.

## Ledger States

Attempted, admitted, invalid, duplicate, pruned, scheduled, running, succeeded, failed, timed-out, cancelled, selected, ensembled and manually overridden.

## Multiplicity

All choices that could influence the reported winner are counted, including prompt-driven feature changes and analyst-guided reruns.

## Stopping

Stopping rules are declared before protected evaluation. “Continue until something works” is forbidden.
