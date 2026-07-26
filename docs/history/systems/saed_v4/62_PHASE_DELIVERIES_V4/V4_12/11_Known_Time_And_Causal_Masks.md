---
title: SAED V4-12 — Known-Time and Causal Masks
status: implemented-reference
version: 1.0.0
created: '2026-07-15'
updated: '2026-07-15'
phase: SAED_V4_12
capability_tier: governed-challenger
tags: [saed-v4, v4-12, sequence-model, state-space, evidence-governance]
---

# SAED V4-12 — Known-Time and Causal Masks

## Objective and bounded scope

Guarantee that every prefix output depends only on observations known at or before the current decision time. The implemented evidence is intentionally limited to deterministic synthetic-reference operation over the exact frozen V4-11 tokenizer and encoder checkpoint. It is not evidence of real alpha, treatment value, runtime parity or production readiness.

## Contract and invariants

1. All inputs are known-time token streams whose upstream hashes match the signed V4-11 handoff.
2. Record identifiers, context identifiers, outcome artifacts, execution results and protected evidence are forbidden model inputs.
3. Sequence order is strict event-time order within one declared root-context, domain and evidence split.
4. Hidden state is reset or rejected at every prohibited boundary; state is never silently carried across roots, domains, folds or corruption.
5. Every candidate, fit, exposure, checkpoint, parity certificate and registry decision has deterministic identity and canonical content hash.

## Engineering implementation

The reference implementation is located in `lab/11_strategy_factory/python/saed_v4_sequence_state_space/`. Closed contracts are under `lab/11_strategy_factory/schemas/saed_v4_12/`; golden evidence is under `lab/11_strategy_factory/artifacts/saed_v4_12/`; adversarial and parameterized tests are under `lab/11_strategy_factory/tests/phase_saed_v4_12_deep_sequence_state_space_models/`.

The phase compares a simple EMA recurrent floor, causal convolution, diagonal continuous-time state-space model, selective state-space model, local causal attention and a hybrid SSM-attention challenger. Core parameters are deterministic reference initializations. Only the next-frozen-representation readout is fitted, using a closed-form ridge solver and a complete exposure ledger.

## Failure modes and containment

- Any upstream hash mismatch blocks construction.
- Any future, outcome, execution or identity token causes a fail-closed causality error.
- Any non-finite numeric value, singular solve, invalid dimension or budget excess blocks the candidate.
- Streaming, chunk or restart parity failure quarantines the checkpoint.
- Collapse, corrupted snapshot or unknown contract field blocks registry admission.
- Missing external evidence remains an explicit limitation rather than being inferred from local tests.

## Verification evidence

The local reference evidence includes closed-schema validation, deterministic golden reproduction, future-suffix mutation, batch/streaming parity, chunk parity, snapshot/restart parity, state stability, collapse checks, baseline preservation, Python authority scanning, Obsidian validation and MQL5 static scanning. Actual MetaEditor compilation, GPU reproduction, real-corpus training, prospective paper, shadow and live qualification are not claimed.

## Authority Boundary

SAED V4-12 may build and compare research challengers and may emit a hash-frozen handoff to V4-13. It may not predict trade outcomes as an authoritative service, rank or select treatments, allocate risk, activate a runtime generation, submit an order, sign promotion or bypass UCEE I12–I18.

## Related controls

- [[00_Phase_Charter|Phase Charter]]
- [[04_Authority_Boundary|Authority Boundary]]
- [[25_Streaming_Batch_Parity|Streaming-Batch Parity]]
- [[40_Immutable_Checkpoint_Registry|Immutable Checkpoint Registry]]
- [[56_V4_13_Handoff|V4-13 Handoff]]
