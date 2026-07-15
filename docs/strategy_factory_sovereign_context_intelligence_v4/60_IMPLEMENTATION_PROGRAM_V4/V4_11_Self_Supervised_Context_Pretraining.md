---
title: V4-11 Self-Supervised Context Pretraining
status: implemented-reference
version: 1.0.0
created: '2026-07-13'
updated: '2026-07-15'
capability_tier: research-reference
tags:
  - saed-v4
  - implementation
  - self-supervised
  - representation-learning
---

# Phase V4-11: Self-Supervised Context Pretraining

## Mission

Build the first learned Context representation in SAED V4 without crossing the evidence, known-time, treatment-selection, portfolio-risk, runtime, or execution boundaries. The accepted output is a deterministic, content-addressed, synthetic-reference encoder checkpoint and its complete evidence bundle. It is not an alpha model, treatment ranker, trading policy, runtime bundle, or production authorization.

## Implemented capability

V4-11 now includes a closed corpus contract, identity-and-time split manifest, canonical multimodal and hypergraph tokenization, view masks, deterministic masked-span augmentation, dependency-safe negative sampling, seven self-supervised objectives, staged curriculum, deterministic embedding trainer, complete exposure accounting, canonical JSON checkpointing, contamination and membership audits, representation collapse checks, non-outcome structural probes, random and frozen controls, immutable checkpoint registration, independent replay, semantic diff, SBOM, telemetry, incident template, MQL5 static mirror, and a hash-frozen handoff to V4-12.

## Authority boundary

The phase may train and register only the reference-synthetic representation. Outcome cube, execution twin, benchmark result, protected-final, prospective, shadow, and live artifacts are prohibited as encoder inputs. The phase cannot predict outcomes, rank or select treatments, allocate risk, activate runtime generations, or place orders.

## Evidence status

Local Python contracts, golden fixtures, negative and mutation tests, deterministic replay, schema closure, boundary scanning, MQL5 static validation, and Obsidian validation are included. Real-corpus training, distributed/GPU reproduction, MetaEditor compilation, prospective paper, shadow, micro-live, and live evidence are not claimed.

## Downstream handoff

The next phase is [[V4_12_Deep_Sequence_And_State_Space_Models|V4-12 Deep Sequence and State-Space Models]]. V4-12 may read the exact frozen tokenizer and encoder checkpoint hashes and build reference challengers. It may not mutate V4-11 evidence identities or infer decision authority from representation quality.
