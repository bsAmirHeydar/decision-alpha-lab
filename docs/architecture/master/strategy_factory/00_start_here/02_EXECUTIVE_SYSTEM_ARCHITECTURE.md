---
type: strategy-factory-document
status: canonical
title: "Executive System Architecture"
tags:
  - strategy-factory
---

# Executive System Architecture

This document defines the major services, ownership boundaries, and the irreversible separation between anatomy truth, research evidence, model decisions, and broker execution.

## Four planes

1. **Anatomy plane** — identifies what happened in the market and when it became knowable.
2. **Research plane** — generates candidates, simulates outcomes, measures uncertainty, and tests hypotheses.
3. **Decision plane** — applies frozen rules or versioned models to current snapshots.
4. **Execution plane** — validates risk, translates intents into broker requests, reconciles fills, and monitors positions.

No plane may silently acquire another plane's authority. A renderer cannot create events. A model cannot mutate anatomy. A broker fill cannot retroactively change a research label.

## Shared services

The shared platform owns contracts, identity, manifest validation, cost models, candidate compatibility, outcome path accounting, fold plans, multiple-testing registry, model registry, paper broker, hard risk limits, observability, incident response, and promotion state. Strategy plugins are consumers of these services.

## Artifact chain

Every stage materializes a versioned artifact: `events.parquet`, `snapshots.parquet`, `candidates.parquet`, `outcomes.parquet`, `model_dataset.parquet`, `folds.parquet`, `predictions.parquet`, `statistics.json`, `anti_overfit.json`, `model_card.md`, and `promotion_decision.json`. A result that cannot be reconstructed from these artifacts is exploratory, not official.

## Reference deployment

MQL5 owns deterministic live detection and broker interaction. Python owns large-scale simulation, statistics, training, and artifact generation. An offline model artifact or compact decision table may be exported to MQL5 inference, but training never occurs inside the live Expert Advisor. LLMs design, inspect, and report; they do not sit in the order path.

