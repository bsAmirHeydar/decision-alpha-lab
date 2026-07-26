---
title: Runbook — Promotion, Runtime Compilation and Portfolio Handoff
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

Transform an approved candidate into immutable UCEE policy/runtime/portfolio artifacts without changing learned behavior, authority or evidence scope.

# Entry conditions

- Signed promotion admission and prospective evidence exist.
- All artifact versions and support boundaries are fixed.
- Runtime/MQL5 and portfolio owners accept handoff scope.

# Roles and separation of duties

| Role | Responsibility |
|---|---|
| Promotion Authority | Signs bounded admission. |
| Runtime Compiler Owner | Builds immutable generation. |
| MQL5 Validator | Runs cross-language parity. |
| Risk/Portfolio Owner | Defines reservation and veto integration. |
| Operations Release | Qualifies activation and rollback. |

# Procedure

## Step 1 — Bind promotion scope

**Action**

Record context, action/treatment/risk support, model, calibration, validity, fallback and kill criteria.

**Mandatory output**

- Promotion admission artifact.

**Stop conditions**

- Admission exceeds evidence support.

## Step 2 — Compile policy graph

**Action**

Integrate manual rules, AI filter/rank, uncertainty, fallback, operator and hard veto order.

**Mandatory output**

- Compiled UCEE I13 policy graph.

**Stop conditions**

- AI can create context or override risk/manual veto.

## Step 3 — Build immutable runtime

**Action**

Compile features, preprocessing, model, policy, treatment, risk, monitoring and rollback pointer.

**Mandatory output**

- UCEE I14 runtime bundle.

**Stop conditions**

- Bundle is partial, unsigned or incompatible.

## Step 4 — Run cross-language parity

**Action**

Compare Python/export/MQL5 features, predictions, decisions, fallback and traces.

**Mandatory output**

- Parity certificate.

**Stop conditions**

- Actual compile/parity evidence is missing or tolerance/decision agreement fails.

## Step 5 — Integrate portfolio contract

**Action**

Publish edge genome, capacity, dependence, requested risk and reservation semantics.

**Mandatory output**

- UCEE I17 handoff.

**Stop conditions**

- Allocation can occur without reservation or conservative dependence.

## Step 6 — Qualify operations

**Action**

Run compile matrix, soak, chaos, no-send, recovery, authorization and release tests.

**Mandatory output**

- UCEE I18 qualification packet.

**Stop conditions**

- Any production gate remains blocked.

## Step 7 — Activate bounded generation

**Action**

Use signed short-lived authorization and atomic generation transition.

**Mandatory output**

- Activation record.

**Stop conditions**

- Authorization expired/revoked or rollback unavailable.

# Completion gates

- [ ] Promotion scope does not exceed evidence.
- [ ] Policy authority order is explicit.
- [ ] Complete immutable bundle and parity pass.
- [ ] Portfolio reservation/risk veto remain independent.
- [ ] I18 qualification and authorization are actual, not fixture/static.

# Evidence retained

- `promotion_admission`
- `compiled_policy_graph`
- `runtime_bundle`
- `parity_certificate`
- `edge_genome`
- `portfolio_handoff`
- `production_qualification`
- `activation_record`

# Failure and escalation matrix

| Condition | Required response |
|---|---|
| Parity mismatch | Block activation; fix source; regenerate all evidence. |
| Portfolio contract unsupported | Abstain or keep standalone paper; no hidden allocation. |
| Runtime artifact changes | New generation and requalification required. |
| Authorization revoked | Immediate disable without rewriting historical evidence. |

# Exit state

Generation is either boundedly active, shadow-only, quarantined or rejected; no ambiguous state.

# Related architecture

- [[00_Home]]
- [[End_To_End_Reference_Architecture]]
- [[Adversarial_Anti_Overfit_Red_Team]]
- [[Failure_Modes_Kill_Criteria_And_Recovery]]
