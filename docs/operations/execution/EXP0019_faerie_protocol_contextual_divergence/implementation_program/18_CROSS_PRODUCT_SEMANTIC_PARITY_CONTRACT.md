---
title: "Cross-Product Semantic Parity Contract"
tags: [exp0019, faerie-protocol, implementation-program, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
implementation_program: FP-IMP-001
program_version: 1.0.0
doc_version: 1.0.0
last_updated: 2026-07-13
language: en
---
# Cross-Product Semantic Parity Contract

## Principle

Indicator, diagnostic EA, paper EA, and live EA are different authority surfaces over one semantic engine. For the same M1 data, context configuration, confirmation timeframe, and data revision, they must produce the same semantic events and signal IDs.

## Compared artifacts

| Artifact | Exact comparison |
|---|---|
| window IDs and OHLC extrema | exact |
| reference IDs/levels/state | exact within symbol tick normalization |
| Hunt event IDs/time/side | exact |
| Candidate IDs/roles/direction | exact |
| confirmation/invalid/neutral state | exact |
| WW stack and active resolver | exact |
| signal ledger sequence | exact |
| pair-session winner/suppression reason | exact |
| chart objects | not compared semantically; projection inventory is product-specific |
| order events | only execution products |

## Differential procedure

1. Freeze the same input manifest and M1 fixture.
2. Run full replay through the indicator engine harness.
3. Run full replay through diagnostic EA.
4. Canonicalize and hash semantic event streams.
5. Compare counts, IDs, ordering, fields, and terminal states.
6. Repeat incremental/live-like feeding.
7. Repeat after restart/checkpoint restore.

## Divergence classification

- `DATA_SOURCE_DIVERGENCE`
- `CONFIGURATION_DIVERGENCE`
- `TIME_OWNERSHIP_DIVERGENCE`
- `EVENT_ORDER_DIVERGENCE`
- `STATE_TRANSITION_DIVERGENCE`
- `IDENTITY_DIVERGENCE`
- `NUMERIC_NORMALIZATION_DIVERGENCE`
- `UNEXPLAINED_DIVERGENCE`

Any unexplained divergence blocks Paper and Live phases.
