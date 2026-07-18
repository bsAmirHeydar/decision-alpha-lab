---
title: ACL-11 01 — Mission Scope and Non Claims
status: accepted-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, acl-11, phase-delivery]
---
# ACL-11 01 — Mission Scope and Non Claims

## Purpose

This delivery unit specifies mission scope and non claims within the runtime parity and custody boundary. It is independently reviewable and links machine contracts, failure semantics and evidence obligations.

## Contract

Inputs remain content-addressed and immutable. Outputs use closed schemas and registered reason codes. Missing, UNKNOWN, incompatible or unauthorized material fails closed.

## Reference behavior

The upstream runtime-candidate count is zero. No runtime generation, signature, activation, order or capital authority is produced.

## Verification

Unit, security-negative, deterministic replay and clean-overlay validation apply. External MetaEditor, Strategy Tester, broker and production-key evidence is not claimed.

## Related

- [[ACL11_RUNTIME_PARITY_AND_CUSTODY_RUNTIME]]
- [[ACL11_ACL12_HANDOFF]]
