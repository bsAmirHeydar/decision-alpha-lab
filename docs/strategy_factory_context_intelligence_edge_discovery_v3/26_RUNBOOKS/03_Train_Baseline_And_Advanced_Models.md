---
title: Runbook — Train Baseline and Advanced Model Ladder
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v3
- runbook
- operations
---

# Purpose

Train a disciplined sequence from manual/naive baselines to advanced representation, causal, survival, foundation and policy challengers while preserving fair comparison and capability boundaries.

# Entry conditions

- Certified outcome cube and clustered fold manifest exist.
- Model ladder, feature families, compute budget and metrics are frozen.
- Training roles cannot access locked/prospective evidence.

# Roles and separation of duties

| Role | Responsibility |
|---|---|
| Model Engineer | Implements models and manifests. |
| Research Owner | Defines scientific comparison. |
| Leakage Sentinel | Audits features, preprocessing and access. |
| Compute Controller | Enforces budget and complete trial ledger. |
| Independent Validator | Challenges finalists, not training decisions. |

# Procedure

## Step 1 — Establish baselines

**Action**

Run Skip-All, Always-Trade, unconditional treatment, context-only, manual policy and regularized classical models.

**Mandatory output**

- Baseline report and prediction artifacts.

**Stop conditions**

- Advanced model starts before baselines are reproducible.

## Step 2 — Train calibrated predictive heads

**Action**

Fit eligibility, fill, survival, distribution, ranking and selection tasks with fold-local preprocessing.

**Mandatory output**

- Task-specific artifacts and calibration report.

**Stop conditions**

- Treatment siblings or temporal clusters cross roles.

## Step 3 — Train representation challengers

**Action**

Evaluate self-supervised, multi-view, state-space, graph or foundation adapters under frozen embeddings and clean folds.

**Mandatory output**

- Representation ablation report.

**Stop conditions**

- Pretraining corpus contains protected periods or hidden outcome labels.

## Step 4 — Train causal challengers

**Action**

Run doubly robust/orthogonal and heterogeneity learners only where identification assumptions are defensible.

**Mandatory output**

- Causal assumption and policy-value report.

**Stop conditions**

- Overlap, consistency or confounding diagnostics fail.

## Step 5 — Train world/offline-policy research models

**Action**

Use world models for stress and offline policy models only over finite approved actions with safe projection.

**Mandatory output**

- Research-only challenger report.

**Stop conditions**

- Synthetic or off-policy value is presented as real evidence.

## Step 6 — Calibrate uncertainty and abstention

**Action**

Fit calibration, ensemble/OOD and conformal/selective controls on designated roles.

**Mandatory output**

- Support and abstention policy.

**Stop conditions**

- Coverage assumptions or calibration transport fail.

## Step 7 — Select protected finalists

**Action**

Use inner/nested evidence, Pareto constraints and complete trial universe; export clean predictions.

**Mandatory output**

- Finalist manifest.

**Stop conditions**

- Selection references locked final or prospective outcomes.

## Step 8 — Reproduce finalists independently

**Action**

Rerun from manifests on clean environment/hardware and compare predictions/decisions.

**Mandatory output**

- Reproduction certificate.

**Stop conditions**

- Declared reproducibility tier is not met.

# Completion gates

- [ ] Simple baselines remain available as fallback.
- [ ] Advanced complexity shows paired protected uplift.
- [ ] All trials, failures and prunes retained.
- [ ] Causal/world/RL claims are labeled by evidence class.
- [ ] Finalists reproduce independently.

# Evidence retained

- `baseline_report`
- `trainer_manifests`
- `trial_ledger`
- `representation_ablation`
- `causal_report`
- `world_model_report`
- `offline_policy_report`
- `support_audit`
- `finalist_manifest`
- `reproduction_certificate`

# Failure and escalation matrix

| Condition | Required response |
|---|---|
| Leakage detected | Invalidate affected trials and descendants; rebuild roles/features. |
| Compute budget exhausted | Stop according to manifest; do not inspect locked evidence. |
| Advanced model only improves aggregate | Reject or constrain to supported subgroup after new preregistration. |
| Foundation checkpoint changes | Create new intake/version and rerun all comparisons. |

# Exit state

Models become `challenge_candidates`; none are promoted by this runbook.

# Related architecture

- [[00_Home]]
- [[End_To_End_Reference_Architecture]]
- [[Adversarial_Anti_Overfit_Red_Team]]
- [[Failure_Modes_Kill_Criteria_And_Recovery]]
