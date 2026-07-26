---
title: "Phase 01 Broker-Symbol Compatibility Hotfix"
status: implemented
phase: PHASE_03
language: en
tags:
  - strategy-factory
  - phase03
  - mql5
  - market-services
---

# Issue

Phase 01 originally applied internal safe-identifier grammar to terminal symbols. This rejected legitimate broker symbols such as `#US30`.

## Correction

A separate terminal-symbol validator was added in both MQL5 and Python. It permits common prefixes and suffixes while forbidding:

- control and space characters;
- canonical wire delimiters;
- quotes;
- backslashes;
- empty or oversized symbols.

`BarRecord` and `AnatomyEvent` now use terminal-symbol validation for symbol fields. Internal IDs, versions, session names, and hashes continue to use strict identifier grammar.

## Why this is architectural

External broker identifiers and internal canonical identifiers have different trust and compatibility requirements. Conflating them either blocks real deployments or weakens internal serialization safety.

## Compatibility

Canonical IDs include the exact broker symbol. Therefore two brokers using different symbol names produce different IDs unless a future canonical instrument mapping is explicitly added. That is intentional for now because feed and contract semantics may differ.
