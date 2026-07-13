---
title: Sequence State Models
status: canonical
version: 2.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v2
- governed-challenger
---

# Purpose

Model evolving context and market state as a causal sequence while retaining interpretable state summaries and restart parity.

## Capability tier

**Governed Challenger**

## System design

### State inputs

Event-time deltas, context lifecycle transitions, path features, intermarket updates, and execution state.

### Architectures

Temporal convolution, recurrent, transformer, state-space, and hybrid state models are benchmarked under the same budget.

### State probes

Decoded regime, context phase, expected path, and missingness ensure the hidden state is scientifically inspectable.

### Operational boundary

Only deterministic exportable models may leave research.

## Input contracts

- `CausalSequence`
- `StateResetPolicy`
- `ContextLifecycle`

## Output contracts

- `SequenceState`
- `ProbeReport`
- `StreamingParity`

## Measurement framework

- Sequence uplift.
- State probe fidelity.
- Batch/stream parity.
- Restart reconstruction.

## Adversarial questions

- Does the state persist information across independent opportunities?
- Does the sequence window use future-aligned normalization?
- Can hidden state drift silently?

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

- [[State_Space_And_Mamba_Encoders]]
