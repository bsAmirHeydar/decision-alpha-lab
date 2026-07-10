---
id: AIEOS2-E589B7384B7E
title: "Alpha Lab Python Research Standard"
type: standard
status: active
domain: engineering
version: 2.0.0
created: 2026-07-10
updated: 2026-07-10
tags:
  - ai-engineering
  - alpha-lab
  - engineering
---
# Alpha Lab Python Research Standard

## Purpose

Python owns reproducible data engineering, research, validation, model comparison, and reporting. Notebook convenience must not become hidden production logic.

## Required Practices

- Python 3.11+ unless a project lock states otherwise.
- Type hints on public functions and data contracts.
- `pathlib.Path` for paths.
- UTC internally; explicit conversion at boundaries.
- Deterministic seeds and stable row ordering.
- No import-time side effects for research modules.
- Configuration is explicit and serialized with each run.
- CLI entry points return meaningful exit codes.
- Missing/invalid data is reported; never silently imputed without a contract.
- Train-only fitting for encoders, scaling, thresholds, and feature selection.
- Tests cover parsers, temporal splits, leakage barriers, metrics, and reproducibility.

## Notebook Rule

Notebooks may explore and visualize. Reusable logic moves into importable modules. A result is not reproducible if it depends on cell execution order, hidden state, or uncommitted local data.

## Experiment Identity

Every run records:

```text
experiment/run ID
code version/commit
configuration hash
dataset/schema version
time range and availability cutoff
seed
fold plan
outputs and checksums
status and reviewer
```

## Model Boundary

Models produce evidence and predictions. Promotion to decision logic requires a separate versioned gate. Production execution must not import ad-hoc research notebooks.
