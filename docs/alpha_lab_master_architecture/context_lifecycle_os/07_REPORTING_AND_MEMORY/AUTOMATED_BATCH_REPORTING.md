---
title: Automated Batch Reporting
status: accepted-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, acl-08, reporting]
---
# Automated Batch Reporting

ACL-08 generates reports only from the verified ACL-07 machine package. The reporter does not query mutable research state, recompute validation gates or infer missing values. Every number in a report must resolve to a source digest.

## Mandatory sections

Identity and source binding, decision distribution, complete candidate evidence, gate status, baselines, diagnostic isolation, unknown evidence, negative findings, limitations, provenance, security boundaries and next permitted actions are mandatory. A report that omits failures or UNKNOWN gates is invalid.

## Determinism

The same ACL-07 handoff, report policy, timestamp and optional previous-report identity must produce byte-identical machine reports and Markdown projections. Human editing of generated reports is prohibited; commentary belongs in separately governed notes.
