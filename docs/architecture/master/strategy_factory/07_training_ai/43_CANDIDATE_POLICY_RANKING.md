---
type: strategy-factory-document
status: canonical
title: "Candidate Policy Ranking"
tags:
  - strategy-factory
---

# Candidate Policy Ranking

Ranking selects the best declared execution policy for an event rather than asking a model to invent one.

## Problem shape

Each event has candidates with shared context and policy descriptors. The ranker estimates expected net R or pairwise preference. `Skip` is included as a candidate with zero or hurdle utility.

## Avoid oracle leakage

Training labels may identify historical best candidate, but features cannot include any path result. Fold splits occur by event cluster so candidates from one event never appear on both sides.

## Metrics

Top-1 net R, top-k coverage, regret versus historical oracle, uplift over fixed policy, stability of selected policy distribution, and turnover in live decisions. An oracle is descriptive and never a deployable benchmark.

