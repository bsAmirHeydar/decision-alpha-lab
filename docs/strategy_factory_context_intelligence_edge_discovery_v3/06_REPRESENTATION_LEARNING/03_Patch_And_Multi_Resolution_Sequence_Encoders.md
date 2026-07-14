---
title: Patch and Multi-Resolution Sequence Encoders
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v3
- governed-challenger
---

# Purpose

Use patch-based sequence modelling to capture local motifs and long horizons while preserving causal alignment and runtime budgets.

## Capability tier

**Governed Challenger**

## System design

### Patch design

Patch length, stride, channel policy, overlap, and normalization are frozen inside nested training.

### Resolution hierarchy

Local trigger windows, context windows, higher-timeframe summaries, and intermarket sequences have separate receptive fields.

### Causal masking

Decision-time encoders cannot attend to future events or finalized higher-timeframe bars unavailable at known time.

### Challenger evidence

Patch models must beat regularized sequence summaries and state-space baselines on stable incremental utility.

## Input contracts

- `SequenceWindowManifest`
- `PatchPolicy`
- `KnownTimeMask`

## Output contracts

- `SequenceEmbedding`
- `AttentionAudit`
- `ExportProfile`

## Measurement framework

- Horizon-specific uplift.
- Sensitivity to patch/stride neighborhoods.
- Attention shortcut probes.
- Runtime latency.

## Adversarial questions

- Are patches aligned to event boundaries using future information?
- Does longer context improve only the selected sample?
- Can the model be exported deterministically?

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
