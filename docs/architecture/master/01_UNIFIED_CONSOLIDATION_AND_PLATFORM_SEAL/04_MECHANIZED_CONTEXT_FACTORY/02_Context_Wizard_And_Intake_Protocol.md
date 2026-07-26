---
id: UCPS-A81CF1239F8E
title: "Context Wizard and Intake Protocol"
type: workflow
status: canonical
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-23
updated: 2026-07-23
tags:
  - consolidation
  - platform-seal
---
# Context Wizard and Intake Protocol

## Purpose

The Wizard turns human market understanding into a complete draft contract through a controlled questionnaire. It replaces fragile prompt chains with typed questions, validation, defaults and explicit unknowns.

## Interaction model

The Wizard groups questions into Doctrine, Market, Clocks, Occurrence, Data Quality, Features, Labels, Research, Treatments, Falsification, Runtime Compatibility and Authority.

## Default policy

Defaults are allowed only when they are platform-approved, displayed to the user and recorded with source and version. An unanswered high-impact question remains `UNRESOLVED` and blocks compilation.

## Outputs

- draft `context.yaml`;
- unresolved-question ledger;
- decision provenance;
- doctrine projection;
- validation preview;
- next allowed actions.

## AI use

AI may clarify language or suggest candidate answers, but the Wizard records which values are user-approved, policy-defaulted or AI-proposed. AI proposals never silently become authoritative.
