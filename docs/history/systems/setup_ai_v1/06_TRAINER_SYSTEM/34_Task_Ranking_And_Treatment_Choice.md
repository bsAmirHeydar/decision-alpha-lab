---
id: SAED-3134D5BCA3
title: "Task 4 — Candidate Ranking and Treatment Choice"
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
  - ranking
---

# Task 4 — Candidate Ranking and Treatment Choice

## Grouped Problem

Candidates are grouped by opportunity. The model ranks only compatible candidates, including Skip.

## Algorithms

- expected-utility regression;
- pairwise rankers;
- listwise ranking;
- treatment-choice classification;
- doubly robust/off-policy methods only with appropriate logged data.

## Metrics

Top-1 net utility, top-k coverage, regret versus fixed baseline, descriptive regret versus historical oracle, selected-policy stability, concentration, turnover and tail behavior.

## Safety

A small ranking margin, unstable winner or unsupported candidate produces abstention or fallback.
