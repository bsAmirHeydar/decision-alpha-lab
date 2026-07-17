---
title: "V4-34 Delivery 026 — Task Template"
status: accepted-reference
phase: SAED_V4_34
version: 1.0.0
updated: 2026-07-17
tags:
  - saed-v4
  - v4-34
  - sovereign-distributed-compute
  - delivery
---
# V4-34 Delivery 026 — Task Template

## Purpose

This delivery freezes the **Task Template** invariant for the sovereign distributed-compute reference. The invariant is additive, deterministic, known-time bounded, independently replayable and subordinate to the UCEE authority boundary.

## Contract

The corresponding JSON artifact and closed schema reject missing fields, unknown fields, mutable identities, future-known records, raw-data export paths, budget ambiguity and authority escalation. Identity is derived from canonical serialization and SHA-256 content binding.

## Deterministic behavior

Planning, partitioning, scheduling, synthetic execution, checkpointing, recovery and evidence construction use stable ordering and explicit seeds. Reordering equivalent registry inputs cannot alter the canonical plan or evidence result.

## Failure semantics

Any violation fails closed by rejecting the artifact, quarantining the node or route, halting the schedule, preserving the baseline and emitting an auditable incident. No fallback may silently weaken residency, evidence or authority constraints.

## Evidence

Verification is provided through golden fixtures, negative fixtures, mutation tests, deterministic replay, schema closure, hash ledgers, static MQL5 mirrors and an explicit distinction between reference evidence and unavailable external evidence.

## Authority boundary

This phase may plan and simulate distributed research compute. It may not select live treatments, allocate risk, mutate UCEE, compile an executable trading runtime, send an order or authorize production.
