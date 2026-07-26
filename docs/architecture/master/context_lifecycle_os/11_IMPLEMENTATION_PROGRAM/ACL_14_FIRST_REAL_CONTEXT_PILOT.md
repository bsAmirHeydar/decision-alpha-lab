---
title: ACL-14 — First Real Context Pilot
status: accepted-reference
version: 2.0.0
updated: 2026-07-18
tags: [acl-os, acl-14, real-context-pilot]
---
# ACL-14 — First Real Context Pilot

ACL-14 consumes the exact `ACL13_TO_ACL14` package, authors an immutable first-real-Context pilot contract and evaluates whether all prerequisites for a separately authorized no-send prospective pilot are present.

## Responsibility boundary

ACL-14 owns Context identity, independent approval, data mapping, availability semantics, precommitted period, frozen evaluation/search rules, support targets, stop/failure conditions and the non-capital boundary. The reference implementation does not execute a pilot or create prospective outcomes.

## Required inputs

- exact ACL-13 manifest, receipt, decision, evidence, events, provenance and handoff;
- ACL-14 action-bound permit;
- approved Context identity and doctrine;
- independent Context owner and pilot reviewer;
- approved real data sources with source digests;
- versioned data mapping and externally verified availability semantics;
- precommitted pilot period;
- frozen outcomes, metrics, setup families and missingness behavior;
- support, stop and failure contracts;
- strict no-send, non-capital boundary.

## Produced artifacts

A pilot contract, approval bundle, mapping and availability contracts, evaluation/search freezes, support/stop/failure contracts, readiness matrix, non-capital decision, explicit empty execution manifest, reports, event ledger, provenance graph, receipt, manifest and `ACL14_TO_ACL15` handoff.

## Reference result

The bundled fixture is explicitly representative and not real market evidence. It proves mechanics and therefore produces `PILOT_CONTRACT_AUTHORED_REAL_EVIDENCE_REQUIRED`, not pilot readiness or prospective evidence.

## Non-negotiable invariants

- Reference or synthetic material never becomes real evidence.
- UNKNOWN mandatory gates block readiness.
- The search space and evaluation rules cannot change after outcomes are observed.
- No pilot execution, broker connection, runtime activation, order submission or capital allocation is authorized.
- A real pilot package must be rebuilt from approved inputs before start.

## Verification obligations

Direct tests, ACL-13 regression, schema/policy validation, hostile security tests, deterministic replay, event/provenance verification, MQL5 forbidden-API scan and clean-overlay delivery validation.

## Handoff

ACL-15 receives the immutable pilot package and may register fleet/closure contracts. It may not invent pilot outcomes or bypass validation, promotion, runtime custody or security.

## Claim ceiling

`FIRST_REAL_CONTEXT_PILOT_REFERENCE_ONLY`
