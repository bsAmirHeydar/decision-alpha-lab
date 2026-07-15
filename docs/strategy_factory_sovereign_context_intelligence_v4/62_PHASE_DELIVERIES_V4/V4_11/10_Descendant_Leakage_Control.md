---
title: SAED V4-11 — Descendant Leakage Control
status: implemented-reference
version: 1.0.0
created: '2026-07-15'
updated: '2026-07-15'
tags:
  - saed-v4
  - v4-11
  - self-supervised-pretraining
---

# SAED V4-11 — Descendant Leakage Control

## Decision

Treats a root Context and all descendants as one indivisible split group and audits cross-split ancestry. This control is implemented for the deterministic synthetic-reference path and is subordinate to the V4-10 evidence boundary and UCEE authority model.

## Contract

The accepted input must carry immutable identity, evidence role, event time, known time, source lineage and exact version. The accepted output must be canonical JSON or source text with a stable content hash. The control may emit research evidence only; it cannot create alpha, treatment, risk, runtime or execution authority.

## Mandatory engineering requirements

1. Preserve exact upstream identities and content hashes; never rewrite V4-10 evidence.
2. Reject unknown fields, missing required fields, non-finite values and unsupported evidence roles.
3. Record every decision-relevant transformation in a deterministic, content-addressed artifact.
4. Keep outcome, protected, prospective, shadow and live information outside encoder inputs.
5. Resolve uncertainty by rejection or quarantine rather than silent fallback.

## Failure modes and deny behavior

- A hash, identity, role or known-time mismatch blocks the entire bundle.
- A forbidden token, source class, canary, cross-split root or duplicate source hash produces quarantine evidence.
- Incomplete exposure, non-deterministic replay, collapsed representations or checkpoint tampering prevents registry admission.
- Missing external evidence remains explicitly `not_claimed` or `pending_local_windows`; local tests cannot be promoted into operational claims.

## Verification evidence

Verification is performed through closed JSON Schemas, golden fixtures, negative and mutation tests, deterministic training replay, semantic diff, contamination and membership audits, control comparisons, boundary scanning, MQL5 static validation, Obsidian validation, file inventory and SHA-256 ledger. Reviewers must use exact artifact hashes rather than narrative equivalence.

## Residual limitation

The delivered corpus and learned checkpoint are synthetic references. They establish architecture, determinism and governance; they do not establish real-market transfer, economic edge, prospective performance, runtime parity, broker compatibility or production readiness.

## Related controls

- [[09_Identity_And_Time_Splits|Previous control]]
- [[11_Tokenizer_Contract|Next control]]
- [[../V4_10/45_V4_11_Handoff|V4-10 handoff]]
- [[../../60_IMPLEMENTATION_PROGRAM_V4/V4_11_Self_Supervised_Context_Pretraining|V4-11 program]]
