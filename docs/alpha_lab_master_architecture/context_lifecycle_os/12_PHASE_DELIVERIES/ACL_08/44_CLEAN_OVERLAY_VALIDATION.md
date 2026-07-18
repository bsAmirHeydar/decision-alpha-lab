---
title: ACL-08 44 Clean Overlay Validation
status: accepted-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, acl-08, reporting]
---
# ACL-08 44 Clean Overlay Validation

## Purpose

Patch application over ACL-07 current state.

## Contract

This phase consumes only verified ACL-07 evidence and is governed by `ACL08_REPORT_POLICY_V1`. Decision status, reason codes and gate states are immutable.

## Acceptance

- Deterministic and replayable output.
- Explicit UNKNOWN and limitations.
- Diagnostic and baseline isolation preserved.
- No alpha, promotion, order or capital authority.
- Source digests and downstream handoff resolve exactly.

## Failure semantics

Missing evidence, policy drift, digest mismatch, redaction leakage or authority escalation stops publication without partial output.
