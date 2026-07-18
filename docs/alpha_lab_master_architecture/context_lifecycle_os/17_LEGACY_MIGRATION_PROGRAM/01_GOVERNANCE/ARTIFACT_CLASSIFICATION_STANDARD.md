---
title: "Artifact Classification Standard"
status: proposed-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration]
---
# Artifact Classification Standard

Every file or logical artifact receives exactly one primary migration disposition:

- `KEEP_CANONICAL`
- `MOVE_WITHOUT_SEMANTIC_CHANGE`
- `WRAP_LEGACY`
- `REWRITE_WITH_PARITY`
- `EXTRACT_SHARED_LOGIC`
- `MERGE_AFTER_EQUIVALENCE_PROOF`
- `ARCHIVE_REFERENCE_ONLY`
- `QUARANTINE_UNCERTAIN`
- `DELETE_AFTER_PROOF`
- `SECURITY_RESTRICTED`

A secondary role class identifies Context, Setup, Treatment, visualization, adapter, research, diagnostic, platform, generated projection, release metadata or source evidence. Unknown classification fails closed.
