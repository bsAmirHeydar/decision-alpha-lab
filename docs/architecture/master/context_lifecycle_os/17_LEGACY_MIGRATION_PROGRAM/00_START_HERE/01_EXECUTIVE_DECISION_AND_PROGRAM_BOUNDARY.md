---
title: "Executive Decision and Program Boundary"
status: proposed-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration]
---
# Executive Decision and Program Boundary

## Decision

Create a separate governed program named **Legacy Context Migration Program (LCM)**. Do not extend the closed ACL-00…ACL-15 reference sequence with an artificial ACL-16. LCM consumes ACL-OS as the destination operating system and treats all previous Context, Setup and execution projects as migration sources.

## Why a separate program is required

The repository contains mature but heterogeneous projects, generated architecture mirrors, research code, MQL5 anatomy experts, paper and execution modules, extensive Obsidian projections and root-level release artifacts. A direct folder cleanup would combine semantic migration, code refactoring, documentation consolidation and deletion in one uncontrolled operation.

LCM separates those concerns and makes each irreversible operation evidence-gated.

## Program invariants

- No semantic change is hidden inside a move or rename.
- No bug fix is hidden inside parity migration.
- No two artifacts are merged from naming similarity alone.
- No legacy file is deleted before a canonical replacement, reference scan, parity evidence, quarantine period and rollback proof exist.
- Diagnostic and future-aware behavior remains segregated.
- Context, Setup, Treatment, visualization and execution authority are separated.
- A report, model or migration tool never acquires order or capital authority.
- The ACL-OS kernel and SAED/UCE platform are protected platform assets, not legacy Contexts to be folded into a domain package.

## Scope

LCM covers:

- MQL5 Experts, Indicators, Scripts and Includes carrying historical Context or Setup behavior;
- Python research or adapter code tied to those domain families;
- experiment specifications and Obsidian knowledge packages;
- duplicate documentation namespaces and generated projections;
- root-level release metadata, installer scripts and commit records;
- compatibility wrappers, redirects, deprecation, quarantine and deletion.

## Non-goals

LCM does not:

- optimize strategy parameters;
- change market doctrine without an approved owner decision;
- establish alpha or validation;
- activate live execution;
- normalize all platform research into one algorithm;
- delete source evidence to make the repository appear clean;
- migrate Product Lab or unrelated product applications unless separately authorized.

## Governing order

Owner-confirmed semantics > approved specification and ADR > source-confirmed doctrine > reviewed architectural derivation > observed legacy behavior > implementation convenience.
