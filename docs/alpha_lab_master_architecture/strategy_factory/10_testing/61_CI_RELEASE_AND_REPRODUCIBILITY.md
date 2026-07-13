---
type: strategy-factory-document
status: canonical
title: "CI, Release, and Reproducibility"
tags:
  - strategy-factory
---

# CI, Release, and Reproducibility

Every Strategy Factory patch and strategy plugin must be independently verifiable and reversible.

## CI minimum

Python compile, pytest, manifest validation, schema tests, deterministic fixture replay, static MQL5 compatibility, documentation link check, and patch collision audit. Live adapters additionally require MetaEditor compile and Strategy Tester evidence.

## Release artifact

Root-relative additive ZIP, file index, hashes, QA report, installation commands that stage only project files, commit message, rollback, known limitations, and exact verification commands.

## Reproducibility

Fix random seeds, record dependencies, preserve input hashes, avoid unordered iteration in identities, and materialize folds. A run that cannot reproduce within declared tolerance cannot promote.

