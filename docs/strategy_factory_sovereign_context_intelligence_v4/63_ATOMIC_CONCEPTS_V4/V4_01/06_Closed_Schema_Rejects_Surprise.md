---
title: Closed Schema Rejects Surprise
status: implemented
version: 1.0.0
phase: V4-01
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: core-production-data-plane
tags:
  - saed-v4
  - v4-01
  - atomic-concept
---

# Closed Schema Rejects Surprise

> **Parent phase:** [[00_MOC_V4_01_Sovereign_Data_And_Artifact_Foundation]]

## Definition

Unknown fields are errors. Producers must explicitly version and migrate contract changes.

## Why it matters

Without this invariant, a research result can appear reproducible while depending on future knowledge, mutable data, hidden schema drift, contaminated evidence or an untraceable correction.

## Machine test

The V4-01 test suite contains at least one positive and one negative or mutation test for this concept. A failure is blocking.

## Related

- [[00_MOC_V4_01_Sovereign_Data_And_Artifact_Foundation]]
