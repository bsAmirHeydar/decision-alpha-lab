---
id: SAED-4577D7DCDD
title: "Context Is Not Setup"
type: architecture
status: canonical
domain: strategy-factory-setup-ai-edge-discovery
version: 1.0.0
created: 2026-07-13
updated: 2026-07-13
tags:
  - strategy-factory
  - setup-factory
  - ai-training
  - doctrine
  - context
---

# Context Is Not Setup

## Rule

A Context is a causal, known-time description of market state. A Setup is a governed exploitation hypothesis. A profitable historical action cannot be used to retroactively redefine the Context.

## Consequences

- Context detection is frozen before Treatment search.
- Context features may describe state but not outcomes.
- Entry, stop and exit logic belongs to Treatment/Policy layers.
- A Context may validly produce no Setup.
- One Context may support multiple Setup archetypes and payoff profiles.
- Rejection of all Treatments does not invalidate the Context semantics.

## Failure Pattern

The most dangerous shortcut is to tune the Context detector until a preferred entry looks profitable. This merges semantic discovery and exploitation selection and makes selection accounting incomplete.

## Verification

Future-suffix perturbation must not change historical Context occurrence identity. Treatment outcomes may change only after the decision timestamp.
