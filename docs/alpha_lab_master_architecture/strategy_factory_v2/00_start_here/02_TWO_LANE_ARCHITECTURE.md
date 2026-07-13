---
title: "Two-Lane Architecture — Deep Research and Compiled Decision"
domain: strategy-factory-v2
status: canonical
language: en
version: 2.0.0
tags:
  - alpha-lab
  - strategy-factory
  - anatomy-to-decision
---

# Why two lanes exist

The work required to discover a setup is different from the work permitted while deciding whether to trade it.

## Deep research lane

The research lane is allowed to be exhaustive and computationally expensive. It may:

- materialize large event and candidate tables;
- generate broad entry/stop/exit combinations;
- run coarse-to-fine searches;
- compare many labels and horizons;
- calculate grouped statistics and confidence intervals;
- perform purged walk-forward and combinatorial CV;
- run permutation, placebo, bootstrap, PBO, DSR, FDR, and reality-check tests;
- train multiple model families;
- create charts, reports, and forensic failure analyses.

It writes immutable artifacts and never sends orders.

## Compiled decision lane

The decision lane receives a promoted plan. It may only:

1. accept a valid AnatomyEvent;
2. update the required context graph;
3. build a bounded candidate set from compiled templates;
4. encode fixed feature vectors;
5. run approved local model routes;
6. calibrate, rank, and abstain;
7. emit a DecisionEnvelope;
8. request independent risk authorization;
9. produce an ExecutionIntent.

It does not perform model selection, hyperparameter search, dataframe joins, report generation, or trial discovery.

## Parity contract

Research and live must share:

- event semantics;
- feature definitions and known times;
- candidate policy code or verified equivalent implementations;
- cost model versions;
- model artifact hashes;
- threshold versions;
- reason-code vocabulary;
- execution intent schema.

The research lane may use a vectorized implementation and the live lane a compiled MQL5 implementation, but differential replay tests must prove equivalent outputs within declared tolerances.
