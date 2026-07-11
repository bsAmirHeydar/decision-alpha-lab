---
title: "Low-Latency Implementation Plan"
tags:
  - strategy-factory
  - implementation-roadmap
  - alpha-lab
status: canonical
doc_version: 1.0.0
---

# Low-Latency Implementation Plan

## Fast-Path Objective

Convert an already-confirmed anatomy event and current causal context into a deterministic decision with bounded latency.

## Startup Work

- parse and validate manifests;
- resolve exact plugin versions;
- compile feature DAG;
- load model artifacts;
- compile fixed vectors;
- resolve candidate templates;
- allocate caches and telemetry buffers;
- warm critical data;
- verify hashes and self-tests.

## Runtime Restrictions

The fast path must avoid:

- filesystem reads;
- network calls;
- dynamic import;
- JSON parsing;
- DataFrame creation;
- unbounded candidate enumeration;
- training or recalibration;
- report generation;
- blocking logs.

## Latency Stages

1. context freshness gate;
2. dirty-feature recomputation;
3. fixed vector assembly;
4. candidate materialization;
5. local inference;
6. utility ranking;
7. abstention gate;
8. pre-risk checks;
9. decision emission.

## Initial Service-Level Objectives

- Python reference runtime: P99 under 10 ms for standard strategies.
- MQL5 local runtime: P99 under 2 ms excluding broker round trip.
- Zero dynamic allocations in the steady-state MQL5 decision loop where practical.
- Fail closed on latency budget breach for time-sensitive strategies.
