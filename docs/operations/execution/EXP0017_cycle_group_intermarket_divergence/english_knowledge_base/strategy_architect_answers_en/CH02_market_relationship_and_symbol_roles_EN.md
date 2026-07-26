# EXP0017 Chapter 02 — Market Relationship and Symbol Roles

> English knowledge-base version of the Strategy Architect doctrine. This document preserves the base doctrine while making the project readable for English implementation, review, collaboration, and future modeling.

## Core Thesis

SPXUSD and NDXUSD are deeply related, but neither symbol receives permanent leadership status in the base version.

## Locked Doctrine

- The relationship is historical, price-based, relative, and structurally sticky because of shared index composition.
- SPXUSD may represent broader market flow, but this is not a fixed authority rule.
- Both symbols are valid hunters and clean symbols.
- The non-hunting symbol is the trade candidate in every confirmed divergence.

## Implementation Consequences

- Compare each symbol only against its own reference.
- Do not compare raw prices between SPXUSD and NDXUSD.

## What This Chapter Does Not Allow

- It does not permit premature ranking.
- It does not permit untested filtering.
- It does not permit AI-driven mutation of the current strategy.
- It does not replace statistical testing with visual or emotional judgment.

## Required Traceability

Every code module that implements this doctrine should produce inspectable state: timestamps, cycle IDs, references, hunt states, divergence states, confirmation states, invalidation states, and report fields where relevant.
