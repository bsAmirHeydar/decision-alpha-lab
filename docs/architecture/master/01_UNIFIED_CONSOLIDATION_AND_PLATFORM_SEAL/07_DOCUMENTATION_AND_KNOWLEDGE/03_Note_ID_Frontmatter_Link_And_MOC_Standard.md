---
id: UCPS-AA9C15313B2A
title: "Note ID, Frontmatter, Link and MOC Standard"
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
# Note ID, Frontmatter, Link and MOC Standard

## Required frontmatter

Every normative note has `id`, `title`, `type`, `status`, `domain`, `version`, `created`, `updated` and `tags`.

## IDs

IDs are stable, unique and independent of title changes. Moving a note preserves its ID unless the meaning is replaced by a new artifact.

## Links

Program notes use full vault-relative wiki paths to avoid basename ambiguity. Links to machine files use checked Markdown paths. Broken links block validation.

## MOCs

Each section has one `00_MOC.md` that links every canonical note in the section and provides navigation to Home and current status. MOCs do not contain independent architecture rules.

## Titles

Titles are precise and singular. `final`, `new`, `latest`, patch IDs and ambiguous phase-only titles are not canonical naming.
