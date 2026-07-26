---
title: State-Space and Mamba Encoders
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v4
- governed-challenger
---

# Purpose

Evaluate structured and selective state-space models as efficient long-sequence challengers for market paths and context lifecycle streams.

## Capability tier

**Governed Challenger**

## System design

### State formulation

Inputs are causal event sequences with explicit time deltas, missingness, and context-state transitions.

### Baselines

S4-style, selective-state-space, convolutional, recurrent, and transformer baselines use identical folds and budgets.

### Streaming parity

The incremental streaming state must match batch inference within declared numerical tolerance.

### Failure containment

State reset, symbol switch, gap, session boundary, and restart behavior are explicit.

## Input contracts

- `CausalEventSequence`
- `StateResetPolicy`
- `EncoderConfig`

## Output contracts

- `StreamingState`
- `SequenceEmbedding`
- `ParityCertificate`

## Measurement framework

- Long-horizon uplift.
- Streaming/batch parity.
- State stability under gaps.
- Latency-memory frontier.

## Adversarial questions

- Does hidden state leak across opportunities or symbols?
- Is performance tied to one sequence length?
- Can restart reconstruct state exactly?

## Mandatory controls

1. Exact upstream hashes and data roles are recorded.
2. Candidate and failure ledgers are complete.
3. Costs, capacity, missingness, censoring, and support are explicit.
4. Validation uses chronological, cluster-aware, purged folds.
5. Advanced outputs cannot bypass manual policy, hard risk, portfolio, or UCEE promotion.
6. Any runtime handoff requires deterministic export, parity, latency, fallback, and revocation evidence.

## Acceptance boundary

Passing research metrics is necessary but never sufficient. The component remains non-authoritative until its evidence is admitted through UCEE I12, compiled by I14, challenged prospectively under I15, bounded by I17, and qualified under I18.

## Related notes

- [[Runtime_Export_And_Parity]]
