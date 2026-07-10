---
id: AIEOS2-8254EA0D9830
title: "Windows PowerShell Patch Delivery"
type: standard
status: active
domain: alpha-lab-standard
version: 2.0.0
created: 2026-07-10
updated: 2026-07-10
tags:
  - ai-engineering
  - alpha-lab
  - alpha-lab-standard
---
# Windows PowerShell Patch Delivery

Decision Alpha Lab patch instructions target Windows PowerShell. Use quoted paths, `Expand-Archive -Force`, `Remove-Item`, `Test-Path`, and explicit arrays of changed files. Commands must be copy-paste safe from repository root and must not stage unrelated work.

Long Windows paths are controlled through bounded filenames and directory depth; do not repeat full semantic context in every filename.
