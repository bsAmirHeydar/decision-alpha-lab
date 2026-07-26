---
id: ALMA-0094FBD74B
title: "Runtime, Security and Execution"
type: architecture
status: canonical
domain: alpha-lab-master-architecture
version: 1.0.0
created: 2026-07-13
updated: 2026-07-13
tags:
  - alpha-lab
  - master-architecture
---
# Runtime, Security and Execution

## 1. Runtime Bundle Compiler

Approved research artifacts are compiled into an immutable generation containing:

- context and feature schema hashes;
- fixed preprocessing and feature order;
- model or deterministic policy;
- calibration and thresholds;
- complete treatment state machine;
- risk and allocation limits;
- abstention and fallback;
- monitoring contract;
- signatures and licensing;
- parity evidence;
- rollback pointer.

Production never mutates a generation in place.

## 2. Fast Path

```text
Market Event
→ Context Update
→ Predecision Gates
→ Candidate Evaluation
→ Model/Policy Decision
→ Utility / Uncertainty / Abstention
→ Decision Envelope
→ Hard Risk Gate
→ Broker Preflight
→ Order Request
→ Fill and Position Reconciliation
```

## 3. Authority Boundaries

The model recommends but cannot place orders, increase size, widen stops or override limits. The execution layer submits and reconciles but cannot rewrite the model decision. The hard risk gate is local, deterministic and fail-closed.

## 4. Hard Risk Gate

Checks include:

- generation authorization;
- context freshness and lineage;
- maximum cash loss;
- stop and volume validity;
- account, strategy and portfolio limits;
- exposure and reservations;
- daily/weekly loss;
- margin;
- broker stop/freeze levels;
- duplicate/idempotency;
- market/session permission;
- kill-switch and incident state.

## 5. Expected Versus Actual

The live ledger separates:

- expected decision;
- expected executable price/fill;
- actual request;
- actual fill;
- actual position.

This distinction is essential for diagnosing edge decay versus execution drift.

## 6. Security and Licensing

Security covers:

- model/code confidentiality;
- signed artifact integrity;
- broker/account binding;
- entitlement and expiration;
- secrets;
- tamper detection;
- update trust;
- audit retention.

License failure must not make open positions unsafe. Safety-critical exit and risk logic remain operable under a defined degraded mode.

## 7. Incidents and Rollback

Kill levels range from one policy to global entry shutdown. Every generation has a known-good predecessor. The incident flow is:

```text
Detect → Contain → Preserve → Reconcile → Diagnose → Correct → Revalidate → Resume or Retire
```

Retraining is not an emergency patch; it opens a new governed lineage.
