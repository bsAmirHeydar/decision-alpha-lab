---
title: Batch Changelog and Diff
status: accepted-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, acl-08, reporting]
---
# Batch Changelog and Diff

ACL-08 accepts an optional prior ACL-08 package. Material comparison is restricted to validation identity, decision distribution, gate-status distribution, unknown-evidence categories and reporting eligibility. File timestamps, paths and Markdown formatting are not material changes.

A missing prior package yields `FIRST_REPORT`. Identical evidence yields `NO_MATERIAL_CHANGE`. Changed evidence yields `MATERIAL_CHANGE` with explicit dimensions. Diff classification does not rank quality or authorize reruns; ACL-09 may use it when planning bounded research.
