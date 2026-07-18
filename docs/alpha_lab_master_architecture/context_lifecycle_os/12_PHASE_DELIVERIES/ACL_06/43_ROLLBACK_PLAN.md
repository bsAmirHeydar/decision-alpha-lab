---
title: Rollback Plan
status: accepted-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, acl-06]
---
# Rollback Plan

## Intent

Deletes staging before publication and reverts commits after publication.

## Accepted design

ACL-06 consumes one exact frozen ACL-05 Batch, plans only closed registered tasks, executes deterministically under frozen budgets and publishes immutable descriptive evidence. No component in this phase may rewrite upstream semantics or infer trading authority.

## Failure semantics

Unknown fields, unresolved identities, digest mismatch, cycles, dependency failure, budget breach, known-time violation, diagnostic-lane escape or publication conflict stop the run fail closed with explicit evidence.

## Verification obligations

The implementation is covered by contract tests, hostile mutations, deterministic replay, resource accounting, schema checks, static contract checks and clean-overlay validation.

## Claim boundary

This document and its code prove reference orchestration mechanics only. They do not establish alpha, statistical robustness, broker parity, live execution or capital fitness.

## Related

[[ACL_06_RESEARCH_DAG_ORCHESTRATION]], [[ACL06_RESEARCH_DAG_RUNTIME]], [[ACL06_ACL07_HANDOFF]]
