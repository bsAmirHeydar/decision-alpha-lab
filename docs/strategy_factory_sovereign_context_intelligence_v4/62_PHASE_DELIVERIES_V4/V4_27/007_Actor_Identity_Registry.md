---
title: V4-27 Delivery 007 — Actor Identity Registry
status: accepted-reference
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
tags:
  - saed-v4
  - v4-27
  - search-ledger
  - exposure-ledger
---

# Actor Identity Registry

## Normative statement

**Actor Identity Registry** is a mandatory control in the V4-27 complete-search and exposure-accounting boundary. The control is evaluated over frozen V4-26 lineage, exact actor identities, exact data roles, immutable experiment manifests, terminal trial histories and append-only exposure events. Unknown, missing, stale, contradictory or non-replayable states resolve fail-closed.

## Engineering contract

The implementation records a deterministic identity, known-time coordinates, data-role semantics, parent lineage where applicable, and a content hash. It cannot mutate a candidate model, select a treatment, alter a risk limit, compile a runtime bundle or invoke broker execution. All materially related events remain inside the multiplicity universe that V4-28 will use for anytime-valid false-discovery control.

## Verification

Verification includes positive, negative, boundary and mutation tests. The golden reference requires exact replay, a valid SHA-256 chain head, zero hidden-evaluation queries, zero protected-evidence exposures, complete failed/pruned/retry/duplicate accounting and zero authority flags. Static MQL5 mirrors are contract evidence only; they are not MetaEditor, runtime-parity or broker-qualification evidence.

## Failure response

A violation rejects the research certificate, preserves the previous accepted baseline, emits no promotion or runtime artifact and routes the record to explicit remediation. Silence, omission and untracked manual work are failures rather than neutral states.

## Related

- [[00_MOC_V4_27_Complete_Search_And_Exposure_Ledger]]
- [[V4_27_Complete_Search_And_Exposure_Ledger]]
- [[V4_28_Anytime_Valid_Online_FDR]]
- [[006_Handoff_Scope_Verification]]
- [[008_Human_Actor_Contract]]
