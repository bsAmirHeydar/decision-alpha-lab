---
id: UCPS-UC01-PRESERVE-4A55BC19
title: "Preservation Architecture and Trust Model"
type: architecture_record
status: approved
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-23
updated: 2026-07-23
tags:
  - preservation
  - recovery
  - trust
---
# Preservation Architecture and Trust Model

UC-01 uses four mutually reinforcing preservation layers:

1. **Git history preservation** — an annotated tag and archive branch point to the committed pre-consolidation HEAD.
2. **Repository-object preservation** — a verified Git bundle contains every Git ref and object available to Git.
3. **Materialized-source preservation** — an external ZIP contains every included working-tree file after Git LFS checkout and after the static UC-01 implementation overlay.
4. **Behavior and structure preservation** — symbols, imports, includes, links, schemas, authority surfaces, tests and critical-domain fingerprints are recorded separately from raw source bytes.

## Trust boundaries

- Backup files live outside the repository.
- Only receipts, absolute backup locations, sizes and hashes are committed.
- Secret content is never copied into JSON reports.
- The materialized archive is verified by extraction into an isolated temporary workspace and byte-for-byte root-digest comparison.
- The temporary recovery workspace is destroyed after verification.

A Git bundle alone is insufficient for Git LFS working content. A source archive alone is insufficient for branches and historical commits. Both are required.
