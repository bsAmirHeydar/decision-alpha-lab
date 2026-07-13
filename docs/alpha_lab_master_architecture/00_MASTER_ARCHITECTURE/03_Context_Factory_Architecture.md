---
id: ALMA-A90324B5D9
title: "Context Factory Architecture"
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
# Context Factory Architecture

## 1. Role

The Context Factory is the bridge between doctrine and every downstream strategy. It produces deterministic, causally valid and immutable context snapshots. It does not decide whether to trade.

## 2. Context Package

```text
ContextPackage
├── DoctrineVersion
├── ContextSpec
├── AnatomyAdapter
├── FeaturePack
├── LifecycleProfile
├── RepresentationProfile
├── AllowedTreatmentFamilies
├── LabelProfile
├── MonitoringAssumptions
├── RuntimeCompatibility
└── ConformanceFixtures
```

## 3. Market Truth Layer

All context engines consume a canonical market layer rather than reimplementing broker/time logic. The shared layer owns:

- bars and ticks;
- bid/ask semantics;
- symbol specification and aliases;
- sessions, trading days and DST;
- higher-timeframe aggregation;
- multi-symbol synchronization;
- missing, stale, duplicated and reordered input states;
- source inventory and revisions;
- spread and executable-price observations.

Centralizing this layer removes a major class of repeated errors.

## 4. Universal Mechanisms, Specific Meaning

Reusable primitives may include structural points, references, boundaries, excursions, returns, confirmations, sequences, relationships, freshness, entitlement, expiration and invalidation.

The primitive supplies identity, lifecycle and replay mechanics. Each context still owns its exact semantic definition. The platform must not force every theory into one universal definition of “break,” “pivot” or “confirmation.”

## 5. Context SDK and Compiler

The intended steady state is declarative onboarding. A ContextSpec declares required fields, state machine, known-time, identity, dependencies, compatibility and fixtures. The compiler generates or validates:

- schema and serialization;
- deterministic IDs;
- registry entry;
- feature-order contract;
- dataset mapping;
- test and fixture scaffolds;
- runtime compatibility;
- monitoring contract skeleton;
- documentation index.

The only hand-written core should be unique extraction semantics.

## 6. Context Occurrence Lifecycle

A generic form is:

```text
Observed
→ Candidate
→ Confirmed
→ Eligible
→ Consumed / Invalidated / Expired
→ Retired
```

Each context can specialize states. The shared lifecycle framework validates transitions and records history, while doctrine defines the transition predicates.

## 7. Context Composition

Context occurrences may form graphs:

- parent/child;
- confirms;
- contradicts;
- prerequisite;
- higher-timeframe owner;
- intermarket relationship;
- temporal predecessor;
- shared opportunity cluster.

Combined contexts receive new identity and lineage; parent occurrences remain immutable.

## 8. Conformance Before Profitability

A context is research-enabled only after:

- semantic fixtures pass;
- future mutation cannot alter prior outputs;
- replay/restart preserve identity;
- lifecycle transitions are valid;
- historical and live modes agree;
- missing/stale behavior is correct;
- performance budgets are met;
- renderer and setup layers cannot mutate context truth.

A profitable but semantically wrong detector is rejected.
