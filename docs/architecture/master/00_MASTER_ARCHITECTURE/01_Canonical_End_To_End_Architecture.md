---
id: ALMA-853203C984
title: "Canonical End-to-End Architecture"
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
# Canonical End-to-End Architecture

## 1. Architectural Mission

Alpha Lab must transform an informal market viewpoint into a capital-bearing live policy without allowing any stage to silently take authority from another stage. The pipeline is therefore built as a sequence of governed transformations, each with its own inputs, outputs, owners, evidence and failure modes.

```text
Human market knowledge
→ formal doctrine
→ context specification
→ deterministic context engine
→ manual or AI exploitation policies
→ causal/economic outcomes
→ statistical evidence
→ capital and portfolio policy
→ immutable runtime generation
→ secure execution
→ assumption-aware monitoring
→ research memory
```

## 2. The Ten Planes

### 2.1 Knowledge Plane

Captures the human model of the market: ontology, vocabulary, causal story, examples, counterexamples, ambiguity, known-time and lifecycle. It defines meaning but does not decide trades.

### 2.2 Context Plane

Converts market truth into immutable context occurrences. It answers: what happened, when was it knowable, what state is it in, and what identity does it have?

### 2.3 Setup Plane

Defines exploitation. A setup may be written by a human or discovered by AI, but it must be a complete treatment: eligibility, entry, stop, exit, management, sizing constraints and abstention.

### 2.4 Research Plane

Generates path outcomes, executable economics, datasets, models, baselines and experiments. It is allowed to search, but only inside an explicit trial budget and protected data-role system.

### 2.5 Evidence Plane

Determines whether an observed result survives uncertainty, multiple testing, resampling, stress, null comparisons, out-of-sample tests and prospective evidence.

### 2.6 Capital Plane

Tests how a supported edge should be sized. It cannot turn a weak or negative edge into a valid one.

### 2.7 Portfolio Plane

Combines multiple edges, resolves overlapping exposure, allocates risk, controls concentration and enforces portfolio-level loss limits.

### 2.8 Runtime Plane

Compiles approved context, feature, model, threshold, treatment, risk and monitoring artifacts into one immutable generation.

### 2.9 Execution Plane

Applies hard risk gates, broker preflight, idempotent order submission, fill reconciliation, position lifecycle and emergency controls.

### 2.10 Monitoring and Evolution Plane

Compares live market, model, execution, portfolio and performance behavior with the assumptions that justified promotion. It can recommend continue, reduce, quarantine, revalidate or retire.

## 3. Why the Separation Matters

A context may be semantically correct but economically useless. A setup may be poorly designed over an informative context. A model may be statistically promising but impossible to execute. An edge may remain valid while broker slippage destroys realized returns. A profitable strategy may become dangerous when combined with correlated strategies.

Without plane separation, all failures collapse into “the strategy stopped working.” With separation, the system can locate the failure and reuse every unaffected layer.

## 4. Shared Platform Versus Strategy-Specific Work

### Shared permanently

- market truth and clock;
- identity and lineage;
- lifecycle framework;
- context SDK;
- treatment compiler;
- outcome and economics;
- dataset and split engine;
- trainer orchestration;
- statistical and anti-overfit suite;
- reporting and AI analyst;
- money-management library;
- portfolio allocation;
- runtime compiler;
- security, licensing and execution;
- monitoring, drift and retirement.

### Strategy/context-specific

- doctrine and semantic meaning;
- unique anatomy extraction;
- context-specific states and fields;
- optional manual setup logic;
- treatment compatibility declarations;
- rare context-specific labels or execution semantics.

## 5. Evidence Is Not Binary

The system uses an evidence lifecycle:

```text
Proposed
→ Context-Conformant
→ Research Candidate
→ Statistically Supported
→ Paper Validated
→ Micro-Live Validated
→ Production Qualified
→ Reduced
→ Quarantined
→ Retired
```

The phrase “this strategy has edge” is replaced with a conditional statement binding edge to context version, treatment, market, cost model, regime, horizon and evidence level.

## 6. The Closed Loop

The architecture is not complete until live evidence returns to research memory without contaminating current protected tests. Realized fills recalibrate economics. Drift creates new experiments. Failures become searchable knowledge. Retired edges remain available as negative evidence.

The loop must learn, but never mutate production invisibly.
