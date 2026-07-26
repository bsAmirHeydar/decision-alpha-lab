---
title: Model Risk Committee
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v3
- core-production
---

# Purpose

Establish independent review for scientific validity, operational safety, security, and authority before promotion.

## Capability tier

**Core Production**

## System design

### Committee composition

Research sponsor, independent statistician, causal reviewer, execution reviewer, model-risk owner, operations owner, and security where applicable.

### Decision scope

Approve challenge plan, restrictions, waivers, promotion, extension, quarantine, retirement, and revocation.

### Evidence standard

Claims link to immutable artifacts; presentations are not evidence.

### Conflict control

Producers cannot constitute a majority or solely approve their own candidate.

## Input contracts

- `PromotionDossier`
- `AdversarialReports`
- `RiskScorecard`

## Output contracts

- `CommitteeDecision`
- `SignedAdmission`
- `OpenConditions`

## Measurement framework

- Issue closure.
- Reviewer independence.
- Decision latency.
- Post-promotion incident correlation.

## Adversarial questions

- Are reviewers evaluating code and evidence or only summaries?
- Can commercial urgency override critical controls?
- Are dissenting opinions preserved?

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

- [[Promotion_Dossier_And_Signed_Admission]]
