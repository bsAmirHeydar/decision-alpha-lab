---
id: SAED-F10B189BFD
title: "Targets, Label Maturity, and Censoring"
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
  - dataset
  - labels
---

# Targets, Label Maturity, and Censoring

## Task Targets

- eligibility/trade-skip;
- target-before-stop;
- net R and utility;
- MFE/MAE quantiles;
- time to fill/stop/target/expiry;
- competing risks;
- candidate ranking;
- treatment choice;
- path/trail capture;
- regime/novelty.

## Maturity

A label is usable only after the Treatment's outcome horizon closes. Rows with unresolved positions or unexpired orders are censored, not force-labeled.

## Censoring

Survival/competing-risk models receive event indicator, event type and censor time. Ordinary regression/classification must not silently treat censored rows as losses or zeros.
