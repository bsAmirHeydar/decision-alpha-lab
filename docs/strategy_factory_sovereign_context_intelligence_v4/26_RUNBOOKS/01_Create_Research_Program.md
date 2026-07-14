---
title: Runbook — Create an Institutional Research Program
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

Turn a business or trading intuition into a bounded, falsifiable, budgeted and authority-safe research program compatible with UCEE and SAED V4.

# Entry conditions

- Approved context package or explicit context-onboarding dependency exists.
- Research owner and independent validator are assigned.
- No protected outcome has been opened for the proposed program.

# Roles and separation of duties

| Role | Responsibility |
|---|---|
| Research Sponsor | Defines economic objective and budget; cannot validate own claims. |
| Program Owner | Authors hypothesis, treatment scope and manifest. |
| Context Owner | Confirms upstream doctrine/version without optimizing it. |
| Independent Validator | Approves identification, folds and challenge plan. |
| Model Risk | Assigns capability tier and evidence requirements. |

# Procedure

## Step 1 — Write the falsifiable thesis

**Action**

Define the context occurrence, proposed economic mechanism, expected affected payoff profiles, supported entry mechanisms, null hypothesis and explicit disconfirmation conditions.

**Mandatory output**

- Signed `edge_hypothesis` with causal/predictive distinction.

**Stop conditions**

- Thesis depends on future information, undefined context semantics or unbounded actions.

## Step 2 — Bind upstream truth

**Action**

Resolve exact context, view, lifecycle, feature and known-time hashes from UCEE.

**Mandatory output**

- `context_binding_manifest`.

**Stop conditions**

- Any upstream artifact is mutable, unresolved or unsupported.

## Step 3 — Freeze finite action space

**Action**

Select payoff profiles, entries, stops, exits, trail/management and Skip/Abstain; compile compatibility graph.

**Mandatory output**

- `treatment_universe_manifest`.

**Stop conditions**

- Candidate count is unbounded or incompatible combinations remain.

## Step 4 — Define evidence roles

**Action**

Specify exploration, train, calibration, selection, locked final, prospective, shadow and live partitions plus access rules.

**Mandatory output**

- `evidence_role_plan`.

**Stop conditions**

- Historical availability cannot support clean roles or cluster-safe folds.

## Step 5 — Define objectives and constraints

**Action**

Choose profile-specific losses, utility, calibration, tail, capacity, complexity and compute constraints.

**Mandatory output**

- `objective_constraint_manifest`.

**Stop conditions**

- One metric can dominate while violating tail, capacity or stability requirements.

## Step 6 — Register budget and search universe

**Action**

Freeze model ladder, feature families, HPO bounds, compute budget, stopping and multiplicity scope.

**Mandatory output**

- `research_program_manifest`.

**Stop conditions**

- Locked evidence has already influenced search-space design without exposure accounting.

## Step 7 — Pre-register challenge plan

**Action**

Independent validator specifies nulls, leakage tests, destructive stresses, transport and kill criteria.

**Mandatory output**

- `red_team_challenge_plan`.

**Stop conditions**

- Program owner can edit challenges after protected results.

## Step 8 — Authorize execution

**Action**

Model Risk confirms capability tier, tool access, agent permissions and downstream gates.

**Mandatory output**

- Signed program admission.

**Stop conditions**

- Missing owner, budget, challenge plan, lineage or authority separation.

# Completion gates

- [ ] Thesis is falsifiable and economically explicit.
- [ ] Finite treatment universe includes Skip/Abstain.
- [ ] Evidence roles and cluster-safe folds are predeclared.
- [ ] Search and exposure universes are countable.
- [ ] Independent challenge and kill criteria are signed.

# Evidence retained

- `research_program_manifest`
- `edge_hypothesis`
- `context_binding_manifest`
- `treatment_universe_manifest`
- `objective_constraint_manifest`
- `red_team_challenge_plan`
- `program_admission`

# Failure and escalation matrix

| Condition | Required response |
|---|---|
| Protected evidence was viewed before registration | Record exposure; version program; reduce or replace final evidence. |
| Context semantics require change | Stop; route to context governance; never patch inside setup research. |
| Treatment universe expands after results | Create a new program version and count prior exposure/trials. |
| Owner conflict | Reassign validator or release authority before execution. |

# Exit state

Program state becomes `admitted_for_exploration`, never `promoted`.

# Related architecture

- [[00_Home]]
- [[End_To_End_Reference_Architecture]]
- [[Adversarial_Anti_Overfit_Red_Team]]
- [[Failure_Modes_Kill_Criteria_And_Recovery]]
