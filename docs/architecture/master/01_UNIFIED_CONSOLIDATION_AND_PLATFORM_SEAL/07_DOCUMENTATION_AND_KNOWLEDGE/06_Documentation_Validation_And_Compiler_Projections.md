---
id: UCPS-E18C621A0DA9
title: "Documentation Validation and Compiler Projections"
type: standard
status: canonical
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-23
updated: 2026-07-23
tags:
  - consolidation
  - platform-seal
---
# Documentation Validation and Compiler Projections

## Validation

Checks cover frontmatter, unique IDs, broken and ambiguous wiki links, Markdown links, case collisions, empty files, MOC coverage, forbidden placeholders, succession state and canonical duplicates.

## Projection compiler

Context, schema, CLI and registry references are generated from machine sources. Projection output includes source and compiler digests.

## CI

The vault validator runs in repository engineering policy. A documentation error that can misdirect operation blocks acceptance.

## Maintenance

Every platform change updates source contracts first, then regenerates projections and validates canonical explanatory notes. Manual synchronization across copied trees is prohibited.
