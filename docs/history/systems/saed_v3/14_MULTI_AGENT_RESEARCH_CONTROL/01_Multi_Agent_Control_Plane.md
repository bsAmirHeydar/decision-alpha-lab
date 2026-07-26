---
title: Multi-Agent Research Control Plane
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v3
- core-production
---

# Purpose

Use specialized AI agents to increase scientific throughput while enforcing deterministic workflows, least authority, and human promotion control.

## Capability tier

**Core Production**

## System design

### Orchestrator

Compiles approved research plans into tasks and monitors dependencies; cannot change hypotheses or data roles.

### Specialist agents

Hypothesis, data, treatment, model, causal, statistical, execution, reproducibility, and model-risk roles.

### Evidence protocol

Agents communicate through typed artifacts and claims with source references, not free-form hidden state.

### Human checkpoints

Research scope, protected-data access, major search expansion, waivers, and promotion require explicit approval.

## Input contracts

- `ResearchCharter`
- `AgentAuthorityMatrix`
- `TaskDAG`

## Output contracts

- `AgentRunLedger`
- `ClaimGraph`
- `ReviewRequests`

## Measurement framework

- Task completion quality.
- Unsupported claim rate.
- Rework.
- Authority violations.
- Human-review load.

## Adversarial questions

- Can agents collude through shared mutable memory?
- Does the orchestrator expand scope silently?
- Are agent summaries treated as evidence without source artifacts?

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

- [[Multi_Agent_Authority_Matrix]]
