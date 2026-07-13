---
title: Promotion Dossier and Signed Admission
status: canonical
version: 2.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v2
- core-production
---

# Purpose

Compile all evidence and authority decisions into a closed, immutable admission that bounds what the policy may do.

## Capability tier

**Core Production**

## System design

### Dossier

Hypothesis, data, trials, baselines, calibration, causal claims, anti-overfit challenges, economics, runtime parity, operations, and incidents.

### Committee decision

Promote, challenge, restrict, reject, or retire with explicit rationale.

### Admission support

Exact context, markets, profiles, treatments, actions, risk tiers, versions, and validity horizon.

### Revocation

Triggers and rollback targets are part of admission.

## Input contracts

- `PromotionDossier`
- `ReviewSignatures`
- `RuntimeBundle`

## Output contracts

- `SignedAdmission`
- `RestrictionSet`
- `RevocationPlan`

## Measurement framework

- Dossier completeness.
- Open issues.
- Reviewer independence.
- Admission/reality consistency.

## Adversarial questions

- Does admission exceed tested support?
- Are unresolved critical incidents waived?
- Can runtime load a newer model under old admission?

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

- [[Manual_AI_Hybrid_Policy_Compilation]]
