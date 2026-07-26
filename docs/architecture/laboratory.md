# Laboratory Architecture

## Decision Alpha Lab

---

## Purpose

Decision Alpha Lab is not a trading bot.

It is an evidence-generation laboratory designed to investigate whether structural information embedded in price can be transformed into robust, adaptive, and economically meaningful trading decisions.

The laboratory exists to answer research questions, generate evidence, reject weak ideas, validate promising hypotheses, and deploy only knowledge that survives rigorous testing.

The objective is not prediction.

The objective is the systematic discovery, validation, and operationalization of alpha.

---

# Fundamental Philosophy

Price is the only directly observable truth of the market.

Markets are collective decision systems continuously oscillating between self-reinforcing (momentum) and self-correcting (mean-reverting) dynamics.

The role of the researcher is not to predict the future.

The role of the researcher is to identify structural regularities, quantify uncertainty, and construct convex decision frameworks.

---

# Operating Principle

Every idea must pass through the following stages:

Observation

↓

Hypothesis

↓

Experimentation

↓

Analysis

↓

Validation

↓

Production

↓

Monitoring

↓

Retirement

No component is allowed to bypass this process.

---

# Layer 1 — Research

Research is the source of all knowledge.

Everything within this layer is considered uncertain.

Nothing in this layer is trusted with capital.

Its purpose is to generate hypotheses and explore mechanisms.

Structure:

research/

├── hypotheses/

├── experiments/

├── analyses/

└── reports/

---

## Hypotheses

A hypothesis is a formal statement describing a proposed market mechanism.

Each hypothesis must include:

* Research Question
* Motivation
* Hypothesis Statement
* Expected Mechanism
* Failure Conditions

Naming convention:

H001

H002

H003

Examples:

H001_decision_nodes

H002_decision_energy

H003_regime_transitions

---

## Experiments

Experiments are designed to challenge hypotheses.

A hypothesis may have multiple competing experiments.

Structure:

experiments/

H001/

EXP001/

EXP002/

EXP003/

Each experiment should contain:

* Configuration
* Dataset definition
* Methodology
* Code
* Results
* Interpretation

Required outcome:

Accepted

Rejected

Inconclusive

The objective is evidence, not confirmation.

---

## Analyses

Analyses are exploratory investigations.

They exist to generate intuition and identify potential directions.

Exploratory work must never enter production directly.

Examples:

* Distribution studies
* Visualization notebooks
* Feature exploration
* Market diagnostics

---

## Research Reports

Reports summarize completed investigations.

They preserve institutional memory.

Reports should include:

* Objective
* Methodology
* Findings
* Limitations
* Future Work

Negative findings are valuable findings.

---

# Layer 2 — Validation

Validation determines whether research findings are robust enough to be trusted.

The objective is not profitability.

The objective is survival under scrutiny.

Structure:

validation/

├── robustness/

├── walk_forward/

├── monte_carlo/

├── stress_tests/

└── benchmarks/

Any finding that fails validation cannot proceed.

---

## Robustness

Questions:

* Does performance collapse under small parameter changes?
* Is the mechanism overly sensitive?

---

## Walk-Forward Validation

Questions:

* Does the result persist out-of-sample?
* Does it generalize through time?

---

## Monte Carlo Analysis

Questions:

* Is the observed performance dependent on trade ordering?
* Could randomness explain the result?

---

## Stress Testing

Questions:

* Does the system survive adverse conditions?
* How fragile is the mechanism?

---

## Benchmarking

Questions:

* Does the proposed mechanism outperform simple alternatives?
* Is the added complexity justified?

Benchmark examples:

* Buy and Hold
* Donchian Trend Following
* ATR-Based Systems
* Moving Average Systems

---

# Layer 3 — Production

Production is reserved exclusively for validated knowledge.

Only mechanisms that survive validation may interact with capital.

Structure:

production/

├── signals/

├── execution/

├── monitoring/

└── models/

---

## Signals

Validated decision rules.

Examples:

SIG001

SIG002

SIG003

---

## Execution

Execution translates signals into broker actions.

Execution must remain simple and deterministic.

Research logic is prohibited.

---

## Monitoring

Production systems must be continuously observed.

Metrics may include:

* Performance drift
* Hit-rate drift
* Feature drift
* Regime instability

---

## Models

Only approved models belong here.

Experimental models remain in Research.

---

# Retirement

No model is permanent.

Any model that deteriorates beyond acceptable limits must be retired.

Structure:

archive/

├── retired_models/

├── rejected_hypotheses/

└── failed_experiments/

Retirement decisions must be documented.

Institutional memory prevents repeated mistakes.

---

# Separation of Responsibilities

Python is the research and intelligence layer.

Responsibilities:

* Data engineering
* Feature generation
* Structural analysis
* Regime detection
* Machine learning
* Backtesting
* Validation
* Signal generation

MQL5 is the execution layer.

Responsibilities:

* Broker communication
* Order placement
* Position management
* Logging
* Fail-safe procedures

Research logic must never reside within execution infrastructure.

---

# Naming Conventions

Hypotheses:

H001

H002

Experiments:

EXP001

EXP002

Reports:

RPT2026Q2

RPT2026Q3

Signals:

SIG001

SIG002

Models:

M001

M002

---

# Laboratory Principles

* Price is the only directly observable market truth.
* Structural assumptions are preferred over arbitrary temporal assumptions.
* Simplicity is preferred over unnecessary complexity.
* Prediction is secondary to adaptation.
* Convexity is more valuable than accuracy.
* Evidence is superior to conviction.
* Negative results are valuable.
* Reproducibility is mandatory.
* Validation is mandatory.
* Capital is entrusted only to validated knowledge.

---

# Closing Statement

Decision Alpha Lab is not a trading system.

It is an evidence-generation laboratory where market hypotheses compete for survival through experimentation, validation, and continuous monitoring before being entrusted with capital.

The purpose of the laboratory is not merely to generate returns.

Its purpose is to generate knowledge worthy of risk.
