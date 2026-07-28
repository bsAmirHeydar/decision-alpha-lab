---
id: UCPS-N1-01-HARDENING
title: "UC04-W1B-N1 Native Host Qualification Hardening"
type: engineering-record
status: canonical
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-28
updated: 2026-07-28
tags:
  - consolidation
  - uc04
  - w1b
  - metaeditor
  - mt5
---
# UC04-W1B-N1 Native Host Qualification Hardening

## Intent

Close the operational uncertainty between accepted W1B tooling and real Windows/MetaEditor/MetaTrader evidence. The stage changes no production source. It provides one deterministic host runner that performs the already-approved compile and runtime evidence contract without writing into tracked repository paths.

## Current behavior

W1B-Q contains the candidate characterization, a test-only runtime script, an independent reviewer and a non-apply cutover candidate generator. The formal exit decision remains `ACCEPTED_TOOLING_NATIVE_EXECUTION_PENDING`; production materialization and consumer cutover are false.

## Desired behavior

The Windows host runner shall:

1. require a clean tracked working tree;
2. replay Engineering Policy, W0, W1A, W1B and W1B-N1 verifiers;
3. derive the terminal data directory from the repository's enclosing `MQL5` tree and `origin.txt`;
4. compile twelve frozen targets in an isolated `%LOCALAPPDATA%` mirror;
5. use documented MetaEditor switches `/compile`, `/include` and `/log`;
6. reject stale EX5/log artifacts and require `0 errors, 0 warnings`;
7. run one script with live trading and DLL imports disabled;
8. require thirteen byte-exact runtime fixtures and one PASS summary;
9. recompute evidence through the independent Python reviewer;
10. optionally generate a non-apply cutover candidate outside the repository;
11. export a sanitized evidence ZIP with host paths removed;
12. prove that tracked repository state is unchanged.

## Invariants

- Candidate ID and engine ID do not change.
- Ten consumer files and forty-one call sites do not change.
- No production include is materialized.
- No helper is deleted.
- No Entry, Treatment, Execution, Stop, Target, Risk, Context, feature, label, model or Train semantics change.
- Runtime, order and capital authority remain false.
- Compilation and runtime occur only on frozen test/consumer sources.

## Non-goals

- applying the generated cutover candidate;
- modifying any production consumer;
- proving strategy profitability or execution correctness;
- connecting evidence to automatic promotion;
- performing Git add, commit or push.

## Exit

Tooling acceptance does not close W1B. The next gate is a real Windows run that produces both `native_acceptance_receipt.json` and `independent_native_review.json` with PASS status.
