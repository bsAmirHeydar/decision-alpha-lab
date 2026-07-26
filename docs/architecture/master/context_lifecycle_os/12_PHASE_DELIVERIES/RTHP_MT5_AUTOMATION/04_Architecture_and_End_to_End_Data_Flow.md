---
title: RTHP MT5 Automation — Architecture and End-to-End Data Flow
status: roadmap-approved-for-implementation
version: 1.0.0
updated: 2026-07-22
tags: [rthp, mt5, architecture, data-flow]
---

# Architecture and End-to-End Data Flow

## Layer diagram

```text
Operator Symbol Selection
        ↓
RTHP MT5 Activation CLI
        ↓
Read-Only MT5 Terminal Adapter
        ↓
Symbol Resolver + Metadata Freeze
        ↓
Closed M1 Bar Acquisition
        ↓
Source Quality and Coverage Gates
        ↓
Immutable M1 Landing Artifacts
        ↓
RTHP M1 Materialization Adapter
        ↓
Existing RTHP ContextPackage / AI Input
        ↓
Existing Train Activation
        ↓
Existing Dataset / Label / Split / Trainer / Validation Engines
        ↓
Immutable Run Evidence and Verification
```

## Ownership

| Layer | Owner | May change shared engine? |
|---|---|---:|
| MT5 terminal adapter | RTHP integration | No |
| Symbol resolver | RTHP integration | No |
| M1 quality validator | RTHP integration | No |
| M1 materialization adapter | RTHP integration | No |
| ContextPackage | Existing RTHP package | No |
| Dataset/trainer/validation | Existing shared engines | Not by this delivery |

## Key design choice

The adapter produces immutable M1 artifacts and delegates downstream computation. It does not embed a parallel dataset engine, model trainer, validator, or research planner.
