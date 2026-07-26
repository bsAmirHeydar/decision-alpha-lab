---
id: SAED-9586657B52
title: "Multiplicity, Nested Selection, and PBO"
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
  - anti-overfit
  - multiplicity
  - pbo
---

# Multiplicity, Nested Selection, and PBO

## Nested Selection

All model, feature, Treatment and threshold choices occur inside the inner process. Outer folds estimate the full procedure, not a preselected winner.

## Multiplicity

Use family definitions and correction appropriate to the selection problem. Count invalid/pruned/failed choices when they were part of the search opportunity.

## PBO / CSCV

Estimate how often in-sample winners underperform out of sample across combinations. Interpret with dependence and limited sample caveats.

## Decision

A candidate with attractive average return but high winner-selection instability remains challenge/reject.
