---
type: strategy-factory-document
status: canonical
title: "Runbook — Debug Research, Paper, and Live Mismatch"
tags:
  - strategy-factory
---

# Runbook — Debug Research, Paper, and Live Mismatch

A mismatch is decomposed by artifact boundary rather than explained narratively.

## Triage order

Source bars and clocks → anatomy events → known times → feature snapshots → candidate policies → model artifact/version → risk gate → broker normalization → fills and costs → position management.

## Reproduction

Freeze the incident inputs and replay each layer with hashes. Identify the first divergent artifact. Do not patch downstream symptoms before the first divergence is understood.

## Resolution

Classify as data, canon, adapter, simulation, model, configuration, broker, or state error. Correct with a versioned patch, regression test, replay, and rollback plan.

