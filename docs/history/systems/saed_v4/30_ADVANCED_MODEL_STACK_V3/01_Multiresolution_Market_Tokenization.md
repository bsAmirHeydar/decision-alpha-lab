---
title: Multiresolution Market Tokenization
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: core-production
tags:
  - saed-v4
---

# Mission

Encode raw paths, bars, events, Context anatomy, and execution state at multiple temporal and structural resolutions without leaking future aggregation.

## Why this component exists

- None declared.

## Authority and safety boundary

- This component may estimate, rank, simulate, challenge, or recommend only inside a declared research scope.
- It cannot create canonical Context truth, modify protected evidence roles, sign promotion, change portfolio risk, activate runtime generations, access live credentials, or place orders.
- Unsupported, stale, contradictory, OOD, hash-mismatched, uncalibrated, or incomplete paths resolve to **Skip**, **Abstain**, **Manual fallback**, **Reject**, or **Quarantine**.
- Every result is subordinate to UCEE I12 promotion admission, I13 authority/fallback, I14 immutable runtime, I17 portfolio/risk, and I18 release qualification.

## Input contracts

- Bitemporal event stream.
- Context event graph.
- Treatment descriptors.

## Output contracts

- Versioned token sequences and masks.

## Algorithmic design

- Separate raw price/quote tokens, event tokens, structural tokens, lifecycle tokens, session/regime tokens, and treatment tokens.
- Use causal patching and hierarchical pooling fitted only on training roles.
- Represent time gaps, missingness, revisions, and market closures explicitly.
- Preserve absolute and relative geometry.


## Data and known-time semantics

- None declared.

## Anti-overfit and model-risk controls

- No centered windows.
- Tokenizer fit hash-bound and fold-local.
- Token vocabulary changes create new model version.

## Measurement system

- Reconstruction quality.
- Downstream uplift.
- Token stability.
- Missingness robustness.

## Scalability and operating model

- None declared.

## Adversarial failure modes

- Future bar close embedded in earlier token.
- Normalization across final data.
- Rare Context IDs become lookup leakage.

## UCEE integration

- None declared.

## Required tests and evidence

- Suffix mutation.
- Irregular sampling.
- Token permutation.
- Fold-local fit.

## Implementation slices

- None declared.

## Decision record

- None declared.

## Acceptance gate

The component is accepted only when its contracts are closed and versioned, all lineage and role boundaries are reconstructible, protected evaluation remains unexposed, negative and mutation tests pass, simpler baselines remain available, and an independent reviewer can reproduce the decision-equivalent result from immutable hashes.

## Related notes

- [[Self_Supervised_Pretraining_Curriculum]]
- [[State_Space_Transformer_Hybrid]]
