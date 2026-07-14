---
title: Run the Institutional Red Team
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: canonical
tags:
  - saed-v3
  - runbook
  - operations
---

# Mission

Independently attempt to falsify the candidate across leakage, nulls, multiplicity, tails, execution, transport, complexity, and operations.

## Entry conditions

- Frozen candidate and full dossier.
- Attack library.
- Independent budget.

## Mandatory roles and separation of duties

- Red-team lead.
- Leakage sentinel.
- Statistical adversary.
- Execution auditor.
- Security reviewer.

## Procedure

1. Reconstruct candidate.
2. Run suffix, role, cluster, and preprocessing attacks.
3. Run null/placebo and best-component removals.
4. Stress costs, delays, fills, tails, regimes, feeds, brokers, and dependence.
5. Challenge parameter surfaces and complexity.
6. Issue severity findings and retest remediation.

## Mandatory outputs

- Red-team report.
- Finding ledger.
- Retest evidence.
- Block/advance recommendation.

## Stop and escalation conditions

- Critical leakage.
- Failed placebo.
- Tail/capacity violation.
- Unresolved reproducibility or security issue.

## Evidence retained

- All attacks, seeds, results, and signatures.

## Completion gate

The runbook is complete only when all required artifacts are content-addressed, all exposures and deviations are recorded, an independent reviewer signs the completion state, and the downstream UCEE gate accepts the exact immutable bundle rather than a narrative summary.

## Related notes

- [[Institutional_Red_Team_And_Falsification_Factory]]
- [[Statistical_Adversary_Review_Board]]
