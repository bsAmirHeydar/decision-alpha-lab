---
title: ACL-09 — Memory and Active Planner
status: proposed-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, acl-09, memory]
---
# ACL-09 — Memory and Active Planner

ACL-09 consumes `ACL08_TO_ACL09` and owns governed memory admission, duplicate detection and bounded research planning.

## ACL-08 dependency contract

ACL-09 must verify the ACL-08 manifest, receipt, report run, Batch Report, Experience Bundle, Event Ledger and Provenance Graph. It must preserve source decision digests and may not rewrite ACL-07 validation semantics.

Required actions are:

- `INGEST_REPORT_PACKAGE`
- `INDEX_EXPERIENCE_RECORDS`
- `DETECT_RESEARCH_DUPLICATES`
- `PROPOSE_BOUNDED_RESEARCH_QUESTIONS`

Forbidden actions include inferring alpha from summaries, promoting reporting output, granting execution authority, activating capital or amending doctrine without approval.

## Outputs expected

A governed memory-admission decision, duplicate/equivalence report, bounded planner proposals, security evidence, human projection and an explicit handoff to ACL-10. Planner proposals are not experiment execution or promotion permission.
