---
type: strategy-factory-document
status: canonical
title: "Candidate Universe Engine"
tags:
  - strategy-factory
---

# Candidate Universe Engine

The candidate engine transforms one anatomy event into a bounded, declared set of execution hypotheses.

## Candidate, not optimized trade

A candidate is an entry/stop/exit/time/cost contract known before the path unfolds. The engine enumerates allowed combinations, filters declared incompatibilities, assigns deterministic identity, and validates geometry. It does not choose the best candidate using future data.

## Bounded search

Cartesian products explode quickly. Each manifest sets a maximum candidate count and must declare pruning rules independent of outcomes. Candidate families should represent meaningful execution hypotheses, not a dense numeric grid designed to mine history.

## Shared and plugin policies

Built-ins cover market confirmation, reference limit, retracement, breakout, anatomy invalidation, reference extreme, ATR buffer, fixed R, explicit target, and time-only exits. New policies implement a small interface and receive tests; they do not fork the engine.

## Candidate identity

Identity includes event, policy IDs, parameters, prices, manifest hash, and simulation semantics. Two candidates with different reward R or ambiguity policy are distinct research trials.

