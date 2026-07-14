---
title: Adversarial Anti-Overfit Red Team and Falsification Program
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v3
- deep-design
- core-production
---

# Objective

Institutionalize an independent adversarial process whose objective is to disprove apparent edge, expose leakage, quantify selection bias and identify brittle dependencies before promotion.

## Capability tier

**Core Production**

# Non-negotiable principles

- The red team is rewarded for valid falsification, not for helping a candidate pass.
- Challenge artifacts are immutable and cannot be silently waived by model authors.
- Every positive claim must be linked to at least one explicit null and one destructive stress.
- Red-team access to locked evidence is controlled and any exposure is recorded.
- Failure is a reusable research asset stored in the institutional memory graph.

# Reference architecture

- Independent statistical adversary receives a frozen promotion dossier and produces a challenge plan.
- Leakage sentinel reconstructs known-time, folds, preprocessing and feature lineage from raw events.
- Execution adversary perturbs spread, slippage, delay, fills, broker rules and path ordering.
- Selection-bias auditor reconstructs the full trial/exposure universe and applies multiplicity diagnostics.
- Regime and transport adversary runs cross-symbol, cross-feed, cross-period and context-drop challenges.
- Kill committee adjudicates critical findings independently from the research program owner.

# Algorithms and decision logic

- Run purged nested walk-forward reconstruction from source events, not cached model-ready matrices.
- Apply random labels, timestamp shifts, direction flips, treatment shuffles, synthetic features and matched null contexts.
- Remove best trades, best clusters, best months, best symbols and top-tail observations under a predeclared ladder.
- Estimate PBO/CSCV, deflated performance, reality-check/SPA style statistics and bootstrap confidence under clustering.
- Probe parameter surfaces, feature subsets, treatment neighborhoods and cost multipliers for brittleness.
- Perform counterfactual leakage tests by perturbing future suffixes while asserting decision-time invariance.
- Require model authors to predict challenge outcomes before results are revealed.

# Canonical contracts

| Contract | Minimum semantics |
|---|---|
| `red_team_charter` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `challenge_plan` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `leakage_audit` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `multiplicity_reconstruction` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `destructive_stress_report` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `critical_finding` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |
| `challenge_verdict` | Versioned, closed, hash-bound artifact; owner and lifecycle required. |

Every contract includes schema version, deterministic identity, upstream hashes, evidence class, known-time declaration where relevant, owner, compatibility range and explicit failure semantics.

# Data, role and lineage controls

1. Raw, canonical, feature, outcome, training, calibration, selection-validation, locked-final, prospective, shadow and live roles are distinct.
2. Human, model, agent, dashboard and report access to protected evidence is recorded in the exposure ledger.
3. Revisions create a new artifact and never rewrite decision-time evidence.
4. Cross-fold preprocessing, tokenization, graph construction, feature selection and model selection are prohibited.
5. Trial, candidate, failure, retry, prune, timeout and waiver records remain immutable.

# Measurement system

- Fraction of claims surviving independent reconstruction.
- Performance after best-component removals and transport stress.
- Multiplicity-adjusted evidence strength.
- Number and severity of unresolved findings.
- Decision invariance under future-suffix and timestamp mutation.
- Time from finding to quarantine or remediation.

Metrics are segmented by time, symbol, context, regime, payoff profile, entry mechanism, broker/economics profile, support bucket and evidence class. Aggregates may not hide unstable subgroups.

# Adversarial failure table

| Class | Failure mechanism |
|---|---|
| Failure | Red team shares incentives or code paths with model authors. |
| Failure | Challenges are selected after seeing which ones are easy to pass. |
| Failure | Waivers erase critical findings without expiry. |
| Failure | Nulls are poorly matched and create false comfort. |
| Failure | Aggregate results hide subgroup collapse. |

# Authority boundary

- Research components propose and estimate; they cannot sign promotion.
- AI agents cannot alter context truth, data roles, protected evidence, risk limits, runtime generations or live authorizations.
- Policies remain bounded by UCEE I12 admission, I13 authority/fallback, I14 compilation, I17 risk/portfolio and I18 release qualification.
- Unsupported, stale, incomplete, OOD, mismatched or corrupt paths resolve to Manual, Skip, Abstain, Reject or Quarantine.

# Acceptance checklist

- [ ] Independent ownership and authority are documented.
- [ ] Challenge plan is frozen before protected evidence access.
- [ ] Critical findings block promotion automatically.
- [ ] All waivers are signed, scoped, expiring and visible.
- [ ] Failure artifacts enter research memory with reusable signatures.

# Required evidence packet

- Specification and assumption cards.
- Code, environment, data and artifact hashes.
- Positive, negative, boundary, mutation and adversarial tests.
- Baseline, ablation, stress, transport and reproducibility reports.
- Open limitations, kill criteria, downstream handoff and rollback path.

# Related architecture

- [[00_Home]]
- [[UCEE_I01_I18_Compatibility]]
- [[Anti_Overfit_Master_Protocol]]
- [[Promotion_Dossier_And_Signed_Admission]]
- [[Release_And_Production_Qualification]]
