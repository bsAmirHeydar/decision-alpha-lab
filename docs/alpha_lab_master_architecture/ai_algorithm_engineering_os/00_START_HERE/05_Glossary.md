---
id: AIEOS-2EC811A423
title: "Glossary"
type: reference
status: active
domain: navigation
version: 1.0.0
created: 2026-07-10
updated: 2026-07-10
tags:
  - ai-engineering
  - glossary
---
# Glossary

| Term | Definition |
|---|---|
| **Artifact** | A durable engineering output: specification, contract, test, decision, patch, log, or evidence record. |
| **Assumption** | A proposition used without confirmed evidence; it must be visible and reviewable. |
| **Context packet** | The bounded information supplied to an AI agent for a specific task. |
| **Determinism** | Equal valid inputs and state produce equal outputs and transitions. |
| **Domain truth** | Project-owned meaning that the AI may not replace with generic knowledge. |
| **Done** | All required behavior, evidence, documentation, and rollback conditions are satisfied. |
| **Event** | An observed occurrence that may trigger a state transition. |
| **Formal specification** | A testable description of behavior, state, timing, constraints, and error semantics. |
| **Gate** | A binary acceptance condition required to proceed. |
| **Idempotency** | Repeating an operation does not create unintended additional effects. |
| **Invariant** | A property that must remain true across all valid states and transitions. |
| **Minimal safe patch** | The smallest bounded change that achieves the approved behavior and can be verified and rolled back. |
| **Non-goal** | Explicitly excluded behavior that prevents scope expansion. |
| **Ontology drift** | Silent replacement or reinterpretation of project terms by an AI or developer. |
| **Patch packet** | The full set of specification, manifest, code delta, tests, review, release, and rollback artifacts for one change. |
| **Replay** | Deterministic reconstruction of state from a historical event sequence. |
| **State** | Durable information required to interpret future events correctly. |
| **Transition** | A permitted state change caused by an event under defined guards. |
| **Vertical slice** | A small end-to-end increment that produces observable value while preserving architecture. |
