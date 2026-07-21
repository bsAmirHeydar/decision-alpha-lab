---
id: AIEOS2-A6E52DE2EBA7
title: "Decision Alpha Lab Engineering Handbook"
type: handbook
status: active
domain: engineering
version: 2.0.0
created: 2026-07-10
updated: 2026-07-10
tags:
  - ai-engineering
  - alpha-lab
  - engineering
---
# Decision Alpha Lab Engineering Handbook

## 1. Purpose

This handbook defines how Decision Alpha Lab converts intuition into durable software and evidence. It governs research, algorithms, data, MQL5, Python, AI-assisted development, patch delivery, validation, model promotion, execution safety, and knowledge management.

The target is not maximum code velocity. The target is **correctness under replay, traceability under review, reversibility under failure, and causal integrity under research**.

## 2. System Lifecycle

```text
Intent
→ Observation
→ Ontology
→ Hypothesis
→ Formal Specification
→ Algorithm / State Model
→ Architecture / Contracts
→ Minimal Vertical Patch
→ Compile and Verification
→ Experiment / Outcome Evidence
→ Validation / OOS
→ Decision Promotion
→ Paper Execution
→ Live Execution
→ Monitoring
→ Retirement / Learning
```

No stage may silently bypass its predecessor. Exploratory code may be fast; production authority may not be implicit.

## 3. Truth and Authority

Market/domain truth comes from approved doctrine and observed evidence. Engineering standards define how truth is encoded; they do not invent it. AI is a bounded engineering participant, never the owner of domain meaning or capital authority.

When implementation and specification disagree, stop and resolve the conflict. Do not normalize the disagreement by adding exceptions in code.

## 4. Specification Standard

A code-ready specification includes:

- problem and owner;
- authoritative vocabulary;
- current and desired behavior;
- examples and counterexamples;
- entities, state, events, transitions;
- invariants and invalidation;
- time, symbol, timeframe, and data-availability semantics;
- inputs, outputs, contracts, errors;
- performance and memory budgets;
- non-goals and compatibility;
- acceptance tests and Definition of Done.

Normative statements must be testable or observable. Unknowns remain named unknowns.

## 5. Architecture Standard

Separate:

```text
pure domain/core calculation
state ownership and lifecycle
signal/scenario construction
persistence and schemas
observability and audit
rendering/UI
adapters and external I/O
risk authorization
execution
```

Every mutable state item has one owner. Data contracts are versioned APIs. Dependency direction follows authority from doctrine toward adapters; adapters cannot redefine doctrine.

## 6. Implementation Standard

Work in reversible vertical slices. Each patch must be small enough to understand and test but complete enough to demonstrate one behavior end to end. Avoid partial horizontal layers that create unused contracts or speculative abstractions.

Before editing, inspect the exact implementation and call graph. During bug fixes, locate the first causal defect. After each patch, rebuild and run focused checks. Consolidation/refactoring follows only after behavior is characterized.

## 7. Causal-Time Standard

All research and live systems distinguish event, observation, availability, and processing time. Historical reconstruction must emulate what was knowable at each historical decision point. Future extrema, final-day ranges, future labels, and full-history rankings cannot enter live/model features unless the decision time truly had them.

For market references, lifecycle is explicit: candidate, active, protected, consumed, invalidated, retired. A consumed or superseded level cannot re-enter by accident.

## 8. MQL5 Standard

MQL5 is treated as its actual language/runtime, not approximate C++. Compiler-specific behavior is documented and scanned. Timeseries indexing, closed-bar confirmation, multi-symbol synchronization, object ownership, callback idempotency, and file paths are explicit.

Known permanent rules:

- Case-conversion functions mutate lvalues and return `bool`.
- Do not assume `LongToString` exists.
- Validate data-copy counts and symbol history.
- Never draw cross-symbol price coordinates on another symbol’s chart.
- Research experts do not place orders.

## 9. Python and Model Standard

Research modules are deterministic, importable, typed, configured, and testable. Notebooks are analysis surfaces, not hidden libraries. Model experiments use fixed OOS folds, train-only transforms, simple baselines, leakage audits, calibration/error analysis, stability, model cards, and reproducible run identity.

A model winner is evidence. It has no execution authority until a human-approved decision promotion artifact changes the production contract.

## 10. Verification Standard

Verification is layered:

```text
compile/static
unit
invariant/property
scenario
historical replay
golden/characterization
visual
performance
schema/lineage
OOS/model
paper execution
release/rollback
```

Each test claims only what it observes. Compilation proves syntax/type acceptance, not strategy correctness.

## 11. Patch and Git Standard

Deliver root-relative ZIP patches with install, exact staging, atomic commit, rollback, and documentation. Use PowerShell commands compatible with the user’s environment. Never stage the entire repository by convenience. Patch identity and file list are part of the audit trail.

## 12. Observability Standard

Diagnostics must reveal state and failures without changing strategy behavior. Logs use stable event IDs and sufficient context. Research ledgers preserve signal/sample identity. UI/renderer objects are disposable projections of state, not the source of state.

## 13. Security and Secrets

No credentials, tokens, license secrets, private keys, personal data, or broker secrets in source, prompts, screenshots, logs, ZIP patches, or Obsidian notes. Configuration separates safe defaults from environment secrets. License systems fail safely and remain isolated from strategy semantics.

## 14. Governance and Exceptions

MUST-level deviations require a waiver with scope, owner, risk, compensating controls, expiry, and closure evidence. Domain ontology, causal integrity, evidence honesty, primary-key integrity, and capital safety cannot be waived informally.

## 15. Completion

Work is done when behavior, evidence, documentation, installation, rollback, and residual risk are all explicit. If a tool was unavailable, say so. If a result is unverified, label it unverified. Durable engineering is independent of the original conversation.

## Related Standards

- [[ALPHA_LAB_POLICY_HIERARCHY|Policy Hierarchy]]
- [[ALPHA_LAB_CODE_STYLE_STANDARD|Code Style]]
- [[ALPHA_LAB_QUALITY_GATE_MATRIX|Quality Gates]]
- [[docs/evidence/alpha_lab_release_standard/db0cec343c04_ALPHA_LAB_PATCH_RELEASE_STANDARD|Patch and Release]]
- [[ALPHA_LAB_MQL5_COMPATIBILITY_STANDARD|MQL5 Compatibility]]
- [[ALPHA_LAB_RESEARCH_REPRODUCIBILITY_STANDARD|Research Reproducibility]]
- [[ALPHA_LAB_EXECUTION_SAFETY_STANDARD|Execution Safety]]
