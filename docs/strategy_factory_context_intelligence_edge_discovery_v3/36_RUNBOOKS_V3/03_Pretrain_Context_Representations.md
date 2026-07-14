---
title: Pretrain Context Representations
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: canonical
tags:
  - saed-v3
  - runbook
  - operations
---

# Mission

Train role-safe self-supervised encoders and evaluate transfer without using outcomes or protected evidence.

## Entry conditions

- Approved pretraining corpus manifest.
- Tokenizer and curriculum.
- Compute budget and contamination plan.

## Mandatory roles and separation of duties

- Representation lead.
- Data leakage sentinel.
- Compute engineer.
- Independent evaluator.

## Procedure

1. Build fold/role-safe token streams.
2. Run contamination and membership canaries.
3. Train curriculum checkpoints.
4. Evaluate reconstruction, linear probes, few-shot transfer, and collapse.
5. Compare random, frozen, and from-scratch controls.
6. Register admitted encoders.

## Mandatory outputs

- Encoder checkpoints.
- Corpus and SBOM.
- Representation dossier.
- Rejected checkpoint ledger.

## Stop and escalation conditions

- Protected data exposure.
- Canary memorization.
- No uplift versus simple controls.
- License/provenance issue.

## Evidence retained

- Training logs.
- Checkpoint hashes.
- Probe results.
- Contamination tests.

## Completion gate

The runbook is complete only when all required artifacts are content-addressed, all exposures and deviations are recorded, an independent reviewer signs the completion state, and the downstream UCEE gate accepts the exact immutable bundle rather than a narrative summary.

## Related notes

- [[Self_Supervised_Context_Pretraining]]
- [[Foundation_Model_Intake_V3]]
