---
title: Runbook — World Model and Synthetic Stress Laboratory
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v4
- runbook
- operations
---

# Purpose

Use learned dynamics and generative path models to create adversarial stress, missing-regime probes and counterfactual scenarios without presenting synthetic performance as empirical edge evidence.

# Entry conditions

- Real replay/outcome engine is certified.
- World model scope and research-only tier are signed.
- Training and challenge data roles are separated.

# Roles and separation of duties

| Role | Responsibility |
|---|---|
| World Model Researcher | Builds dynamics/generative models. |
| Replay Engineer | Defines real-path truth interface. |
| Statistical Adversary | Tests realism and exploitability. |
| Model Risk | Prevents synthetic evidence substitution. |

# Procedure

## Step 1 — Define state/action/observation semantics

**Action**

Bind context, market path, treatment action, costs and exogenous variables.

**Mandatory output**

- World-model program manifest.

**Stop conditions**

- State includes future or hidden outcome information unavailable at decision time.

## Step 2 — Train dynamics/generative model

**Action**

Fit on training roles with uncertainty and ensemble diversity.

**Mandatory output**

- World-model artifacts.

**Stop conditions**

- Training instability, mode collapse or role contamination.

## Step 3 — Validate one-step and rollout behavior

**Action**

Test calibration, distribution, dependence, tail, event timing and horizon degradation.

**Mandatory output**

- Rollout validity report.

**Stop conditions**

- Model fails essential invariants or tails.

## Step 4 — Run exploitability tests

**Action**

Optimize policies against simulator and check whether gains transfer to held-out real replay.

**Mandatory output**

- Simulator exploitation report.

**Stop conditions**

- Policy exploits model artifacts or impossible states.

## Step 5 — Generate adversarial scenarios

**Action**

Create volatility, gap, liquidity, correlation, path/chop and regime-transition stresses.

**Mandatory output**

- Synthetic stress library.

**Stop conditions**

- Scenarios violate market/account invariants without explicit labeling.

## Step 6 — Challenge real candidates

**Action**

Measure decision stability, trail behavior, risk, capacity and kill activation under scenarios.

**Mandatory output**

- Stress challenge report.

**Stop conditions**

- Candidate fails declared safety/economic bounds.

## Step 7 — Archive with evidence labels

**Action**

Store synthetic origin, model version, uncertainty and permitted uses.

**Mandatory output**

- World-model evidence package.

**Stop conditions**

- Synthetic result is blended into real OOS metrics.

# Completion gates

- [ ] Synthetic evidence remains distinct.
- [ ] Rollout limitations and horizon are explicit.
- [ ] Exploitability challenge passes.
- [ ] Market/broker invariants enforced.
- [ ] Stress failures affect risk/promotion even though synthetic gains do not prove edge.

# Evidence retained

- `world_model_program`
- `world_model_artifact`
- `rollout_validity_report`
- `exploitation_report`
- `synthetic_stress_library`
- `stress_challenge_report`

# Failure and escalation matrix

| Condition | Required response |
|---|---|
| Simulator exploitation | Quarantine affected policy; improve model/stress; never count gain. |
| Tail mismatch | Limit horizon/use or reject model. |
| Impossible scenario | Label or remove; update invariants. |
| Synthetic contamination of OOS report | Invalidate report and rebuild evidence. |

# Exit state

World model remains a research/stress component; it never receives standalone promotion.

# Related architecture

- [[00_Home]]
- [[End_To_End_Reference_Architecture]]
- [[Adversarial_Anti_Overfit_Red_Team]]
- [[Failure_Modes_Kill_Criteria_And_Recovery]]
