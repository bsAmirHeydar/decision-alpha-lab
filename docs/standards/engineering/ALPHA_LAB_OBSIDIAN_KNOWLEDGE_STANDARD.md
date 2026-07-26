---
id: AIEOS2-B337BC090B04
title: "Alpha Lab Obsidian Knowledge Standard"
type: standard
status: active
domain: engineering
version: 2.0.0
created: 2026-07-10
updated: 2026-07-10
tags:
  - ai-engineering
  - alpha-lab
  - engineering
---
# Alpha Lab Obsidian Knowledge Standard

## Purpose

Make project knowledge durable, navigable, versioned, and independent of chat history.

## Required Metadata

Normative notes include:

```yaml
id: stable-id
title: descriptive title
type: specification | standard | ADR | checklist | report
status: draft | active | deprecated | archived
version: semantic version
created: YYYY-MM-DD
updated: YYYY-MM-DD
owner: role/name
```

## Linking

- Each module has a MOC.
- Specifications link to implementation, tests, decisions, and evidence.
- Patches link to the contracts they change.
- Deprecated notes point to replacements.
- Duplicate sources of truth are prohibited.

## Lifecycle

```text
draft → review → active → superseded/deprecated → archived
```

Changes to normative meaning update version and changelog. Generated document cards may mirror metadata but do not become the source of truth.

## Validation

Run the vault validator before release. Broken/ambiguous links, duplicate IDs, empty notes, and unresolved placeholders outside templates are failures.
