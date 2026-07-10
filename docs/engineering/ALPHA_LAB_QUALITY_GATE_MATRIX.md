---
id: AIEOS2-851667FF700E
title: "Alpha Lab Quality Gate Matrix"
type: standard
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
# Alpha Lab Quality Gate Matrix

## Gate Philosophy

Gates fail closed when evidence is missing. A warning is not silently converted to pass.

| Gate | Required Evidence | Blocks |
|---|---|---|
| Discovery | Problem, ontology, examples/counterexamples, unknowns | Formal design |
| Specification | States, events, invariants, inputs/outputs, time semantics, non-goals | Coding |
| Architecture | Boundaries, ownership, dependency direction, contracts | Patch approval |
| Code Readiness | Exact files, tests, rollback, compatibility | Implementation |
| Compile/Static | Zero errors; warnings reviewed; compatibility scan | Runtime testing |
| Unit/Invariant | Deterministic tests and property checks | Integration |
| Replay/Visual | Historical/live parity and visual evidence | Validation |
| Data/Schema | Version, lineage, duplicate/orphan checks, availability time | Model research |
| OOS/Model | Fixed folds, baseline, leakage audit, calibration, stability | Promotion |
| Decision Promotion | Human approval, versioned rule, rollback | Execution inclusion |
| Paper Execution | Broker, state, risk, idempotency, failure tests | Live capital |
| Release | Package, checksum, changelog, install, rollback, monitoring | Deployment |

## Evidence Record

Every gate result records:

```text
gate_id
status: PASS | CONDITIONAL | FAIL
artifact/version
commands executed
result summary
reviewer
exceptions
expiry/next review
```

## Conditional Pass

Conditional status is allowed only when the missing evidence cannot affect domain correctness, capital safety, schema integrity, or replay parity. It must have an owner and expiry.
