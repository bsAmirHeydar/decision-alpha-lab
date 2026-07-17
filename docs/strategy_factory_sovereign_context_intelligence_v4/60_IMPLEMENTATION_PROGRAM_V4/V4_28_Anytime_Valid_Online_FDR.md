---
title: V4-28 Anytime Valid Online FDR
status: accepted-reference
version: 1.0.0
created: '2026-07-16'
updated: '2026-07-16'
capability_tier: core-production-reference
tags:
  - saed-v4
  - implementation
  - online-fdr
  - anytime-valid
  - multiplicity
---

# Phase V4-28: Anytime Valid Online FDR

## Executive status

V4-28 is implemented as a closed, deterministic, research-only reference capability. It consumes the immutable and complete search/exposure universe certified by [[V4_27_Complete_Search_And_Exposure_Ledger]], assigns predictable family-level alpha budgets, validates anytime evidence at known time, executes an online false-discovery procedure, records every alpha spend and reward in an append-only wealth chain, and emits an append-only rejection chain.

The accepted reference does **not** claim a universal real-world FDR guarantee. Statistical validity still depends on the assumptions of the selected procedure, the quality of the anytime-valid evidence process, dependence structure, correctness of the complete hypothesis universe, and preservation of known-time ordering. It does not access hidden evaluation evidence and has no promotion, runtime, risk, execution, or production authority.

## Mission

Create the governed selection-risk layer between complete search accounting and protected hidden evaluation. The phase makes multiplicity treatment explicit and replayable rather than leaving repeated search, optional stopping, human inspection, agent inspection, retries, and adaptive experiment choice outside the evidence record.

## Upstream contract

The exact V4-27 certificate, handoff, multiplicity universe, complete trial ledger, complete exposure ledger, and integrity report are immutable inputs. Hash mismatch, missing family, incomplete trial history, incomplete exposure history, or nonzero protected-evidence access causes fail-closed rejection.

## Core capabilities

1. Closed anytime-evidence contract with running-min anytime p-values and nonnegative e-values.
2. Known-time selection of the last admissible look at or before decision time.
3. Future-suffix invariance and explicit accounting of discarded future looks.
4. Frozen predictable family allocation over the complete V4-27 family universe.
5. Deterministic gamma sequence with exact normalization and nonincreasing weights.
6. Primary LORD++-style wealth-capped reference procedure.
7. Alpha-spending, alpha-investing, SAFFRON-style, ADDIS-style, and e-LOND challengers.
8. Append-only wealth ledger with sequence, previous hash, entry hash, spend, reward, and post-decision wealth.
9. Append-only rejection ledger requiring an auditable threshold crossing.
10. Registered predictable stopping rules with fixed look budgets and no future-data use.
11. Synthetic truth audit for deterministic QA only; never promoted to a real-world guarantee.
12. Explicit UCEE authority boundary and handoff to [[V4_29_Hidden_Evaluation_Air_Gap]].

## Mathematical contract

Let the global target be `q`. Each frozen family `f` receives `q_f = q * w_f`, with nonnegative weights summing exactly to one. At family-local test index `t`, the procedure computes a predictable threshold `alpha_{f,t}` using only information known strictly before the decision. A p-based rejection requires `p_{f,t} <= alpha_{f,t}`. An e-based rejection requires `e_{f,t} >= 1 / alpha_{f,t}`. Alpha is capped by the family budget and current research wealth. Wealth must never become negative.

The gamma sequence is finite, deterministic, nonincreasing, nonnegative, and normalized to one. No threshold may be retroactively changed after observing the current or future evidence. Every threshold, evidence hash, rejection, reward, and wealth transition is committed to a hash chain.

## Evidence firewall

Hidden evaluation and protected-final roles remain outside V4-28. The phase accepts only public, synthetic, train, validation, stress, and negative roles. Any hidden or protected access is a boundary violation, not an input to the online FDR procedure.

## Accepted evidence

The reference fixture contains 36 ordered synthetic hypotheses across six frozen families, three prespecified looks per hypothesis, three intentionally appended future looks, six registered procedures, a 256-term gamma sequence, deterministic golden artifacts, closed JSON schemas, extensive mutation tests, static MQL5 mirrors, an authority-boundary scan, and a reproducible QA bundle.

## Claim ceiling

V4-28 may claim only that the local closed reference implementation deterministically enforces its contracts on the attached fixture. It may not claim real alpha, universal FDR control, prospective success, hidden-evaluation validity, independent replication, model promotion, runtime parity, broker qualification, live execution, or production authorization.

## Acceptance gates

- Exact V4-27 hashes verified.
- Complete hypothesis-family universe preserved.
- Closed contracts reject unknown fields.
- Gamma sequence normalized and nonincreasing.
- Family weights frozen and normalized.
- Evidence uses only known-time looks.
- Future suffixes do not alter decisions.
- Wealth remains nonnegative.
- Every rejection crosses its registered threshold.
- Wealth and rejection hash chains verify.
- Synthetic fixture FDP remains within target.
- Security and authority scans pass.
- Golden replay is byte-equivalent at the JSON object level.

## Handoff

The next phase is [[V4_29_Hidden_Evaluation_Air_Gap]]. V4-29 may build sealed evaluator identity, one-shot query tokens, protected dataset custody, irreversible query commitment, air-gap transport receipts, and result-redaction policy. It may not infer promotion or runtime authority from V4-28.
