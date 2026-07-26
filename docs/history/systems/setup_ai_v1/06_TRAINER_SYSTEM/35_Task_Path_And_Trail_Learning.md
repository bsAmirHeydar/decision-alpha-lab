---
id: SAED-21CBA87678
title: "Task 5 — Path Shape and Trail Suitability"
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
  - trainer
  - path-model
---

# Task 5 — Path Shape and Trail Suitability

## Purpose

Estimate whether a move is smooth, choppy, persistent or prone to deep pullbacks, and evaluate declared trail policies.

## Features

Only pre-decision sequence or state summaries are permitted. Post-entry paths are labels.

## Targets

- future path smoothness;
- pullback-depth quantiles;
- trend persistence;
- trail capture/giveback;
- premature exit;
- optimal policy among a finite trail registry.

## Boundary

The model selects among certified trail policies; it does not synthesize arbitrary live trail updates.
