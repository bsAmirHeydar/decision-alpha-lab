---
title: Complete Trial and Exposure Ledger
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v3
- core-production
---

# Purpose

Record every scientific attempt and every human or agent exposure to protected evidence.

## Capability tier

**Core Production**

## System design

### Trial states

Proposed, compiled, duplicate, invalid, running, pruned, failed, timed out, cancelled, completed, selected, rejected.

### Exposure events

Opening dashboards, inspecting examples, reading metrics, agent summaries, exporting rows, or modifying hypotheses after protected evidence.

### Hash chain

Ledger entries are append-only and hash-linked.

### Multiplicity scope

All materially related trials and exposures feed selection-risk calculations.

## Input contracts

- `ExperimentManifest`
- `ActorIdentity`
- `DataRole`

## Output contracts

- `TrialLedger`
- `ExposureLedger`
- `MultiplicityUniverse`

## Measurement framework

- Ledger completeness.
- Orphan-run count.
- Exposure count by data role.
- Hash-chain integrity.

## Adversarial questions

- Are local notebooks missing?
- Are failed seeds omitted?
- Does an agent summarize final-test rows without logging exposure?

## Mandatory controls

1. Exact upstream hashes and data roles are recorded.
2. Candidate and failure ledgers are complete.
3. Costs, capacity, missingness, censoring, and support are explicit.
4. Validation uses chronological, cluster-aware, purged folds.
5. Advanced outputs cannot bypass manual policy, hard risk, portfolio, or UCEE promotion.
6. Any runtime handoff requires deterministic export, parity, latency, fallback, and revocation evidence.

## Acceptance boundary

Passing research metrics is necessary but never sufficient. The component remains non-authoritative until its evidence is admitted through UCEE I12, compiled by I14, challenged prospectively under I15, bounded by I17, and qualified under I18.

## Related notes

- [[Research_Exposure_And_Data_Role_Firewall]]
