---
title: Runbook — Execute a Governed Multi-Agent Research Run
status: canonical
version: 2.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v2
- runbook
- operations
---

# Purpose

Coordinate specialized AI agents for bounded research tasks with reproducible tool use, independent verification and zero promotion/trading authority.

# Entry conditions

- Approved research program and agent authority matrix exist.
- Typed task envelopes and sandbox capabilities are issued.
- Canonical memory and artifact stores are reachable under role controls.

# Roles and separation of duties

| Role | Responsibility |
|---|---|
| Human Run Owner | Accepts plan and final artifacts. |
| Director Agent | Decomposes task within envelope. |
| Worker Agents | Produce proposals/code/analysis. |
| Verifier Agents | Independently test claims and artifacts. |
| Security Monitor | Enforces tool and credential policy. |

# Procedure

## Step 1 — Create signed run manifest

**Action**

Declare objective, inputs, tools, roles, budgets, forbidden actions, stop conditions and outputs.

**Mandatory output**

- Agent run manifest.

**Stop conditions**

- Task requires promotion, risk change, live action or protected access outside envelope.

## Step 2 — Plan and decompose

**Action**

Director creates explicit dependency graph and assigns least-privilege subtasks.

**Mandatory output**

- Agent execution plan.

**Stop conditions**

- Plan mutates canonical assumptions or hides unverified dependencies.

## Step 3 — Execute in sandboxes

**Action**

Workers use approved deterministic tools and create content-addressed artifacts.

**Mandatory output**

- Worker artifact set and tool log.

**Stop conditions**

- Agent attempts unauthorized file/network/credential action.

## Step 4 — Verify independently

**Action**

Verifiers rerun tests, inspect lineage, challenge assumptions and record disagreement.

**Mandatory output**

- Verification records.

**Stop conditions**

- Critical claims lack independent verification.

## Step 5 — Adjudicate disagreement

**Action**

Human/independent owner reviews evidence; no coordinator overwrite.

**Mandatory output**

- Disagreement packet and decision.

**Stop conditions**

- Evidence is insufficient or conflict involves authority boundary.

## Step 6 — Merge approved artifacts

**Action**

Apply reviewed diff, run QA and bind hashes to parent program.

**Mandatory output**

- Accepted artifact bundle.

**Stop conditions**

- Generated content changes unapproved paths or contracts.

## Step 7 — Close and learn

**Action**

Record failures, costs, accepted/rejected outputs and reusable memory.

**Mandatory output**

- Agent run closure.

**Stop conditions**

- Tool logs or source trace are incomplete.

# Completion gates

- [ ] Least privilege enforced.
- [ ] All tool calls and artifacts auditable.
- [ ] Independent verification exists.
- [ ] Human owner accepts changes.
- [ ] No agent can promote, authorize or trade.

# Evidence retained

- `agent_run_manifest`
- `execution_plan`
- `tool_log`
- `worker_artifacts`
- `verification_records`
- `disagreement_packet`
- `run_closure`

# Failure and escalation matrix

| Condition | Required response |
|---|---|
| Unauthorized action attempt | Deny, terminate token, preserve logs, open incident. |
| Fabricated source/evidence | Reject artifact; quarantine agent configuration; review memory. |
| Generated leakage | Invalidate downstream artifacts and update sentinel tests. |
| Agent disagreement unresolved | Escalate; no merge/promotion. |

# Exit state

Approved research artifacts are merged or rejected; authority state is unchanged.

# Related architecture

- [[00_Home]]
- [[End_To_End_Reference_Architecture]]
- [[Adversarial_Anti_Overfit_Red_Team]]
- [[Failure_Modes_Kill_Criteria_And_Recovery]]
