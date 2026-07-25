---
id: UCPS-72A6721A6592
title: "Qualification, Determinism and Negative Testing"
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
# Qualification, Determinism and Negative Testing

## Required qualification

UC-02 runs contract validation, static-patch verification, authority-ledger verification, differential guards, direct tests, Obsidian validation, repository policy, MQL5 static checks and deterministic rebuild.

## Negative tests

The suite proves that controls reject:

- a new root release artifact;
- a new Strategy Factory-like engine;
- a nested `src/alpha_lab` product root;
- invalid owner or disposition values;
- authority escalation;
- incomplete system disposition;
- non-deterministic output.

## Determinism

Repository, package, capability, documentation and system ledgers are sorted and compressed deterministically. Rebuilding from the same UC-01 baseline and contract set must produce identical digests.

## Non-compensatory gates

A large number of classified files cannot compensate for one unowned production capability, failed guard, invalid contract or unknown package destination.
