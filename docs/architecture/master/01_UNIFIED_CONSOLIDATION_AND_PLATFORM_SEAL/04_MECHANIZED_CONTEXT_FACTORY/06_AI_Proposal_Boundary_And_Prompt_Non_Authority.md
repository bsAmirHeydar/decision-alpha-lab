---
id: UCPS-DAFE136EC49E
title: "AI Proposal Boundary and Prompt Non-Authority"
type: policy
status: canonical
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-23
updated: 2026-07-23
tags:
  - consolidation
  - platform-seal
---
# AI Proposal Boundary and Prompt Non-Authority

## Allowed AI proposals

- feature and representation candidates;
- Treatment candidates;
- model and experiment candidates;
- diagnostic hypotheses;
- documentation drafts;
- code changes inside an approved extension scope.

## Forbidden authority

AI cannot modify universal lifecycle states, create new authority classes, bypass final-test locks, change known-time semantics, edit generated artifacts, silently choose unresolved Context meaning, create broker authority or add arbitrary repository roots.

## Proposal protocol

Every AI output is typed, schema-valid, provenance-recorded and reviewed by the appropriate compiler or policy. Invalid proposals are rejected without partial mutation.

## Prompt role

Prompts are interaction aids and templates. They are not contracts, source code, state transitions or approval records. If a critical requirement exists only in a prompt, the platform is incomplete.
