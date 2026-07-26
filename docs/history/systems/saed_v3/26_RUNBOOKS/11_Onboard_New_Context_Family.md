---
title: Runbook — Onboard a New Context Family into SAED V3
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

Connect a new UCEE context family to the setup/AI research system without modifying central engine semantics or bypassing context governance.

# Entry conditions

- Context doctrine and lifecycle specification are approved or ready for I16 onboarding.
- Legacy source/adapter scope is identified where applicable.
- No setup labels are embedded in context truth.

# Roles and separation of duties

| Role | Responsibility |
|---|---|
| Context Owner | Owns semantics and known-time. |
| Onboarding Engineer | Generates context package/adapters. |
| Setup Research Owner | Defines compatible archetypes/treatments. |
| Independent Validator | Audits invariance and differential parity. |

# Procedure

## Step 1 — Create immutable context package

**Action**

Use UCEE I16 factory for schema, features, views, lifecycle, fixtures, tests and capabilities.

**Mandatory output**

- Context package.

**Stop conditions**

- Central engine modification is required without ADR/compatibility review.

## Step 2 — Certify occurrence identity

**Action**

Test determinism, known-time, future-suffix invariance, lifecycle and clustering.

**Mandatory output**

- Context certification.

**Stop conditions**

- Occurrence changes from future-only data or rerun nondeterminism.

## Step 3 — Build ontology mapping

**Action**

Map anatomy, direction, horizon, invalidation, views and parent/child relations.

**Mandatory output**

- Context ontology entry.

**Stop conditions**

- Mapping embeds treatment outcome or future label.

## Step 4 — Define setup archetypes

**Action**

Specify continuation/reversal/retest/etc. and compatibility with payoff/entry/trigger registries.

**Mandatory output**

- Setup compatibility graph.

**Stop conditions**

- Unbounded or semantically invalid treatments.

## Step 5 — Build replay/outcome support

**Action**

Add required path, fill, stop, exit, trail and economics support.

**Mandatory output**

- Outcome support manifest.

**Stop conditions**

- Replay cannot faithfully represent required treatment.

## Step 6 — Run baseline tournament

**Action**

Execute manual/naive/classical baselines under common folds and complete ledger.

**Mandatory output**

- Context baseline report.

**Stop conditions**

- Insufficient independent occurrences or role separation.

## Step 7 — Admit advanced research selectively

**Action**

Enable only technologies justified by data, horizon and baseline gap.

**Mandatory output**

- Capability admission.

**Stop conditions**

- Complexity precedes baseline or support.

## Step 8 — Publish onboarding handoff

**Action**

Register exact versions, limitations, monitoring and next experiment.

**Mandatory output**

- Context SAED handoff.

**Stop conditions**

- Any unresolved critical certification issue.

# Completion gates

- [ ] No central-core drift.
- [ ] Known-time/determinism certified.
- [ ] Finite compatibility graph.
- [ ] Replay/economics support complete.
- [ ] Baseline and capability admission documented.

# Evidence retained

- `context_package`
- `context_certification`
- `ontology_entry`
- `compatibility_graph`
- `outcome_support_manifest`
- `baseline_report`
- `capability_admission`
- `saed_handoff`

# Failure and escalation matrix

| Condition | Required response |
|---|---|
| Legacy mismatch | Remain differential/shadow; no behavior-changing migration. |
| Insufficient samples | Use manual-only or pooled research with explicit uncertainty; no promotion. |
| Unsupported path treatment | Remove candidate or improve replay before labels. |
| Core change requested | Require ADR and engine compatibility review. |

# Exit state

Context is research-ready, manual-only, shadow-only or rejected with explicit reasons.

# Related architecture

- [[00_Home]]
- [[End_To_End_Reference_Architecture]]
- [[Adversarial_Anti_Overfit_Red_Team]]
- [[Failure_Modes_Kill_Criteria_And_Recovery]]
