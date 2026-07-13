---
id: ALMA-2EBC1B49A6
title: "Knowledge-to-Context Architecture"
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
# Knowledge-to-Context Architecture

## 1. Purpose

The first architectural responsibility is to preserve the human viewpoint before implementation or profitability pressure changes it. The system turns subjective understanding into a stable semantic asset.

## 2. Transformation Chain

```text
Raw sources and human knowledge
→ doctrine package
→ ontology and vocabulary
→ ambiguity and assumption registers
→ formal context specification
→ implementation design
→ deterministic context engine
→ conformance evidence
```

## 3. Doctrine Package

Every context family starts with a versioned doctrine package containing:

- executive definition;
- market mechanism and rationale;
- exact vocabulary;
- entities, relationships and ownership;
- scope, non-goals and unsupported interpretations;
- event-time, known-time, confirmation-time and maturity-time;
- lifecycle states and terminal conditions;
- positive examples;
- visually similar negative examples;
- equality, overlap and one-tick boundary cases;
- invalidation, consumption and expiration;
- unresolved questions;
- source inventory and decision history.

Doctrine states what the market phenomenon means. It must not quietly include a preferred trade unless the trade action is itself part of the phenomenon.

## 4. Three Separate Documents

### Doctrine Document

Owns semantic truth and examples.

### Context Specification

Owns the machine-readable public contract: identity, fields, types, time semantics, lifecycle, compatibility, missingness and runtime requirements.

### Implementation Design

Owns algorithms, state stores, synchronization, performance, persistence, replay, MQL5/Python responsibility, tests and phased delivery.

Keeping these separate prevents implementation convenience from rewriting meaning.

## 5. Canon Freeze

A context may move through:

```text
Draft → Reviewable → Canonical → Superseded → Archived
```

After canon freeze, semantic changes require a new version and, when historical classification changes, a new research lineage. A definition cannot be edited after poor backtest results while pretending the same hypothesis was tested.

## 6. Human and AI Authority

Humans own ontology, unresolved interpretation, risk tolerance and canon approval. AI may extract, formalize, compare, critique, create fixtures, design algorithms and identify contradictions. AI cannot silently decide semantic truth.

## 7. Context Readiness

Before implementation:

- terms must have exact definitions;
- known-time must be explicit;
- state ownership must be unique;
- positive, negative and boundary cases must exist;
- missing/stale behavior must be declared;
- unresolved questions must be marked blocking or deferred;
- the intended context must be distinguishable from the intended setup.

## 8. Compounding Knowledge

Every solved ambiguity becomes reusable doctrine, fixture, primitive or rule. This is the first layer of compounding: the system no longer depends on remembering how the concept was understood during one conversation or one coding session.
