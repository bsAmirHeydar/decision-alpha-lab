---
title: Human Accountability and Dual Control
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: core-production
tags:
  - saed-v3
---

# Mission

Keep named humans accountable for specifications, protected access, promotion, risk, authorization, and exceptions.

## Why this component exists

- None declared.

## Authority and safety boundary

- This component may estimate, rank, simulate, challenge, or recommend only inside a declared research scope.
- It cannot create canonical Context truth, modify protected evidence roles, sign promotion, change portfolio risk, activate runtime generations, access live credentials, or place orders.
- Unsupported, stale, contradictory, OOD, hash-mismatched, uncalibrated, or incomplete paths resolve to **Skip**, **Abstain**, **Manual fallback**, **Reject**, or **Quarantine**.
- Every result is subordinate to UCEE I12 promotion admission, I13 authority/fallback, I14 immutable runtime, I17 portfolio/risk, and I18 release qualification.

## Input contracts

- Signed agent task envelope.
- Approved source artifacts.
- Tool allowlist and compute budget.

## Output contracts

- Structured proposal, code, test, finding, or evidence artifact.
- Complete action and exposure trace.

## Algorithmic design

- Separate planner, executor, critic, and approver roles.
- Use deterministic tools and schemas where possible.
- Require source citations and artifact hashes for claims.
- Route material outputs to independent human or model-risk review.


## Data and known-time semantics

- No protected role unless explicitly granted for safety/forensics.
- Memory is campaign- and role-scoped.
- Retrieved content is untrusted input.

## Anti-overfit and model-risk controls

- No order, broker, capital, promotion, signature, risk, runtime activation, or Context-truth authority.
- Short-lived credentials.
- Filesystem and network sandbox.
- Budget and expiration.

## Measurement system

- Task success.
- Unauthorized-action rate.
- Exposure count.
- Human correction rate.
- Reproducibility.

## Scalability and operating model

- Event-driven agent queue.
- Per-agent quotas.
- Artifact-mediated collaboration rather than shared hidden state.

## Adversarial failure modes

- Prompt injection.
- Agent fabricates evidence.
- Agent retries until significance.
- Memory leaks hidden result.
- Human rubber-stamps output.

## UCEE integration

- Agents may prepare artifacts; only UCEE governance and named authorized humans admit, compile, allocate, or activate.

## Required tests and evidence

- Privilege escalation.
- Prompt injection corpus.
- Protected-data canary.
- Tool failure.
- Conflicting agents.

## Implementation slices

- None declared.

## Decision record

- None declared.

## Acceptance gate

The component is accepted only when its contracts are closed and versioned, all lineage and role boundaries are reconstructible, protected evaluation remains unexposed, negative and mutation tests pass, simpler baselines remain available, and an independent reviewer can reproduce the decision-equivalent result from immutable hashes.

## Related notes

- [[Multi_Agent_Research_Operating_System]]
- [[Agent_Task_Envelope_And_Sandbox]]
