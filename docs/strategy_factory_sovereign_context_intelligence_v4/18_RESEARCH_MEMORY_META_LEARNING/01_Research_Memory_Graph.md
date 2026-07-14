---
title: Research Memory Graph
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v4
- core-production
---

# Purpose

Preserve the institution's complete scientific memory as a graph of questions, hypotheses, data, trials, failures, evidence, decisions, and live observations.

## Capability tier

**Core Production**

## System design

### Memory nodes

Context, hypothesis, feature, treatment, model, dataset, experiment, result, challenge, incident, promotion, and retirement.

### Relations

Supports, contradicts, duplicates, extends, invalidates, transports, depends-on, and failed-because.

### Negative evidence

Rejected and null findings are first-class and searchable.

### Retrieval

Agents receive bounded source-backed context with data-role controls and temporal validity.

## Input contracts

- `ArtifactGraph`
- `TrialLedger`
- `CommitteeDecisions`
- `Incidents`

## Output contracts

- `ResearchMemoryGraph`
- `RetrievalIndex`
- `KnowledgeCards`

## Measurement framework

- Duplicate-work reduction.
- Negative-evidence reuse.
- Retrieval precision.
- Decision traceability.

## Adversarial questions

- Does memory summarize away uncertainty?
- Can protected evidence leak through retrieval?
- Are failures retained after project ownership changes?

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

- [[Failure_Memory_And_Falsification_Library]]
