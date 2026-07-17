---
title: Sealed Evaluator Zone Contract
status: accepted-reference
version: 1.0.0
phase: SAED_V4_29
tags: [saed-v4, v4-29, hidden-evaluation, air-gap]
---

# Sealed Evaluator Zone Contract

## Purpose

Permits deterministic evaluation under custodian control while denying network and researcher access. This module is interpreted only inside the [[V4_29_Hidden_Evaluation_Air_Gap]] authority ceiling and cannot independently authorize model promotion, runtime compilation, capital allocation, order submission or production use.

## Contract

The input is a closed, versioned object with deterministic identity. Unknown fields, missing fields, identity mismatch, hash mismatch, temporal ambiguity or an access state not explicitly permitted by the frozen policy cause `quarantine`. No default value may silently widen access. Candidate, protocol, protected commitment, evaluator and disclosure identities are resolved before the one-shot token is issued.

## Engineering invariants

1. The research actor never receives plaintext hidden labels, key shares, row-level predictions or evaluator diagnostics.
2. The sealed evaluator performs one deterministic evaluation against one candidate commitment, one protected commitment and one protocol commitment.
3. Every permitted movement and access event is represented in a domain-separated append-only chain.
4. Result egress is projected onto the immutable disclosure allowlist and rounded to the approved precision.
5. Future suffixes, retries, interactive debugging, package installation, shell escape, network access and adaptive feedback cannot change the accepted output.

## Failure modes and response

A stale upstream certificate, candidate mutation, protocol mutation, token reuse, custody threshold failure, protected commitment mismatch, topology escape, forbidden disclosure field, non-contiguous ledger or security scanner hit is a hard failure. The safe action is quarantine; the system does not infer success, retry, select an alternative candidate or request more detailed feedback.

## Evidence and verification

Verification is performed through exact JSON schemas, canonical hashes, golden reproduction, negative fixtures, mutation tests, future-suffix invariance, authority scans, MQL5 static checks and the V4-29 delivery validator. External physical isolation, HSM custody, independent labs, MetaEditor compilation, runtime parity and broker qualification remain separately evidenced future gates.

## Relations

- Parent phase: [[V4_29_Hidden_Evaluation_Air_Gap]]
- Previous governed phase: [[V4_28_Anytime_Valid_Online_FDR]]
- Next governed phase: [[V4_30_Independent_And_Multi_Lab_Replication]]
