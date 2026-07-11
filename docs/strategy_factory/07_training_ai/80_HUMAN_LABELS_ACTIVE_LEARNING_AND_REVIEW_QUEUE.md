---
type: strategy-factory-document
status: canonical
title: "Human Labels, Active Learning, and Review Queue"
tags:
  - strategy-factory
---

# Human Labels, Active Learning, and Review Queue

Your discretionary expertise can accelerate model development when captured as timestamped, structured evidence rather than post-hoc explanations.

## Label types

Anatomy correctness, ambiguity, context quality, invalidation quality, preferred policy, trade/skip, and reason codes. Separate what you knew at decision time from retrospective diagnosis.

## Active learning

The model sends uncertain, novel, or high-disagreement events to a review queue. Human review improves coverage of boundaries instead of labeling easy duplicates. Selection into the queue is logged so label prevalence is not mistaken for market prevalence.

## Teacher fallibility

Human labels are a feature or target candidate, not truth by default. Compare label consistency, inter-rater agreement where possible, outcome uplift, and model performance with and without human judgment.

## LLM support

An LLM can convert free-form review into structured reason codes, flag contradiction with canon, retrieve analogous events, and draft tests. The architect approves labels and semantic changes.

