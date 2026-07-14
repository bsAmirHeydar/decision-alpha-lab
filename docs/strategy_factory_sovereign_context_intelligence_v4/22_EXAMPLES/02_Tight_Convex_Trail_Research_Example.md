---
title: P3 Tight-Convex Trail — Research Example
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v4
- example
- p3
---

# Research question

Does a tight trigger stop combined with a path-aware trail produce stable right-tail capture in a specific context family after realistic execution and selection adjustment?

## Required decomposition

- Entry quality
- Initial stop validity
- Path smoothness and persistence
- Trail activation
- Ratchet geometry
- Giveback
- Premature exit
- Tail capture
- Re-entry opportunity
- Cost and capital time

## Models

Manual trail state machine, explicit path descriptors, survival/competing-risk models, distributional models, sequence challenger, and research-only offline policy challenger.

## Disqualifying shortcuts

- OHLC-favorable intrabar ordering
- selecting trail parameters on final paths
- treating many trail variants as independent trades
- omitting non-fill or early stop cases
- reporting maximum MFE rather than realized trail outcome
