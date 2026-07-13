---
id: ALMA-7052E314E2
title: "Assumption-Aware Monitoring"
type: architecture
status: canonical
domain: alpha-lab-master-architecture
version: 1.0.0
created: 2026-07-13
updated: 2026-07-13
tags:
  - alpha-lab
  - master-architecture
---
# Assumption-Aware Monitoring

## 1. Monitoring Thesis

A live strategy is supported by assumptions, not only a historical equity curve. Monitoring therefore asks:

> Are the market, model, execution and portfolio assumptions that justified this edge still alive?

## 2. Promotion-Time Monitoring Contract

Each production candidate publishes expected ranges for:

- context frequency and distribution;
- features and regime mix;
- spread, slippage, latency and fill probability;
- holding time, MFE and MAE;
- win rate, expectancy and calibration intervals;
- drawdown and loss clustering;
- trade coverage and abstention;
- portfolio dependence and capacity;
- runtime health.

## 3. Drift Taxonomy

### Data Drift

Feed, timestamp, missingness, mapping or specification changes.

### Market Drift

Context frequency or market-state distribution changes.

### Model Drift

Calibration, ranking, uncertainty or feature relevance deteriorates.

### Execution Drift

Costs, latency, fills or broker behavior diverge from assumptions.

### Portfolio Drift

Correlation, concentration, capacity or joint drawdown changes.

### Edge Decay

The context-treatment-outcome relationship weakens or reverses.

## 4. Health Lifecycle

```text
Healthy
→ Watch
→ Reduced
→ Quarantined
→ Retired
```

A short period of improved P&L does not automatically reactivate a quarantined policy. Recovery requires governed revalidation.

## 5. Champion–Challenger

New generations run offline, shadow and micro-live before replacing a champion. Comparison includes decision agreement, treatment selection, calibration, latency, execution feasibility and portfolio effect, not only P&L.

## 6. Retraining Governance

The prohibited loop is:

```text
Performance down → auto-retrain → silent live replacement
```

The correct loop is:

```text
Drift alert
→ reduce/quarantine
→ diagnostic packet
→ new experiment
→ protected validation
→ challenger generation
→ shadow comparison
→ explicit promotion
```

## 7. Closed-Loop Learning

Live fills improve cost models. Failed assumptions create new tests. Drift and retirement update Research Memory. But live outcomes do not automatically rewrite doctrine or production models.
