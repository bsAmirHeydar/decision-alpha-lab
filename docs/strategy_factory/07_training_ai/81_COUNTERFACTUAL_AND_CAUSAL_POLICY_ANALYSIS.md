---
type: strategy-factory-document
status: canonical
title: "Counterfactual and Causal Policy Analysis"
tags:
  - strategy-factory
---

# Counterfactual and Causal Policy Analysis

Because only one live action can be taken, historical candidate simulation and careful counterfactual design are needed to compare policies.

## Historical counterfactuals

The outcome engine can replay multiple candidate policies on the same future path. Keep all candidates in one event cluster and never split them across folds. Recognize that bar-based fills may not capture market impact or mutually exclusive order interactions.

## Treatment framing

Anatomy, confirmation, and model decisions can be framed as treatments only when confounders and assignment are understood. Matched baselines, inverse-propensity methods, and doubly robust estimates may be explored later, but they do not create randomized evidence.

## Live counterfactuals

Shadow decisions and paper challengers provide cleaner comparisons. Contextual bandits can gather controlled exploration after safety and sample requirements are met.

## Interpretation

Use causal language conservatively. Most Strategy Factory outputs are conditional predictive evidence. Mechanism claims require stronger design and external knowledge.

