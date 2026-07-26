---
title: Look Budget Contract
status: accepted-reference
version: 1.0.0
phase: SAED_V4_28
tags: [saed-v4, v4-28]
---

# Look Budget Contract

This note is part of the accepted V4-28 online-FDR reference. It specifies the **look budget contract** contract as a closed, deterministic, known-time research control. The implementation consumes only the immutable V4-27 completeness evidence and cannot access hidden evaluation data.

## Engineering rule

The rule is enforced through exact input fields, deterministic ordering, canonical hashes, mutation tests, and fail-closed validation. Evidence observed after decision time cannot alter alpha, wealth, rejection, or certificate state. Any ambiguity resolves to quarantine or `skip`, never to an inferred rejection.

## Authority ceiling

This capability has no promotion, runtime, risk-allocation, execution, online-learning, or production authority. Static MQL5 evidence is not MetaEditor compilation; MetaEditor compilation is not runtime parity; runtime parity is not broker qualification.

## Relations

- Parent roadmap: [[V4_28_Anytime_Valid_Online_FDR]]
- Next governed phase: [[V4_29_Hidden_Evaluation_Air_Gap]]
