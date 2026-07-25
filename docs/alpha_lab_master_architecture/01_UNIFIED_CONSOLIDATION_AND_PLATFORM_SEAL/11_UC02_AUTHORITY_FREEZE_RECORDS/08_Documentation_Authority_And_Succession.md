---
id: UCPS-825D7C44EA76
title: "Documentation Authority and Succession"
type: execution-record
status: approved
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-24
updated: 2026-07-24
tags:
  - consolidation
  - uc02
  - authority-freeze
---
# Documentation Authority and Succession

## Document classes

1. `NORMATIVE_AUTHORED` — architecture, standards, policies, ADRs and runbooks.
2. `CONTEXT_AUTHORED` — Context doctrine, limitations, falsification and operation.
3. `GENERATED_PROJECTION` — references generated from machine contracts.
4. `HISTORICAL_RELEASE` — superseded phase, patch, QA, installation and rollback evidence.

## Authority priority

Machine contract outranks human normative explanation; the human explanation outranks generated projection; historical release material cannot override current authority.

## One concept, one authority

A concept cannot have several simultaneously authoritative documents. Obsidian is the human knowledge projection of contracts and decisions, not an independent source of runtime semantics.

## Succession

Replacing a document requires successor identity, source hash, bounded redirect window, consumer-link rewrite and archive evidence. Permanent redirects and silent deletion are prohibited.

## UC-03 implication

Documentation movement is handled as a dedicated wave so code moves do not silently break Obsidian links, generated references or external consumers.
