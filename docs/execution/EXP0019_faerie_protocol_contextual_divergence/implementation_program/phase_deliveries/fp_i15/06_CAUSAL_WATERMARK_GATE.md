---
title: "FP-I15 — Pair data completeness and causal finality"
tags: [exp0019, faerie-protocol, fp-i15, paper-execution, obsidian]
status: implemented-source-accepted
phase: FP-I15
phase_version: 1.0.0
doc_version: 1.0.0
last_updated: 2026-07-13
language: en
---
# Pair data completeness and causal finality

## Purpose

Pair data completeness and causal finality. This note is normative for the FP-I15 source release and is implemented by `fp_i15_paper`, the MQL5 contract mirror under `I15`, the paper-only EA, the closed schemas, and the accepted test fixtures.

## Deterministic contract

1. The admitted signal must be the active pair-session winner already selected by FP-I09.
2. FP-I14 diagnostic consensus, configuration hash, source revision, and causal data completeness must match.
3. The protected symbol is the only trade symbol. The raw structural stop is supplied by the setup adapter and is never guessed here.
4. BUY uses Ask and leaves the structural stop unchanged. SELL uses Bid and adds exactly one contemporaneous `Ask-Bid` spread to the raw stop before sizing.
5. Fixed-dollar volume is floored to the broker volume step using the worst-case entry inside the configured adverse-slippage budget. Estimated stop loss may not exceed the configured risk amount.
6. Every transition is reason-coded, identity-bearing, append-only, and reproducible from the event stream.
7. Paper quota policies are explicit simulation profiles. `FP-DEC-012` remains `UNSET`; no paper profile is represented as owner-confirmed live behavior.

## Implementation linkage

- Python package: `lab/10_infrastructure/EXP0019_faerie_protocol/phase_i15/python/fp_i15_paper`
- MQL5 mirror: `mql5/Include/AlphaLab/EXP0019/FaerieProtocol/I15`
- Product: `mql5/Experts/EXP0019/FaerieProtocol/EXP0019_FaerieProtocol_Paper.mq5`
- Self-test: `mql5/Experts/EXP0019/FaerieProtocolTests/EXP0019_FP_I15_PaperSelfTest.mq5`
- Tests and fixtures: `lab/10_infrastructure/EXP0019_faerie_protocol/phase_i15/tests`

## Failure behavior

- Missing diagnostic acceptance, mismatched config/revision, incomplete pair data, or non-winner signal blocks plan creation.
- Missing or crossed quote blocks geometry. SELL with unavailable zero spread is blocked.
- Invalid stop side, minimum-distance breach, minimum-volume risk breach, or maximum-loss breach blocks the plan without deleting the original signal.
- A second signal cannot acquire a paper reservation while the pair-session quota is reserved or consumed.
- Illegal lifecycle transitions and event-ID collisions fail closed.
- Invalid checkpoints are discarded and rebuilt; historical paper evidence is not rewritten.

## Evidence and tests

The acceptance suite covers positive BUY/SELL geometry, exact spread adjustment, risk cap, all six paper quota profiles, rejection/cancellation/partial-fill paths, revalidation, checkpoint corruption, restart parity, MQL5 authority scanning, and clean-baseline patch replay. Local MetaEditor compile and same-terminal paper runtime remain external evidence gates.

## Operational consequence

This phase enables controlled synthetic execution research while retaining zero broker authority. Live initialization and order submission remain disabled until FP-I16 freezes or migrates `FP-DEC-012` and all local acceptance gates pass.

## Change policy

A change to entry source, spread transformation, stop normalization, sizing equation, target R, policy consume event, releasable reason set, or quota key is behavior-bearing. It requires a version bump, new golden vectors, restart migration evidence, and differential review against FP-I09 and FP-I14.

## Navigation

- [[00_FP_I15_DELIVERY_MOC|FP-I15 Delivery MOC]]
- [[../../phases/FP_I15_RISK_GEOMETRY_PAIR-SESSION_RESERVATION_AND_PAPER_EXECUTION|FP-I15 Program Phase]]
- [[../../../39_QUOTA_CONSUMPTION_EXPLAINER_AND_OPEN_DECISION|FP-DEC-012 Explainer]]
