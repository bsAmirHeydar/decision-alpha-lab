---
title: AI Analyst and Diagnostic Packets
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v3
- governed-challenger
---

# Purpose

Generate source-backed explanations of performance, failure, drift, and candidate differences without granting narrative authority.

## Capability tier

**Governed Challenger**

## System design

### Packet contents

Opportunity attribution, context/regime breakdown, treatment effects, path clusters, costs, calibration, support, stress, failures, and unresolved questions.

### Evidence links

Every statement references an immutable metric, row set, plot specification, or report.

### Counter-narratives

Generate competing explanations and strongest skeptical interpretation.

### Access control

Protected and live details are summarized only within authorized roles.

## Input contracts

- `EvidenceBundle`
- `AttributionReport`
- `MemoryGraph`

## Output contracts

- `DiagnosticPacket`
- `ClaimGraph`
- `FollowUpQuestions`

## Measurement framework

- Unsupported claim rate.
- Diagnostic usefulness.
- Competing-explanation coverage.
- Reproduction links.

## Adversarial questions

- Does the analyst invent causal explanations?
- Can a persuasive narrative override weak evidence?
- Are selected examples representative?

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

- [[Multi_Agent_Control_Plane]]
