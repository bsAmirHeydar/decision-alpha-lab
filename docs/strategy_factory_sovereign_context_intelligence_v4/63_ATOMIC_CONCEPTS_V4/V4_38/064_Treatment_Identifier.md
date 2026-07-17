---
title: SAED V4-38 Treatment Identifier
status: canonical
phase: SAED_V4_38
tags: [atomic-concept, immutable, research-only]
---
# SAED V4-38 — Treatment Identifier

## Definition

**Treatment Identifier** is a research-only atomic control in the immutable runtime and MQL5 parity architecture. It has one closed meaning, a deterministic representation and an explicit failure action.

## Invariant

The control must not silently expand authority, mutate a sealed runtime bundle, reinterpret an ABI field, convert static evidence into external evidence, or bypass baseline preservation.

## Evidence

The accepted evidence is a closed schema, canonical example, deterministic hash, positive test, negative or mutation test and a traceable reference in the V4-38 evidence bundle.

## Failure behavior

Any missing, stale, inconsistent or unverifiable input causes abstention and escalation. Actual MetaEditor or terminal claims require actual external evidence; synthetic parity is insufficient.
