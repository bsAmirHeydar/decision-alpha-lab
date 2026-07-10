---
id: EXP0018-P06-DOD
title: "P06 Definition of Done"
type: implementation-note
status: implemented
project: EXP0018
phase: P06
version: 2.0.0
created: 2026-07-10
updated: 2026-07-10
tags:
  - exp0018
  - p06
  - confirmation
---

# Definition of Done

- exact host timeframe resolution works;
- both symbols must share the same host-bar timestamp;
- fresh attach produces no retroactive candidate;
- live one-sided transition opens one candidate;
- first host close emits one typed final outcome;
- double hunt cannot confirm;
- source availability through close is required;
- duplicate callbacks cannot duplicate results;
- restart before close restores pending state;
- missed close fails closed;
- confirmed geometry is Hunter-local;
- HIGH/LOW remain non-directional;
- no lifecycle, drawing, risk, or execution authority exists;
- contract, fixtures, validator, tests, docs, Obsidian, install, manifest, and rollback are present;
- MetaEditor zero-error evidence remains required on the target terminal.
