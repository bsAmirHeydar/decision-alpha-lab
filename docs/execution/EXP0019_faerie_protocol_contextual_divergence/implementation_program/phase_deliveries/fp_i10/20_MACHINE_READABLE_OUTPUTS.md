---
tags: [exp0019, faerie-protocol, fp-i10, indicator]
status: normative
phase: FP-I10
version: 1.0.0
last_updated: 2026-07-13
language: en
---
# Machine-Readable Outputs

## Purpose

Stable output frame for iCustom, diagnostics, testing, and future UI.

## Normative architecture

FP-I10 is the first executable Indicator product shell. It composes the accepted FP-I03 through FP-I09 contracts through one composition root. Upstream modules remain the sole authority for time, data synchronization, references, relations, confirmation, WW policy, and ledger/arbitration. The Indicator is a product boundary and state projection layer; it does not reinterpret alpha semantics.

## Deterministic procedure

1. Validate every user input and derive the canonical pair and configuration hash.
2. Validate the exact upstream phase sequence, version, contract fingerprint, health, and `NONE` authority.
3. Derive an instance identity from chart, terminal instance, pair, context epoch, and configuration hash.
4. Restore an exact checkpoint or start a bounded deterministic rebuild.
5. Process only new closed M1 work after the initial bounded history pass.
6. Aggregate module/data/history/checkpoint/performance health into READY, DEGRADED, or BLOCKED.
7. Emit the fixed twelve-channel machine-readable output frame.
8. Append lifecycle evidence and preserve instance-scoped cleanup.

## Invariants

- No order, position, broker, network, or global chart mutation authority exists.
- Two indicator instances cannot share an instance ID, namespace, checkpoint key, or lifecycle event chain.
- The exact buffer order is versioned and cannot be reordered silently.
- A repeated calculate call for the same closed minute performs no duplicate semantic work.
- Suppressed signals remain represented in counts and future visual projections.
- Missing or conflicting data blocks conclusions instead of creating synthetic evidence.
- Checkpoints are caches; incompatible checkpoints are rejected and rebuilt.

## Failure behavior

Input or dependency incompatibility fails initialization. Missing history keeps the shell degraded while bounded backfill proceeds. Data conflict or blocked upstream health produces a BLOCKED output state. Performance lag preserves semantic processing, marks DEGRADED, and continues in bounded chunks. Deinitialization only releases the current instance.

## Evidence

The phase exposes configuration hash, composition hash, instance identity, module versions, source revision, last processed M1, health reason codes, buffer frame hash, snapshot hash, lifecycle chain head, counters, and checkpoint disposition.

## Navigation

- [[00_FP_I10_DELIVERY_MOC|FP-I10 Delivery MOC]]
- [[../../phases/FP_I10_COMPLETE_INDICATOR_SHELL_ENGINE_COMPOSITION_HEALTH_AND_MACHINE-READABLE_OUTPUTS|FP-I10 Program Phase]]
- [[51_HANDOFF_TO_FP_I11|Handoff to FP-I11]]
